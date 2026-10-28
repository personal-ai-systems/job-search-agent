# Moltis Connection

Moltis can install multiple SKILL.md folders from this repository. The agent
entrypoint is `job-search-agent`; its three specialist workflows remain separate.
The root AGENT.md is an operating document, not automatically a named skill.

## Install And Review

```sh
moltis skills add personal-ai-systems/job-search-agent
moltis skills list
moltis skills info job-search-agent
```

Use the actual installed CLI help and Skills UI for your Moltis version. Registry
installation, review/trust and enabling are separate states; do not edit trust
metadata by hand or disable protections to make installation appear successful.
For a private repository, a loader without GitHub authentication can return404;
authenticated downloading is separate from installation. Never paste a token
into a skill to bypass that boundary.

Before enabling, inspect provenance, pinned commit and all linked code. Existing
Personal/Project skills with the same names can take priority over Registry
copies. Inspect the actual selected path and preserve intentional host bindings;
do not delete or overwrite working skills blindly.

## Bind Private Memory

Create a private host binding outside Git, using examples/workspace/host.md as
a starting point. In the host's workspace instructions route job-search requests
to job-search-agent and this binding. Supply real intent/profile/CV locators,
source catalogue, existing tracker, current checkpoint, browser/document/cloud
capabilities and approval policy. Do not commit these values to this repository.

The public collector can be used directly, or a deliberately retained reviewed
host adapter can provide the same workflow. If using the public collector,
explicitly set timezone/hour/location signals to match the private host policy.

No Codex-only browser calls are Moltis APIs. Discover the host's actual supported
tools. A visible skill does not grant browser, native-editor or cloud access.
Do not replace a user's configured provider, voice settings or runtime limits.

## Acceptance

Ask the current Moltis conversation for a read-only activation test: load
job-search-agent, its root AGENT.md, private host binding and current checkpoint;
identify the selected specialist paths, next action, blockers and current
scheduler owner. Do not change career files or send applications during the test.
Confirm actual tool reads/output, not just an assistant claim of readiness.

Continue an approved bounded work item only after this read-only check. Installing
the entrypoint does not start a daily loop. Reuse the existing scheduler/owner,
or explicitly migrate it after verification; never run two hosts on the same
application queue. An independent scheduled run and an actual ATS receipt are
separate acceptance tests.
