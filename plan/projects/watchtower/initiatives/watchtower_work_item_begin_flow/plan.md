# WatchTower Work Item Begin Flow Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_work_item_begin_flow`
- `trace_id`: `trace.watchtower_work_item_begin_flow`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:26Z`

## Scope and Non-Goals
Adds a local-first begin command so operators can mark one WatchTower work item as actively in progress before completion.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add WatchTower work-item begin flow: Add a CLI path that marks one local work item in progress and persists active-work metadata.
- Validate WatchTower work-item begin flow: Cover the begin flow with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_work_item_begin_flow.add_watchtower_work_item_begin_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/.wt/tasks/add_watchtower_work_item_begin_flow/task.json) | `completed` | `high` | `repository_maintainer` | Add a CLI path that marks one local work item in progress and persists active-work metadata. | - |
| [task.watchtower_work_item_begin_flow.validate_watchtower_work_item_begin_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/.wt/tasks/validate_watchtower_work_item_begin_flow/task.json) | `completed` | `high` | `repository_maintainer` | Cover the begin flow with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance. | task.watchtower_work_item_begin_flow.add_watchtower_work_item_begin_flow |

## Dependencies and Risks
- Task `task.watchtower_work_item_begin_flow.validate_watchtower_work_item_begin_flow` depends on `task.watchtower_work_item_begin_flow.add_watchtower_work_item_begin_flow`.

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
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
