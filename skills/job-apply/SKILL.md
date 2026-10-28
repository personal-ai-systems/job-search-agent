---
name: job-apply
description: "Prepare and verify a job application from a vacancy or employer-portal link, selecting the supported CV, completing every applicable field and asking about missing answers, including optional fields. Track exact attachments, approvals and receipts; not bulk outreach, assessments or an unattended scheduler."
---

# Job Apply

## Mandatory Execution Contract

Before filling or resuming an employer form, load THIS skill and [field-completion.md](references/field-completion.md), resolve the private candidate profile and current resume profile, and read the selected CV. Loading `resume-update` alone does not load this workflow. Repeat this recovery after context compaction, switching applications, or receiving a correction; an earlier read in another task is insufficient.

Every applicable field, including optional fields and empty work-experience, education, skills and website sections, needs a supported answer or an explicit user disposition. "No asterisk", "the PDF already contains it", "avoid duplication" and "the portal accepted Next" are not valid reasons to omit it. Do not infer a start date/notice period from cessation of employment. Search the scoped profile and evidence before claiming information is missing or asking again.

Before EACH forward Next/Continue/Review action, update the live page inventory and field ledger, run `python3 scripts/audit_application.py /absolute/field-coverage.json --page N`, and require `page_gate_clear: true` for that actual page. A nonzero exit, missing checker, unlisted section or `waiting-user` field blocks that forward action. Ask one unresolved question and wait; independent preparation may continue. Do not fabricate a pass, substitute portal validation or remove an unresolved field from the inventory. Back/Save draft/Cancel remain available to preserve or repair work. A user-directed skip is recorded as the applicable explicit disposition, never silently inferred.

Before final review run the full audit without `--page`; before submission require full coverage plus the applicable exact-copy approval. Page approval is not submission approval. This contract binds every agent using the skill, including a resumed/delegated worker, but a Markdown skill and an optional checker do not technically intercept browser actions. Do not claim host-level enforcement unless the host actually blocks them.

The active assistant executes this workflow. A vacancy URL is sufficient to start when the candidate's private profile already exists; a second application URL or requested CV track is useful but not mandatory. Do not restart a career interview, require a new agent or create a paid/background service. Skill installation alone is not autonomous execution.

## Pre-Flight Gate

Run this before the first question, on every application, even when the form looks familiar. Skipping it is the most common way this skill fails in practice.

1. Read `structured/projects/work/job-apply-profile.json` and extract every `knownFacts` entry into a working list: key, value, scope, recheck condition.
2. Read `doNotGeneralize` as the list of facts explicitly NOT available for reuse.
3. Resolve the current CV locator from `resumeProfile`.
4. State the resolved list to the candidate in the current chat as short plain lines before filling anything: which facts come from the profile, which are role-scoped history that must be re-asked, and which are genuinely unknown.
5. Only then ask questions, and only about what remains.

Hard rules:

- Never ask a question that a `knownFacts` entry already answers within its scope. Re-asking a settled fact wastes the candidate's time and is an execution defect, not diligence. Australian citizenship is a standing fact; it is not re-asked per employer.
- A `recheck` condition means re-verify against the named evidence, not re-interrogate the candidate.
- A fact listed in `doNotGeneralize` (salary history, notice period, office attendance, redundancy eligibility) must be asked with its exact scope for this role. Do not present it as unknown policy, and do not carry an old number forward.
- If the profile contradicts the live form or a new candidate statement, say so plainly and let the candidate decide. Never silently pick one side.

## Four-Skill Chain

Getting from "nothing" to "applied" is four skills working together, not one. Each has a different authority and the boundary between them is the point:

- `job-search-discovery` finds and ranks vacancies against the private interest model and work rights. It produces leads only; it never touches an employer form. Run it first, or on a schedule.
- The private Vault profile (`job-apply-profile.json`, `job-search-interest.json`, `job-sources.json` plus `resume-update-profile.json`) holds standing facts, preferences and locators. It is the only place personal data lives; the portable skills stay free of it so they can be shared.
- `resume-update` selects, and only when authorized edits, the native CV for this role.
- This skill drives the employer portal field by field and gates submission.

If any of the four is missing or unreadable, stop and report the specific gap. Do not substitute an invented fact, a generic CV or a guessed portal behaviour. A lead from discovery is not an instruction to apply: it is a candidate awaiting the user's decision.

## Recover And Check

1. Read the current host's personal instructions and configured private candidate profile (`structured/projects/work/job-apply-profile.json` on a Vault host). If a profile is configured, reading it is mandatory; on another host use that candidate's supplied evidence. Resolve only relevant facts, current CV locators, application checkpoint and tracker; keep personal data outside this portable skill.
2. Match employer, role and requisition ID across the supplied advert and actual portal. Read the original employer posting, attachments, submission requirements and candidate AI-use rules. A job board's Apply click is not submission. If an assessment starts, stop assistance prohibited by its rules and hand it to the candidate.
3. Check the application log, portal state, relevant receipt and any active owner. Continue the existing application rather than creating another. Already-applied is not a new submission; record unknown historical attachment/date honestly. Keep user-edited browser fields and files; do not reload a live form unnecessarily.
4. Discover actual available tools and use the configured external signed-in Chrome. Respect account restrictions; no human-like evasion, artificial traffic camouflage, alternate blocked surface or hidden API bypass. Login, passwords, MFA, signatures and approvals follow current host rules.

## Match Documents And Facts

Choose the current verified CV for the actual role, not simply the newest file. Use `resume-update` for authorized tailoring or formatting; preserve native source, user edits and historical submitted bytes. If that skill is absent, preserve the same source/save/reopen/render/export gates and state the capability limit. Read [evidence-and-documents.md](references/evidence-and-documents.md).

Record the exact selected path, hash, filename and upload readback. Prepare a targeted cover letter and any requested tables/selection responses within the employer's limits. Do not send a generic paragraph in place of an unfilled recruiter table or hide missing evidence with keyword claims. A parsed resume is a draft: review and correct each generated employment/education entry, dates and duplicate rows.

## Every Field Must Be Addressed

Read [field-completion.md](references/field-completion.md) before filling forms. On every page inventory all visible relevant controls, required AND optional. After an answer, rescan newly revealed conditional fields. Exclude hidden technical inputs, not inconvenient questions.

- Fill supported facts and verify the actual saved/selected values. A visible string, parser suggestion or click does not prove a dropdown choice committed.
- Search existing evidence before asking. If an applicable answer is unknown, ambiguous, conflicting or approval-sensitive, ask one focused question in the current chat and wait. Use the host question tool when available; otherwise ask normally. Do not silently choose No, Not specified, Prefer not to say, blank, N/A or zero.
- Optional means the employer permits omission, not that the user authorized it. Ask whether to answer or decline when needed. A user-approved decline may use the portal's actual decline option or a documented blank when none exists. Do not force sensitive disclosure, manufacture a response or re-ask an already scoped decision.
- Continue independent preparation while waiting, but do not mark the application ready while any applicable field lacks an answer or explicit user disposition. If the user pauses/skips, retain that unresolved state; do not submit merely because the portal permits Next.
- Keep a small per-application field ledger in existing task assets: label/page, applicability, intended answer, evidence/scope, observed value and disposition. Retain exact user corrections. This is a checklist, not a replacement candidate database.

### Blank Is A Disposition, Not An Absence

Every active control on the page ends in exactly one state: `answered`, `waiting-user`, `declined` or `not-applicable`. A blank with no recorded disposition is an unfinished field, not a decision.

This applies hardest to parser-generated sections: work experience, education, skills, websites. A portal labels them optional because it permits omission; that is not authorization to omit. Leaving them empty discards the CV's substance and produces an application weaker than the PDF alone. Fill them from the current CV and resume profile, then have the candidate confirm the parsed rows and dates.

Before pressing Next or Continue on any page, report its audited answered/declined/not-applicable counts and any intentional blanks with their actual user decisions. A page with all optional fields answered can have zero blanks. Compare the ledger's `control_ids` with the live controls AND section headings; an empty repeatable section is still an inventory item, not an absent field.

Run `scripts/audit_application.py` against the ledger before final review; format is in [field-completion.md](references/field-completion.md). It catches declared omissions and stale approval fingerprints, not undiscovered fields or browser truth. Compare the ledger with the live form as well. Do not claim completeness from an empty or partial ledger.

## Returning To A Completed Page

When a page was finished too early, repair it rather than submitting around the gap.

1. Re-inventory from the live form, not from the prior ledger.
2. Keep what the candidate typed himself; do not reload or overwrite a live form.
3. Re-verify downstream pages: saved answers can re-render or clear conditional fields.
4. Mark repaired fields with a fresh observation and withdraw any earlier completeness claim.

## Growing A Repeating Section

Parser-backed sections (work experience, education) can silently drop rows when a saved list is edited again. The live form showing a row is not proof: only the saved review shows what the employer will receive.

Observed on a Workday tenant: a list saved once and verified persisted correctly. Appending rows to that saved list and saving again destroyed previously saved entries three times in a row (10 rows saved as 8, then as 2, then 3 rows saved as 1). Incremental growth is therefore unsafe in both directions.

Safe procedure, verified to hold ten work-experience rows:

1. Delete the existing rows and rebuild the whole list inside one editing pass.
2. Add every row first, then fill each one, keeping all rows mounted while filling.
3. Verify every row in the live form — title, company, both dates, description — before saving.
4. Save once, then read the saved review and confirm the row count and each company name.
5. If the saved count is lower than the filled count, stop and report. Do not re-save the same list; rebuild again from scratch.

Record any observed loss on the application record so a later run does not repeat it.

## Review, Submit And Verify

Read [submission-and-recovery.md](references/submission-and-recovery.md). Verify every page and attachment, check completeness and display the exact CV/letter/final answers in external Chrome. Explain gaps and leave reviewable work. Obtain the current exact-copy submission approval required by host/user guidance. Acceptance of a privacy notice is NOT approval to submit; a later content change invalidates earlier exact-copy approval. The user creating this skill does not approve any pending application.

After specific approval, submit once, inspect actual success/receipt and check ambiguous outcomes before retrying. Update the existing log and native Job Search spreadsheet with the correct track and valid status; read back the changed row. Preserve evidence and current private backup. Close only completed application/used-source tabs after receipt is saved, retaining unfinished forms and tracker; retain review tabs when requested. Never call attempted, validation-only or prepared work Applied.

Persist between pages and user questions: actual stage, exact files, field coverage, approved answers/consents, remaining question, receipt and next action. End with a short factual result. No new timer, other-agent message, subscription or job search campaign is created by invoking this skill.
