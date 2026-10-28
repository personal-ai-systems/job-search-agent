#!/usr/bin/env python3
"""Read-only, review-oriented PDF checks. No document edits or external calls."""

import argparse
from collections import Counter
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys

import pdfplumber

TEXT_TOKEN_PATTERN = re.compile(r"(?<![\w:/])(?:[A-Za-z]+:[A-Za-z]+|:[A-Za-z]{2,})\b")


def text_layer_findings(text, expected_phrases=()):
    findings = []
    for code, pattern in (
        ("suspect-extracted-token", TEXT_TOKEN_PATTERN),
        ("unmapped-extracted-glyph", re.compile(r"\ufffd|\(cid:\d+\)")),
    ):
        samples = Counter(pattern.findall(text))
        if samples:
            findings.append({"code": code, "samples": dict(samples),
                             "explanation": "Extraction heuristic, not proof of a spelling or visual defect. Compare native text and another parser; never auto-replace."})
    normalized = " ".join(text.split())
    for phrase in expected_phrases:
        if " ".join(phrase.split()) not in normalized:
            findings.append({"code": "expected-text-not-extracted", "expected": phrase})
    return findings


def font_name(value):
    return re.sub(r"^[A-Z]{6}\+", "", value or "unknown")


def font_family(value):
    return re.sub(r"(?:[-, ]?(?:BoldItalic|BoldOblique|Bold|Italic|Oblique|Regular|Roman))$", "", value)


def extract_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n\f\n".join(page.extract_text() or "" for page in pdf.pages)


def audit(path, profile=None, reference=None, formatting_only=False):
    path = Path(path)
    profile_supplied = profile is not None
    profile = profile or {}
    config = profile.get("pdf_audit", profile)
    allowed = set(config.get("allowed_fonts", []))
    symbols = config.get("symbol_fonts", {})
    findings, pages, texts = [], [], []

    def issue(code, page=None, **details):
        findings.append({"code": code, "page": page, **details})

    with pdfplumber.open(path) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            chars = [char for char in page.chars if char.get("text", "").strip()]
            text = page.extract_text() or ""
            texts.append(text)
            fonts = Counter(font_name(char.get("fontname")) for char in chars)
            pages.append({"page": number, "width": page.width, "height": page.height,
                          "visible_characters": len(chars), "fonts": dict(fonts)})
            if not chars and not page.images:
                issue("empty-page", number)
            unusual = Counter()
            lines = {}
            for char in chars:
                font = font_name(char.get("fontname"))
                is_symbol = char["text"] in symbols.get(font, [])
                if allowed and font not in allowed and not is_symbol:
                    unusual[(font, char["text"])] += 1
                if char["x0"] < -0.5 or char["x1"] > page.width + 0.5 or char["top"] < -0.5 or char["bottom"] > page.height + 0.5:
                    issue("out-of-page-glyph", number, text=char["text"], font=font)
                if not is_symbol:
                    key = round(char["bottom"] / 2) * 2
                    lines.setdefault(key, []).append(char)
            if unusual:
                issue("unexpected-font", number, samples=[{"font": font, "text": char, "count": count}
                      for (font, char), count in unusual.most_common(20)])
            for baseline, line in lines.items():
                families = Counter(font_family(font_name(char.get("fontname"))) for char in line)
                if len(families) > 1:
                    issue("mixed-font-family-line", number, baseline=baseline, families=dict(families),
                          text="".join(char["text"] for char in sorted(line, key=lambda c: c["x0"]))[:200])

    text = "\n\f\n".join(texts)
    extraction_findings = text_layer_findings(text, config.get("expected_text", []))
    findings.extend({"page": None, **finding} for finding in extraction_findings)
    normalized_lines = [" ".join(line.split()).upper() for page in texts for line in page.splitlines()]
    for heading in config.get("headings", []):
        count = normalized_lines.count(" ".join(heading.split()).upper())
        if count != 1:
            issue("heading-occurrence", heading=heading, expected=1, actual=count)
    comparison = None
    if reference:
        before = extract_text(reference)
        equal = " ".join(before.split()) == " ".join(text.split())
        comparison = {
            "reference": str(Path(reference).resolve()),
            "normalized_text_equal": equal,
            "non_whitespace_character_counts_equal": Counter(re.sub(r"\s", "", before)) == Counter(re.sub(r"\s", "", text)),
            "diff_excerpt": list(difflib.unified_diff(before.splitlines(), text.splitlines(), fromfile="reference", tofile="current", lineterm=""))[:100]
        }
        if formatting_only and not equal:
            issue("formatting-only-text-change", explanation="Investigate content or extraction-order differences before finalization.")
    if formatting_only and not reference:
        raise ValueError("--formatting-only requires --reference")
    return {
        "path": str(path.resolve()), "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "page_count": len(pages), "pages": pages, "findings": findings,
        "comparison": comparison,
        "audit_configuration": {"profile_supplied": profile_supplied, "effective_config": config},
        "text_layer": {"status": "needs-review" if extraction_findings else "heuristic-checks-clear",
                       "finding_count": len(extraction_findings), "independent_parser_verified": False},
        "status": "needs-review" if findings else "machine-checks-clear",
        "visual_review_required": True,
        "limitations": ["No native save/editability verification", "No text-box overflow or background-object geometry verification",
                        "Mixed-family lines are heuristic; inspect intentional designs", "No semantic or ATS certification"]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--formatting-only", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        # Never allow a report to replace the input, reference, or private profile.
        protected = {p.resolve() for p in (args.pdf, args.profile, args.reference) if p}
        if args.output and args.output.resolve() in protected:
            raise ValueError("Report output must not overwrite an input file")
        profile = json.loads(args.profile.read_text()) if args.profile else None
        report = audit(args.pdf, profile, args.reference, args.formatting_only)
        report["audit_configuration"].update({
            "profile_path": str(args.profile.resolve()) if args.profile else None,
            "profile_sha256": hashlib.sha256(args.profile.read_bytes()).hexdigest() if args.profile else None,
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        })
        result = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
        if args.output:
            args.output.write_text(result)
            print(json.dumps({"report": str(args.output.resolve()), "status": report["status"], "findings": len(report["findings"])}))
        else:
            print(result, end="")
        return 2 if report["findings"] else 0
    except Exception as error:
        print(f"Audit failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
