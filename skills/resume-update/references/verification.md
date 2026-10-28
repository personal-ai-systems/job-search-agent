# Verification

## Read-Only PDF Check

Use an available Python runtime with `pdfplumber`. Locate bundled dependencies through the host's dependency tool when needed; do not install a paid service. Run:

```bash
python3 scripts/audit_resume.py /absolute/current.pdf --output /absolute/audit.json
python3 scripts/audit_resume.py /absolute/current.pdf --profile /absolute/private-profile.json --reference /absolute/before.pdf --formatting-only --output /absolute/audit.json
python3 -m unittest discover -s scripts -p 'test_audit_resume.py'
```

The checker reads the PDF only, reports its SHA256 and checks visible fonts, mixed-family lines, out-of-page glyphs, empty pages, configured section headings, suspicious extracted tokens and optional reference text. It normalizes subset font prefixes and ignores whitespace-only font differences. Allow intentional symbol fonts explicitly in the profile; do not whitelist a defective body font just to pass. Use the resolved private profile when one exists. Helvetica list markers beside Cambria body text can be intentional, not a reason to change the resume font. The report records the effective configuration and CLI profile/checker hashes; compare results only for the same PDF revision and configuration.

Exit 0 means no configured machine finding; exit 2 means review findings; exit 1 means the check failed. An output report never certifies native editability, clipped text-box overflow, semantic correctness, correct object alignment or ATS compatibility. Text extraction itself can be imperfect, especially ligatures; investigate rather than silently rewriting the resume to satisfy it.

## Extracted Text Is A Separate Gate

Visually correct glyphs can still export with incorrect Unicode mappings. Inspect extracted words, headings, dates, contact details and reading order separately from the rendered pages. Colon fragments such as `work:lows`, replacement characters and unmapped CID tokens are review signals, not automatic corrections. For known critical labels, configure `pdf_audit.expected_text` from verified native text; this catches plausible-looking substitutions too.

When extraction is suspect, compare with the native text or a verified DOCX export and a second PDF parser. Agreement between two extractors strengthens the finding but does not identify its cause. A fresh re-export alone does not prove repair. Test a native typography/export setting on a protected working copy when supported, then check both text and all-page rendering. Never patch PDF text mappings while leaving the native source inconsistent.

A DOCX with clean extracted text is a possible alternative only if accepted by the destination and its layout, reading order and content have also been checked. Do not recommend all DOCX files as ATS-safe or assume a Pages export preserves anchoring. No heuristic-clear result certifies an employer's parser.

## Visual And Native Checks

Render all pages with the PDF skill/available Poppler. Compare the full document to the selected approved visual reference at matching scale and inspect suspect areas enlarged. Check every section, not just page one. Native object alignment/box dimensions must also be checked in the editor; PDF text coordinates cannot establish the geometry of a background shape.

For photograph proportions and page-edge banners, use the explicit checks in [layout-fidelity.md](layout-fidelity.md). Neither heading presence nor a five-page/minimum-line-count check covers those defects. Keep visual results distinct from machine audit findings.

For formatting-only work, inspect both text changes and reading-order changes. For content edits, reconcile the diff with the approved factual additions. Page count is a baseline, not a universal five-page target; never shrink text or hide content to force it.

Classify geometry findings before changing them. Decorative page-edge bleed may be intentional and clipped by the page; out-of-page text is different. Unequal skill columns are not inherently wrong. Compare section rules, date alignment, spacing and column geometry with the approved reference and native objects. Record an actual inconsistency separately from an optional redesign.

Verify save/reopen in the native editor, export identity, current backup revision and the final external-Chrome display independently. Record exceptions precisely. A previous screenshot/receipt covers only the revision it actually checked.

Update an existing mapped private Drive file where appropriate. Record local and cloud identifiers, size, timestamp and hash verification level; download-back SHA256 is stronger than metadata/size. Never alter sharing to make a handoff easier. If an artifact cannot be opened externally, say handoff pending and retain the local work.
