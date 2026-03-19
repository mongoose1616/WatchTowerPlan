# WatchTower Work Item Bootstrap Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_work_item_bootstrap`
- `trace_id`: `trace.watchtower_work_item_bootstrap`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:17Z`

## Scope and Non-Goals
Adds a local-first work-item record flow so operators can start bounded work inside an initialized WatchTower workspace.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add WatchTower work-item start flow: Add a CLI path that creates one local work-item record under the initialized workspace state root.
- Validate WatchTower work-item start flow: Cover workspace-required work-item creation with CLI tests and exercise the flow against the initialized WatchTower repo.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_work_item_bootstrap.add_watchtower_work_item_start_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/.wt/tasks/add_watchtower_work_item_start_flow/task.json) | `completed` | `high` | `repository_maintainer` | Add a CLI path that creates one local work-item record under the initialized workspace state root. | - |
| [task.watchtower_work_item_bootstrap.validate_watchtower_work_item_start_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/.wt/tasks/validate_watchtower_work_item_start_flow/task.json) | `completed` | `high` | `repository_maintainer` | Cover workspace-required work-item creation with CLI tests and exercise the flow against the initialized WatchTower repo. | task.watchtower_work_item_bootstrap.add_watchtower_work_item_start_flow |

## Dependencies and Risks
- Task `task.watchtower_work_item_bootstrap.validate_watchtower_work_item_start_flow` depends on `task.watchtower_work_item_bootstrap.add_watchtower_work_item_start_flow`.

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
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
