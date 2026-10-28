# Repository Instructions

This repository owns reusable agent instructions, helpers and synthetic tests.
Private candidate/company state belongs to an external workspace, not this Git
tree. Never copy a live Vault, cloud identifiers, CVs, receipts, credentials or
host-specific private instructions into source, fixtures or commit history.

Before changes, read README.md and the affected skill/reference. Preserve
evidence/approval boundaries and native document layout requirements. Keep the
workflow model-independent; do not add a database, paid service or always-on
model as a prerequisite. Do not confuse the collector with the host executor.

Use examples as documentation, not trusted facts. Keep network calls out of
tests; mock feed responses and generate temporary synthetic PDFs. Run `make
test` with the development requirements available. Inspect the staged files and
diff before commit/push; tests and .gitignore do not prove absence of secrets.

Do not change a user's installed skills, private workspace, browser permissions
or scheduler as a side effect of repository maintenance. Installation/deployment
is separate, explicit work. Record tested host capabilities without claiming
cross-host activation from a file copy or clone.
