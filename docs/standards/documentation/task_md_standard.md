---
id: "std.documentation.task_md"
title: "Historical Task Markdown Standard"
summary: "This standard defines the retained-history rules for legacy task Markdown stored under docs/planning/tasks/ after the hard cutover to live plan task state."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "task_md"
owner: "repository_maintainer"
updated_at: "2026-03-18T14:00:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
aliases:
  - "historical task record standard"
  - "task markdown retention standard"
---

# Historical Task Markdown Standard

## Summary
This standard defines the retained-history rules for legacy task Markdown under `docs/planning/tasks/`. New live tasks no longer use this document family.

## Purpose
- Preserve historical task Markdown long enough for retention, audit, and purge workflows.
- Prevent retained docs-backed task files from being mistaken for live operational authority.
- Keep the historical corpus readable without encouraging new live work to re-enter the retired model.

## Scope
- Applies to retained task Markdown stored under `docs/planning/tasks/**`.
- Covers retained-file readability, archive expectations, and the boundary between historical task Markdown and live plan task state.
- Does not define live task creation, live task indexing, or GitHub sync behavior for the active operational model.

## Use When
- Reviewing, preserving, or purging retained pre-cutover task Markdown.
- Clarifying that a task document under `docs/planning/tasks/**` is historical and not the live task source of truth.
- Repairing archival hygiene for retained historical task documents.

## Related Standards and Sources
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md): defines the live task authority model that replaced docs-backed task Markdown.
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md): defines the live machine-readable task index.
- [planning_retention_and_purge_standard.md](/docs/standards/governance/planning_retention_and_purge_standard.md): defines when retained historical task packages can later be removed.
- [task_template.md](/docs/templates/task_template.md): retained historical template surface that should not be used for new live task execution work.
- [README.md](/docs/planning/tasks/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Do not create new live tasks under `docs/planning/tasks/**`.
- Use `watchtower-core task create|update|transition` and initiative-local `plan/**/.wt/tasks/**/task.json` for all new live task execution work.
- Treat retained task Markdown as historical evidence only.
- Preserve stable IDs, timestamps, and original archival context when editing retained historical task files for hygiene.
- Keep historical task prose readable and execution-oriented; do not rewrite retained history just to mimic the live JSON model.
- Do not hand-maintain `docs/planning/tasks/task_tracking.md` as if it were sourced from retained Markdown.
- When a retained task file needs durable policy, guidance, or closeout meaning, promote that meaning into current authoritative standards, plans, or live closeout artifacts instead of relying on the retained task file.

## Structure or Data Model
- governed front matter
- title
- execution-oriented body content
- any retained historical sections needed to understand the archived task in context

### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Retained historical task | `docs/planning/tasks/**` | Historical only. No new live authority. |
| Historical closed task archive | `docs/planning/tasks/closed/archive/<yyyy>/<mm>/<dd>/` | Retained until an explicit purge or retention action removes the package. |
| Task tracker | `docs/planning/tasks/task_tracking.md` | Derived from live plan task state, not from retained Markdown. |

## Operationalization
- `Modes`: `documentation`
- `Operational Surfaces`: `docs/planning/tasks/`; `docs/planning/tasks/closed/archive/`; `docs/templates/task_template.md`

## Validation
- Retained historical task Markdown should remain readable and internally coherent.
- Historical task Markdown should not be advertised as the live source of truth by current standards, workflow docs, or command docs.
- No new live task should be authored under `docs/planning/tasks/**`.

## Change Control
- Update this standard when the repository changes retention handling for the docs-backed historical task corpus.
- Update the task tracking standard, task template, and planning-retention guidance in the same change set when retained task Markdown expectations change materially.

## References
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md)
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md)
- [planning_retention_and_purge_standard.md](/docs/standards/governance/planning_retention_and_purge_standard.md)
- [task_template.md](/docs/templates/task_template.md)
- [README.md](/docs/planning/tasks/README.md)

## Updated At
- `2026-03-18T14:00:00Z`
