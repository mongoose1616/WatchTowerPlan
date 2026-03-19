---
id: "std.data_contracts.task_index"
title: "Task Index Standard"
summary: "This standard defines the role, structure, and boundary rules for the live plan task index stored under plan/.wt/indexes/."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "task_index"
  - "planning_index_family"
owner: "repository_maintainer"
updated_at: "2026-03-18T14:00:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "plan/.wt/indexes/task_index.json"
aliases:
  - "task index"
  - "live task index"
---

# Task Index Standard

## Summary
This standard defines the role, structure, and boundary rules for the live plan task index stored under `plan/.wt/indexes/`.

## Purpose
Provide one machine-readable lookup surface for live initiative-local task state so tooling, agents, and sync workflows can query current task execution without scanning every initiative directory directly.

## Scope
- Applies to `plan/.wt/indexes/task_index.json`.
- Covers entry shape, source-of-truth rules, and the relationship between initiative-local task state, human trackers, and task lookup.
- Does not replace initiative-local `task.json` state as the live task source of truth.

## Use When
- Adding or updating live initiative-local tasks.
- Rebuilding task lookup data after live task changes.
- Reviewing whether task metadata belongs in the task index or only in the initiative-local task record.

## Related Standards and Sources
- [planning_index_family_standard.md](/docs/standards/data_contracts/planning_index_family_standard.md): defines the shared derived-index baseline and discoverability contract this task-family standard narrows.
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md): defines the live task authority boundary and companion human tracker expectations.
- [task_md_standard.md](/docs/standards/documentation/task_md_standard.md): defines the retained-history boundary for docs-backed task Markdown.
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md): constrains trace-linked task expectations.
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): constrains schema and validation behavior for the artifact family.

## Guidance
- Keep the authoritative task content in initiative-local `task.json` records under `plan/**/.wt/tasks/**`.
- Keep the human task tracker and task index derived from that live task state.
- Every task-index entry must point to an existing initiative-local `task.json` path.
- Keep live task execution state in the entry `status` field and use the canonical live task vocabulary.
- Update the task index in the same change set whenever live task records change materially.

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
| `initiative_id` | Required | Stable live initiative identifier. |
| `project_id` | Optional | Present when the task belongs to a project-scoped initiative. |
| `trace_id` | Required | Shared initiative trace identifier. |
| `initiative_title` | Required | Human-readable initiative title. |
| `title` | Required | Stable task title. |
| `summary` | Required | Short execution summary. |
| `status` | Required | Current live execution state such as `planned` or `completed`. |
| `task_kind` | Required | Bounded task category such as `feature` or `bug`. |
| `priority` | Required | Task priority. |
| `owner` | Required | Responsible maintainer or role. |
| `doc_path` | Required | Repository-relative live task record path ending in `task.json`. |
| `updated_at` | Required | Last meaningful task update in UTC. |
| `blocked_by` | Optional | Task IDs that block the current task. |
| `depends_on` | Optional | Task IDs the current task depends on. |
| `related_ids` | Optional | Stable IDs for PRDs, decisions, designs, plans, or other governed surfaces. |

## Process or Workflow
1. Create or update one or more initiative-local live task records.
2. Rebuild `plan/.wt/indexes/task_index.json` from that live task state.
3. Refresh companion human trackers and coordination surfaces in the same change set.
4. Validate that every task-index entry points to an existing live task record and that status values match the allowed vocabulary.
5. Validate the task index artifact against its published schema before treating the change as complete.

## Examples
- A newly created task should appear with `status` set to `planned` and a `doc_path` beneath one initiative-local `.wt/tasks/` root.
- A completed task should remain in the index with `status` set to `completed` and the same initiative-local `doc_path`.
- A project-scoped task should carry both `initiative_id` and `project_id`.

## Operationalization
- `Modes`: `artifact`; `documentation`
- `Operational Surfaces`: `plan/.wt/indexes/task_index.json`; `plan/initiatives/`; `plan/projects/`; `docs/planning/tasks/task_tracking.md`

## Validation
- In addition to the shared planning-index-family validation contract:
- Every `doc_path` should exist and point to a live initiative-local `task.json`.
- Every entry `status` should use the canonical live task vocabulary.
- `blocked_by` and `depends_on` references should point to existing task IDs in the current index.

## Change Control
- In addition to the shared planning-index-family change-control contract:
- Update this standard when the repository changes how live tasks are indexed or queried.
- Update the task tracker, task-tracking standard, and coordination surfaces in the same change set when task-index changes alter execution visibility materially.

## References
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md)
- [task_md_standard.md](/docs/standards/documentation/task_md_standard.md)
- [README.md](/docs/planning/tasks/README.md)

## Updated At
- `2026-03-18T14:00:00Z`
