#!/usr/bin/env python3
"""Read-only coverage check for an agent's per-application ledger, not a browser gate."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def blank(value):
    return value is None or (isinstance(value, str) and not value.strip()) or value == [] or value == {}


def fingerprint(data):
    snapshot = {key: value for key, value in data.items() if key != "approval"}
    encoded = json.dumps(snapshot, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def audit(data, page_number=None):
    if not isinstance(data, dict):
        raise ValueError("Ledger must be a JSON object")
    if page_number is not None and (type(page_number) is not int or page_number < 1):
        raise ValueError("Page number must be a positive integer")
    page_check = page_number is not None
    findings = []

    def flag(where, message):
        findings.append({"where": where, "message": message})

    if blank(data.get("job_id")) or not re.match(r"^https?://", str(data.get("url", ""))):
        flag("application", "Identify the actual requisition and source URL")
    count = data.get("page_count")
    pages = data.get("pages", [])
    if type(count) is not int or count < 1:
        flag("pages", "Declare the actual positive page count")
        count = 0
    if not isinstance(pages, list) or any(not isinstance(page, dict) for page in pages):
        raise ValueError("pages must be a list of objects")
    if page_check:
        pages = [page for page in pages if page.get("number") == page_number]
        if len(pages) != 1 or page_number > count:
            flag("pages", "The selected page must exist exactly once within the actual page count")
    numbers = [page.get("number") for page in pages]
    if not page_check and (any(type(number) is not int for number in numbers) or sorted(numbers) != list(range(1, count + 1))):
        flag("pages", "Inventory every page exactly once")
    for page in pages:
        if page.get("inventoried") is not True or blank(page.get("evidence")):
            flag(f"page:{page.get('number')}", "Live field inventory evidence missing")

    fields = data.get("fields", [])
    if not isinstance(fields, list) or any(not isinstance(field, dict) for field in fields):
        raise ValueError("fields must be a list of objects")
    if page_check:
        fields = [field for field in fields if field.get("page") == page_number]
    for page in pages:
        controls = page.get("control_ids")
        where = f"page:{page.get('number')}"
        if (not isinstance(controls, list) or not controls
                or any(not isinstance(key, str) or blank(key) for key in controls)):
            flag(where, "List every observed control and empty repeatable section in control_ids")
            continue
        if len(set(controls)) != len(controls):
            flag(where, "Observed control IDs must be unique")
        recorded = {field.get("id") for field in fields if field.get("page") == page.get("number")
                    and isinstance(field.get("id"), str)}
        missing, extra = set(controls) - recorded, recorded - set(controls)
        if missing:
            flag(where, "Observed controls/sections missing from ledger: " + ", ".join(sorted(missing)))
        if extra:
            flag(where, "Ledger fields absent from live inventory: " + ", ".join(sorted(extra)))
    if not fields:
        flag("fields", "Empty ledger cannot establish field coverage")
    seen = set()
    for field in fields:
        key = field.get("id")
        where = f"field:{key}"
        if not isinstance(key, str) or blank(key) or key in seen:
            flag(where, "Field ID missing or duplicated")
        else:
            seen.add(key)
        if blank(field.get("label")) or field.get("page") not in numbers:
            flag(where, "Field needs its label and inventoried page")
        if type(field.get("required")) is not bool or type(field.get("active")) is not bool:
            flag(where, "Required/applicability status must be explicitly observed")
        disposition = field.get("disposition")
        if disposition not in {"answered", "declined", "not-applicable"}:
            flag(where, "Ask the unresolved question, even when optional")
            continue
        if field.get("verified") is not True or blank(field.get("evidence")):
            flag(where, "Evidence and actual form readback required")
        if disposition == "answered":
            if field.get("active") is not True or blank(field.get("value")):
                flag(where, "Answer must apply and must not be a placeholder blank")
        elif disposition == "declined":
            if blank(field.get("user_decision")):
                flag(where, "Optional omission/decline needs the user's explicit decision")
            if field.get("required") is True and blank(field.get("value")):
                flag(where, "Required field needs a valid portal answer, not a blank decline")
        elif disposition == "not-applicable":
            if blank(field.get("condition")):
                flag(where, "Record the observed inapplicability condition")
            if field.get("active") is True and blank(field.get("user_decision")):
                flag(where, "Visible inapplicable field needs an explicit disposition")
            if field.get("active") is True and field.get("required") is True and blank(field.get("value")):
                flag(where, "Required visible field cannot remain blank")
        if "observed_value" not in field or field.get("observed_value") != field.get("value"):
            flag(where, "Intended and observed values differ or readback is missing")

    documents = data.get("documents", [])
    if not isinstance(documents, list) or any(not isinstance(doc, dict) for doc in documents):
        raise ValueError("documents must be a list of objects")
    if not documents and not page_check:
        no_docs = data.get("document_free_workflow", {})
        if not isinstance(no_docs, dict) or no_docs.get("verified") is not True or blank(no_docs.get("evidence")) or blank(no_docs.get("user_decision")):
            flag("documents", "Record the selected resume or an explicitly reviewed document-free workflow")
    for doc in ([] if page_check else documents):
        if blank(doc.get("name")) or not re.fullmatch(r"[a-fA-F0-9]{64}", str(doc.get("sha256", ""))):
            flag("documents", "Exact selected filename/hash missing")
        if doc.get("verified") is not True:
            flag("documents", "Actual attachment readback missing")

    current = fingerprint(data)
    approval = data.get("approval", {})
    if not isinstance(approval, dict):
        raise ValueError("approval must be an object")
    approved = approval.get("fingerprint") == current and approval.get("final_copy_shown") is True and not blank(approval.get("evidence"))
    return {
        "status": "needs-attention" if findings else ("page-coverage-clear" if page_check else "declared-coverage-clear"),
        "scope": "page" if page_check else "application",
        "page": page_number,
        "page_gate_clear": page_check and not findings,
        "fingerprint": current,
        "findings": findings,
        "ready_for_review": not page_check and not findings,
        "approval_matches": not page_check and approved,
        "submission_gate_clear": not page_check and not findings and approved,
        "limitation": "Checks the supplied ledger only; does not discover controls, verify browser truth, accept terms or submit. Host approval rules still apply.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", help="Path to field-coverage.json")
    parser.add_argument("--page", type=int, help="Check this page before forward navigation; not a submission check")
    args = parser.parse_args()
    try:
        result = audit(json.loads(Path(args.ledger).read_text()), page_number=args.page)
    except (OSError, ValueError, TypeError) as exc:
        print(f"Check failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready_for_review"] or result["page_gate_clear"] else 2


if __name__ == "__main__":
    sys.exit(main())
