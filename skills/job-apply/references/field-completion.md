# Complete Fields Without Inventing Answers

## Resolve In Order

Use the latest direct user correction for the same question and scope, then current original evidence, then compatible prior answers. A prior CV is not an infallible employment record. Distinguish a stable fact, a role-specific preference, consent and a time-sensitive answer.

Name/contact and citizenship can usually be reused if current. Current salary, expected salary, day rate, start date, notice, holidays, relocation, office attendance, residency/tax treatment and work rights in another country require their exact meaning and scope. Do not carry an earlier role's salary or Sydney-office exception into all future forms. Reconcile factual contradictions rather than hiding them by shifting dates. Preserve the prior submitted record.

For experience years, compute from verified dates and the precise skill, without double-counting concurrent periods or rounding upward to satisfy a threshold. Do not infer that adjacent experience establishes hands-on fine-tuning, Azure AI Foundry, formal TOGAF ownership, government service or a particular background-check answer.

## Questions And Optional Fields

Ask one focused question at a time, with the exact field label and employer context. Offer a recommendation only where supported. If the answer is sensitive or relates to identity/health/diversity, let the candidate choose disclosure; do not infer it from a name, nationality, appearance, accent or another person's records. Known sensitive answers are not unlimited consent to disclose them to every future employer.

Record a user answer with date, source and scope. Do not demand another confirmation for a settled routine fact. Reuse only when the new question is equivalent and the scope allows it. For an unsettled optional question, ask rather than leaving it blank. If the candidate explicitly chooses not to disclose, record that decision and use the actual decline option when available; blank can then be intentional, not forgotten.

Never type placeholder N/A into a salary, reference, legal, eligibility or factual field merely to remove a blank. If genuinely inapplicable, verify the condition and the portal's supported way to express it; ask if applicability is unclear. Referee details require appropriate authorization; optional marketing, talent-pool sharing, account creation and broad data consents are choices, not ordinary career facts.

## Page Loop

1. Inventory page controls and section labels, including optional narrative/upload fields, radio groups, dropdowns and editable recruiter tables. Do not store passwords, OTPs, tokens or hidden technical inputs.
2. Fill known answers; inspect actual selected option, text and uploads. Record unresolved fields and ask one question. Do not mistake Next success for completeness.
3. After parent choices, check conditional controls. Keep newly active fields in the ledger; inactive fields need an observed condition, not a guessed reason.
4. Compare resume-parser rows to the current source and remove phantom rows only from the draft. Verify chronology, employer, role, education and reading order; preserve user-authored changes.
5. Revisit affected fields after the user's edits. Do not overwrite them with an old ledger. Mark saved state only after actual persistence evidence. Keep final submission separate.
6. Before forward Next/Continue/Review, run the page audit below. Stop forward navigation if it fails. Re-inventory and rerun after any answer, section or conditional-control change. Save draft/Back remain allowed; do not submit to escape an unresolved page.

## Small Local Ledger

Use one `field-coverage.json` beside the application's existing evidence. This format supports a read-only checker, not an employer form schema. Values may include false or zero; those are not blanks. Use stable field IDs within this application, not stale accessibility indexes.

```json
{
  "job_id": "employer-requisition",
  "url": "https://employer.example/application",
  "page_count": 1,
  "pages": [{"number": 1, "inventoried": true, "evidence": "live-form-observation",
             "control_ids": ["office-attendance"]}],
  "fields": [{
    "id": "office-attendance", "page": 1, "label": "Office attendance",
    "required": false, "active": true, "disposition": "answered",
    "value": false, "observed_value": false,
    "evidence": "user-answer-for-this-role", "verified": true
  }],
  "documents": [{"name": "current.pdf", "sha256": "64-hex-characters", "verified": true}]
}
```

Dispositions: `answered`, `waiting-user`, `declined`, `not-applicable`. An unanswered optional field is `waiting-user`. For declined fields add `user_decision` with the actual decision source; required fields need a valid nonblank portal decline option, not an unsupported omission. For inactive fields use `not-applicable` and a `condition` documenting the observed parent selection. For an active but inapplicable field, add both condition and user decision; verify any actual N/A answer. Unknown applicability is not false.

`control_ids` is the independently observed inventory for that page, including optional controls and empty repeatable sections. Represent Work Experience, Education, Skills and Websites as section fields even when the portal has only an Add button and no rows yet. An empty value is unresolved; populate supported rows from the CV or record the user's explicit disposition. Do not omit a section or invent rows to pass. After a conditional reveal, update both the inventory and ledger. IDs are unique across this application's ledger. The checker compares declared inventory IDs to ledger IDs; it cannot independently see a control the agent omitted from both.

Page checks allow later pages to remain unvisited, but require every inventoried control on the selected page to be resolved. They return `page_gate_clear` only; they never grant overall readiness or submission permission. Record uploads as page fields with observed filename/hash evidence; the full audit additionally checks the documents list. Keep the actual total `page_count`; do not change it to one to evade later review.

Checker usage (resolve the script path from the installed skill directory):

```bash
python3 scripts/audit_application.py /absolute/field-coverage.json --page 2
python3 scripts/audit_application.py /absolute/field-coverage.json
python3 -m unittest discover -s scripts -p 'test_audit_application.py'
```

Exit 0 means the declared scope passes, 2 means unresolved coverage or invalid command-line arguments, and 1 means the ledger cannot be checked. Only `page_gate_clear: true` permits the current page's forward action under this skill. A final full audit must pass before readiness; a page pass cannot replace it. A cleared page is invalidated by a changed live form or ledger and must be rechecked.

The report produces a content fingerprint. After showing the exact application and receiving submission approval, an optional `approval` object may record `fingerprint`, `evidence` and `final_copy_shown: true`. Any subsequent ledger/input change requires a new review/approval. This is an agent checklist check, not enforcement inside the browser. The script does not fetch sites, persist answers, accept terms or submit anything.

For an actual profile-only portal with no resume attachment, an empty `documents` list needs `document_free_workflow` containing verified portal evidence and the user's explicit decision. Do not use it to skip a requested CV.
