# WatchTower Next Work Selection Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_next_work_selection`
- `trace_id`: `trace.watchtower_next_work_selection`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:24Z`

## Scope and Non-Goals
Adds a local-first next-work command so operators can ask WatchTower what unfinished work should be picked up next from the current workspace state.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add WatchTower next-work flow: Add a CLI path that selects one unfinished local work item and returns a compact resume snapshot.
- Validate WatchTower next-work flow: Cover next-work selection with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_next_work_selection.add_watchtower_next_work_flow](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/.wt/tasks/add_watchtower_next_work_flow/task.json) | `completed` | `high` | `repository_maintainer` | Add a CLI path that selects one unfinished local work item and returns a compact resume snapshot. | - |
| [task.watchtower_next_work_selection.validate_watchtower_next_work_flow](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/.wt/tasks/validate_watchtower_next_work_flow/task.json) | `completed` | `high` | `repository_maintainer` | Cover next-work selection with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance. | task.watchtower_next_work_selection.add_watchtower_next_work_flow |

## Dependencies and Risks
- Task `task.watchtower_next_work_selection.validate_watchtower_next_work_flow` depends on `task.watchtower_next_work_selection.add_watchtower_next_work_flow`.

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
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_next_work_selection/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
