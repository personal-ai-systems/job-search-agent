---
name: job-search-agent
description: Run a bounded job-search workflow across discovery, CV preparation and applications using the host's private intent, memory and existing tracker. Resume past blockers without duplicate applications; does not create a scheduler or grant submission authority.
metadata:
  version: "0.1.0"
---

# Job Search Agent

This is the orchestration entrypoint, not another model or a background worker.
Read the repository's [AGENT.md](../../AGENT.md) before a run. Resolve the current
host's private binding from its workspace instructions; never infer a person's
profile, tracker, scheduler, source catalogue or permissions from the examples.

Use the installed job-search-discovery, resume-update and job-apply workflows.
The host binding identifies the actual selected versions and any reviewed
host-specific adapters. Read those sources rather than assuming a repository
install overrides a personal skill of the same name. Preserve deliberate host
overrides; report a genuine conflict instead of silently replacing user edits.

Check live ownership and receipts before work. Continue ready independent items
when one waits. Apply current exact-copy review, scoped action permissions and
human-only gates. No second schedule, new model, account permission or paid
service is installed by invoking this skill.

For a read-only installation test, read the bindings and current checkpoint,
identify the three selected skill locations, one next action, current blockers
and scheduler owner. Do not fetch feeds, change the queue, edit a CV, message
an employer or submit anything merely to prove the entrypoint loads.
