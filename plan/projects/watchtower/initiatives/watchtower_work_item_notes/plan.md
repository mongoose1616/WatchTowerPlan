# WatchTower Work Item Notes Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_work_item_notes`
- `trace_id`: `trace.watchtower_work_item_notes`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:22Z`

## Scope and Non-Goals
Adds local-first note capture on work items so operators can preserve thread context and resume a bounded slice without external scratch notes.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add WatchTower work-item note flow: Add a CLI path that appends one timestamped note to an existing local work-item record.
- Validate WatchTower work-item note flow: Cover note capture with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_work_item_notes.add_watchtower_work_item_note_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/.wt/tasks/add_watchtower_work_item_note_flow/task.json) | `completed` | `high` | `repository_maintainer` | Add a CLI path that appends one timestamped note to an existing local work-item record. | - |
| [task.watchtower_work_item_notes.validate_watchtower_work_item_note_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/.wt/tasks/validate_watchtower_work_item_note_flow/task.json) | `completed` | `high` | `repository_maintainer` | Cover note capture with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance. | task.watchtower_work_item_notes.add_watchtower_work_item_note_flow |

## Dependencies and Risks
- Task `task.watchtower_work_item_notes.validate_watchtower_work_item_note_flow` depends on `task.watchtower_work_item_notes.add_watchtower_work_item_note_flow`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `2`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_work_item_notes/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
