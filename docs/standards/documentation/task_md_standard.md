---
id: "std.documentation.task_md"
title: "Task Document Standard"
summary: "This standard defines the role, structure, placement, and quality expectations for local-first task records under docs/planning/tasks/."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "task_md"
owner: "repository_maintainer"
updated_at: "2026-03-15T15:30:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/open/"
  - "docs/planning/tasks/closed/"
aliases:
  - "task record standard"
  - "task markdown standard"
---

# Task Document Standard

## Summary
This standard defines the role, structure, placement, and quality expectations for local-first task records under `docs/planning/tasks/`.

## Purpose
Keep local tasks readable for humans, structured for agents, and modular enough that multiple engineers can update different tasks without colliding in one shared tracker file.

## Scope
- Applies to task record documents stored under `docs/planning/tasks/open/` and `docs/planning/tasks/closed/`.
- Covers placement, required structure, front matter expectations, and the boundary between task records and derived tracking surfaces.
- Does not define the task-index artifact schema or GitHub sync behavior in full.

## Use When
- Creating a new local task record.
- Updating a task's execution status, owner, blockers, or linked planning surfaces.
- Reviewing whether a document under `docs/planning/tasks/` is shaped like a governed task record.

## Related Standards and Sources
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [github_task_sync_standard.md](/docs/standards/governance/github_task_sync_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [planning_retention_and_purge_standard.md](/docs/standards/governance/planning_retention_and_purge_standard.md): companion standard that constrains when retained closed task documents can later be removed with the full trace package.
- [front_matter_standard.md](/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [compact_document_authoring_standard.md](/docs/standards/documentation/compact_document_authoring_standard.md): companion standard that constrains this standard's default section density and compact-authoring expectations.
- [task_template.md](/docs/templates/task_template.md): authoring scaffold that should stay aligned with this standard.
- [README.md](/docs/planning/tasks/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Store one task per file.
- Use a stable `task_id` in front matter instead of relying on the filename for identity.
- Keep execution status in `task_status`, not in the document `status` field.
- Keep active or non-terminal tasks in `open/`.
- Keep `done` and `cancelled` tasks in dated archive paths beneath `closed/archive/` while the parent trace remains retained.
- Use front matter as the primary structured metadata surface for tasks.
- Keep GitHub sync metadata in front matter when a task has been published externally.
- Keep the body focused on why the task exists, what is in scope, what counts as done, and which planning or implementation surfaces it touches.
- Keep task prose short and execution-oriented.
- Treat archived task documents as retained execution history, not as the enduring home of active policy or operational guidance.
- Use real repository paths and stable IDs in front matter or optional links rather than informal notes.
- `Context` and `Links` are optional when the title, summary, front matter, and scope already make the task legible.
- Do not hand-maintain `task_tracking.md` as if it were the source of truth for task state.

## Structure or Data Model
- governed front matter
- Title
- `Summary`
- `Scope`
- `Done When`
- optional `Context`
- optional `Links`
- optional `Notes`
- optional `Updated At`

### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Active or non-terminal task | `docs/planning/tasks/open/<task_name>.md` | Use stable snake_case filenames derived from the task topic. |
| Closed task | `docs/planning/tasks/closed/archive/<yyyy>/<mm>/<dd>/<task_name>.md` | Default retained home while the parent trace remains in the planning corpus; preserve the dated archive directory on later closed-task edits until an explicit trace purge removes the package. |
| Task tracker | `docs/planning/tasks/task_tracking.md` | Generated human-readable task board. |

## Operationalization
- `Modes`: `documentation`
- `Operational Surfaces`: `docs/planning/tasks/open/`; `docs/planning/tasks/closed/`; `docs/templates/task_template.md`; `docs/planning/tasks/`

## Validation
- The task should validate against the published task front-matter profile.
- The H1 title should align with the front matter title.
- The task should make ownership, execution status, and completion criteria easy to find.
- Optional sections should be omitted when they do not add non-derivable information.
- The task should not mix multiple unrelated work items into one file.
- The task location should match the task-status class defined by the governance standard.

## Change Control
- Update this standard when the repository changes task-document shape, placement, or required sections.
- Update the task template, task front-matter schema, and task-index surfaces in the same change set when task-document expectations change materially.

## References
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md)
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md)
- [github_task_sync_standard.md](/docs/standards/governance/github_task_sync_standard.md)
- [planning_retention_and_purge_standard.md](/docs/standards/governance/planning_retention_and_purge_standard.md)
- [task_template.md](/docs/templates/task_template.md)
- [README.md](/docs/planning/tasks/README.md)

## Updated At
- `2026-03-15T15:30:00Z`
