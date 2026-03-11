---
id: "std.data_contracts.task_index"
title: "Task Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable task indexes stored under core/control_plane/indexes/tasks/."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "task_index"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/indexes/tasks/task_index.v1.json"
aliases:
  - "task index"
  - "task board index"
---

# Task Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable task indexes stored under `core/control_plane/indexes/tasks/`.

## Purpose
Provide a compact machine-readable lookup surface for local tasks so Python tooling, agents, and future sync workflows can query task state without parsing every Markdown task file directly.

## Scope
- Applies to machine-readable task index artifacts stored under `core/control_plane/indexes/tasks/`.
- Covers placement, entry shape, derived-source rules, and the relationship between task records, the human tracker, and the task index.
- Does not replace the task Markdown records as the local task source of truth.

## Use When
- Adding or updating local task records.
- Rebuilding task lookup data after task changes.
- Reviewing whether task metadata belongs in the task index or only in task prose.

## Related Standards and Sources
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/tasks/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Model task lookup as an index, not as a registry.
- Keep the authoritative task content in the task Markdown records under `docs/planning/tasks/`.
- Keep the task tracker and task index derived from those records.
- Store published task indexes under `core/control_plane/indexes/tasks/`.
- Use JSON for the published task index artifact.
- Every task-index entry must point to an existing task document.
- Keep optional GitHub identifiers as foreign-key metadata only; do not make them the local task identity.
- Keep task execution state in `task_status` and artifact lifecycle state in `status`.
- Update the task index in the same change set whenever task records change materially.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the task-index artifact family. |
| `id` | Required | Stable identifier for the task index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of task records. |

### Task entry fields
| Field | Requirement | Notes |
|---|---|---|
| `task_id` | Required | Stable machine-usable task identifier. |
| `title` | Required | Stable task title. |
| `summary` | Required | Short execution summary. |
| `status` | Required | Task-record lifecycle state, usually `active`. |
| `task_status` | Required | Current execution state such as `backlog` or `in_progress`. |
| `task_kind` | Required | Bounded task category such as `feature` or `bug`. |
| `priority` | Required | Task priority. |
| `owner` | Required | Responsible maintainer or role. |
| `doc_path` | Required | Repository-relative task document path. |
| `updated_at` | Required | Last meaningful task update in UTC. |
| `trace_id` | Optional | Shared traceability identifier when the task participates in a traced initiative. |
| `blocked_by` | Optional | Task IDs that block the current task. |
| `depends_on` | Optional | Task IDs the current task depends on. |
| `related_ids` | Optional | Stable IDs for PRDs, decisions, designs, plans, or other governed surfaces. |
| `applies_to` | Optional | Paths or concepts the task touches directly. |
| `github_repository` | Optional | GitHub repository in `owner/name` form for the mirrored issue. |
| `github_issue_number` | Optional | Future GitHub issue foreign key. |
| `github_issue_node_id` | Optional | Future GitHub GraphQL issue foreign key. |
| `github_project_owner` | Optional | GitHub project owner login for a synced project item. |
| `github_project_owner_type` | Optional | `user` or `organization` for a synced project item. |
| `github_project_number` | Optional | GitHub project number for a synced project item. |
| `github_project_item_id` | Optional | Future GitHub project-item foreign key. |
| `github_synced_at` | Optional | Last successful GitHub sync timestamp in UTC. |
| `tags` | Optional | Small query labels. |
| `notes` | Optional | Short operator note. |

## Process or Workflow
1. Create or update one or more local task records under `docs/planning/tasks/`.
2. Rebuild the task tracker and task index from those task records.
3. Validate that every task-index entry points to an existing task record and that task-status values match the allowed vocabulary.
4. Rebuild the traceability index when traced tasks changed.
5. Validate the task index artifact against its published schema before treating the change as complete.

## Examples
- A backlog task for GitHub sync should appear as a non-terminal task entry with `task_status` set to `backlog`.
- A closed implementation task should remain in the task index with `task_status` set to `done` and a `doc_path` under `docs/planning/tasks/closed/`.
- A task can carry a local `task_id` plus a future `github_issue_number` without changing its stable local identity.

## Operationalization
- `Modes`: `artifact`; `documentation`
- `Operational Surfaces`: `core/control_plane/indexes/tasks/task_index.v1.json`; `core/control_plane/indexes/tasks/`; `core/control_plane/indexes/tasks/README.md`; `docs/planning/tasks/`

## Validation
- The task index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a task document under `docs/planning/tasks/`.
- A task-index entry under `docs/planning/tasks/open/` should not use `done` or `cancelled`.
- A task-index entry under `docs/planning/tasks/closed/` should use only `done` or `cancelled`.
- `blocked_by` and `depends_on` references should point to existing task IDs in the current index.

## Change Control
- Update this standard when the repository changes how tasks are indexed or queried.
- Update the companion artifact schema, examples, live task index, and task sync logic in the same change set when the task-index family changes structurally.

## References
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/tasks/README.md)

## Updated At
- `2026-03-11T06:00:00Z`
