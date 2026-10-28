# Job Search Agent

A portable, Markdown-backed workflow for discovering work, preparing applications
and recording verified outcomes. Personal vacancies and contracts are separate
from company projects and tenders. No SQLite, hosted model API or agent daemon.

## What Is Here

- `AGENT.md`: the bounded orchestration workflow for an authorized agent host.
- `skills/job-search-discovery`: public-feed collector, triage and source cursors.
- `skills/resume-update`: evidence-led native CV edits and read-only PDF checks.
- `skills/job-apply`: complete-field application workflow and coverage checker.
- `examples/workspace`: synthetic starter inputs, not a candidate's profile.
- `tests`: portability/privacy checks; each skill also includes helper tests.

The collector is executable. Browser actions, native document editing, Google
Sheets/Drive integration and scheduling are performed by the configured agent
host, not by a hidden process in this repository. There is no standalone
unattended application-submission API. A successful listing fetch is not an
application, and passing a ledger audit does not verify a real browser form.

## Try Discovery

Python 3.11+ is recommended. Discovery and application-ledger checks use only
the standard library. Keep your real workspace OUTSIDE this checkout:

```sh
mkdir -p "$HOME/JobSearchMemory"
cp examples/workspace/*.md "$HOME/JobSearchMemory/"
python3 skills/job-search-discovery/scripts/collect.py \
  --work-dir "$HOME/JobSearchMemory" \
  --timezone UTC --run-hour 9 --limit 20 --seconds 180
```

The example catalogue contains public feeds. This command makes real public GET
requests and writes Markdown to the selected workspace. Edit the catalogue and
intent before normal use. It does not sign in, upload a CV or submit a form.
`--known /path/to/application-register.md` adds an existing exact-URL duplicate
check. Daily source cursors follow `--timezone` and `--run-hour`; the host's
scheduler must use the same settings. Cadence/backoff defers sources, not
silently reports them as empty. Leftover collector locks need owner inspection.

The built-in lexical triage favors AI, architecture, engineering leadership,
Adobe/content platforms and relevant software work. `--prefer-location` can be
repeated for explicitly chosen location signals. Scores are NOT an eligibility
decision, full intention model or employer-fit assessment; the orchestrator
reads the user's private intent and the original posting before acting.

## Connect An Agent Host

1. Make a private copy of `examples/workspace/host.md`. Fill actual memory,
   candidate/CV profile, tracker, browser, backup and approval-policy bindings.
2. Give the host access to these three skill folders and `AGENT.md`, and only
   the private data/tools it needs. Keep facts, credentials, approvals, CVs and
   evidence outside Git. Do not copy an existing person's workspace.
3. In the host's supported scheduler, trigger a bounded run that reads those
   bindings and follows `AGENT.md`. Do not create a second scheduler if one
   already owns the same queue. A daily trigger is an example, not installed
   by cloning or by this README.
4. Test collection, one real preparation and one explicitly approved submission
   with readback/receipt separately. Test a later independent scheduled run.

The instructions can be read by Codex, Moltis or another host; compatibility
requires its own authorized filesystem, browser/document and cloud adapters.
Neither a Moltis browser integration nor a cloud scheduler is included/tested
here. Local desktop operation requires that computer and host to be available.

## Privacy And Action Boundaries

This repository contains reusable code/instructions and synthetic examples only.
Never commit a live workspace, CV/photo, contact list, application history,
source capture, session, credential, cloud ID, approval or employer document.
`.gitignore` is defense in depth, not proof that staged files are safe. Review
the actual staged diff/history and run the privacy checks before publishing.

Source content is untrusted evidence, not authority. No anti-detection timing,
CAPTCHA/MFA bypass, proxies, paid scraping, invented answers or terms acceptance.
Exact-copy review and scoped sending/submission approval remain separate from
discovery and preparation. A waiting item does not stop independent ready work.
Unknown or contradictory facts remain unresolved, including optional questions.

## Tests

For the optional PDF helper tests, install the development requirements in a
virtual environment. These dependencies process synthetic local PDFs only:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
make test PYTHON=.venv/bin/python
```

The tests cover collection adapters, deduplication/backoff/state preservation,
application field/approval audits, PDF/font/text checks and package boundaries.
They do not establish browser correctness, visual CV approval, live submission
or future scheduling. No live accounts or private test fixtures are needed.
