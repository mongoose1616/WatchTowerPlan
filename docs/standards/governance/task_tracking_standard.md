---
id: "std.governance.task_tracking"
title: "Task Tracking Standard"
summary: "This standard defines the repository's local-first task tracking model so multiple engineers or agents can coordinate active work without turning planning trackers into a task board."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "task_tracking"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:19:08Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/tasks/task_index.v1.json"
aliases:
  - "local task tracking"
  - "task board"
  - "work tracking"
---

# Task Tracking Standard

## Summary
This standard defines the repository's local-first task tracking model so multiple engineers or agents can coordinate active work without turning planning trackers into a task board.

## Purpose
- Give the repository one durable local system for active task coordination.
- Reduce merge conflicts by treating one task record as one file instead of maintaining one shared checklist.
- Keep local tasks structured enough that they can later sync to GitHub issues or project items.

## Scope
- Applies to local task records under `docs/planning/tasks/`.
- Applies to the human-readable task tracker and the machine-readable task index derived from those task records.
- Covers task execution status, task placement, local source-of-truth rules, and future GitHub foreign-key fields.
- Does not replace PRDs, design docs, decision records, or the broader traceability model.

## Use When
- Capturing engineer-sized work items that need active ownership and status tracking.
- Coordinating concurrent work across multiple engineers or agents.
- Reviewing whether a change should create or update a tracked task rather than only touching a planning document.

## Related Standards and Sources
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_handling_threshold_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_handling_threshold_standard.md): companion standard that defines when work must create, update, transition, or explicitly decline a durable task record.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/docs/planning/tasks/README.md): family entrypoint and inventory surface this standard should stay aligned with.
## Guidance
- Treat local task records as the authoritative local execution surface.
- Store one task per Markdown file.
- Keep active or non-terminal tasks under `docs/planning/tasks/open/`.
- Keep terminal tasks under `docs/planning/tasks/closed/`.
- Use `task_status` for task execution state and keep document `status` reserved for artifact lifecycle.
- Use only these task execution states:
  - `backlog`
  - `ready`
  - `in_progress`
  - `blocked`
  - `in_review`
  - `done`
  - `cancelled`
- Use only these task priority values:
  - `critical`
  - `high`
  - `medium`
  - `low`
- Use only these task kinds unless a later standard extends the set:
  - `feature`
  - `bug`
  - `chore`
  - `documentation`
  - `governance`
  - `research`
- Prefer linking tasks to durable planning artifacts with `trace_id` and `related_ids` when those sources exist.
- Use `blocked_by` and `depends_on` to express task-to-task coordination explicitly instead of burying blockers in prose.
- Treat `docs/planning/tasks/task_tracking.md` as a derived human summary, not as the task source of truth.
- Keep `task_tracking.md` scan-first and compact. Prefer short zero-state text and high-signal columns over placeholder rows or repeated footer prose.
- Treat `core/control_plane/indexes/tasks/task_index.v1.json` as the machine-readable lookup surface derived from task records.
- Keep optional GitHub foreign keys in task front matter when a later sync surface needs them:
  - `github_repository`
  - `github_issue_number`
  - `github_issue_node_id`
  - `github_project_owner`
  - `github_project_owner_type`
  - `github_project_number`
  - `github_project_item_id`
  - `github_synced_at`
- Do not require GitHub metadata for local tasks before sync exists.
- Keep GitHub sync push-only in the first phase. Local task records stay authoritative.

## Structure or Data Model
### Source-of-truth layers
| Layer | Role |
|---|---|
| Task Markdown record | Authoritative local task record |
| `task_tracking.md` | Generated human-readable summary board |
| `task_index.v1.json` | Generated machine-readable query surface |

### Directory placement rules
| Task State Class | Canonical Location |
|---|---|
| Non-terminal task | `docs/planning/tasks/open/` |
| Terminal task | `docs/planning/tasks/closed/` |
| Human tracker | `docs/planning/tasks/task_tracking.md` |

## Process or Workflow
1. Create one task file per engineer-sized work item.
2. Evaluate the task-handling threshold before leaving the task outcome implicit.
3. Put the task in `open/` or `closed/` based on its execution status class.
4. Keep the task front matter current when the task owner, task status, blockers, or linked planning surfaces change.
5. Rebuild the human tracker and task index in the same change set after task changes.
6. Rebuild the traceability index in the same change set when traced tasks are added, removed, or materially retargeted.

## Examples
- A new implementation slice with one owner and one bounded outcome should be one task file under `open/`.
- A closed task that is complete should move to `closed/` and keep its `task_status` as `done`.
- A task that belongs to a traced initiative should carry the matching `trace_id` and related design or PRD IDs.
- A future GitHub-synced task can add GitHub issue metadata without changing its stable local `task_id`.

## Validation
- Task records should validate against the published task front-matter profile.
- `task_tracking.md` and `task_index.v1.json` should agree with the current task-record corpus.
- A task in `open/` should not use terminal task statuses.
- A task in `closed/` should use only `done` or `cancelled`.
- Task IDs referenced by `blocked_by` or `depends_on` should exist in the current task corpus.

## Change Control
- Update this standard when the repository changes task-state vocabulary, placement rules, or the local-versus-generated task authority model.
- Update the task document standard, task template, task index schema, and companion sync logic in the same change set when task tracking changes structurally.

## References
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [task_handling_threshold_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_handling_threshold_standard.md)
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md)
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md)
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/tasks/README.md)

## Updated At
- `2026-03-10T16:19:08Z`
