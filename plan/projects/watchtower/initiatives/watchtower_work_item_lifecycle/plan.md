# WatchTower Work Item Lifecycle Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_work_item_lifecycle`
- `trace_id`: `trace.watchtower_work_item_lifecycle`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:18Z`

## Scope and Non-Goals
Adds local-first work-item inspection and completion flows so operators can see current work and close it cleanly inside an initialized WatchTower workspace.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add WatchTower work-item completion flow: Add a CLI path that marks one local work item completed and records its closeout metadata.
- Add WatchTower work-item inspection flows: Add CLI paths that list local work items and show one work-item record from the initialized workspace state root.
- Validate WatchTower work-item lifecycle flow: Cover work-item inspection and completion with CLI tests, exercise the commands against the initialized WatchTower repo, and refresh repo guidance.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_work_item_lifecycle.add_watchtower_work_item_completion_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/.wt/tasks/add_watchtower_work_item_completion_flow/task.json) | `completed` | `high` | `repository_maintainer` | Add a CLI path that marks one local work item completed and records its closeout metadata. | task.watchtower_work_item_lifecycle.add_watchtower_work_item_inspection_flows |
| [task.watchtower_work_item_lifecycle.add_watchtower_work_item_inspection_flows](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/.wt/tasks/add_watchtower_work_item_inspection_flows/task.json) | `completed` | `high` | `repository_maintainer` | Add CLI paths that list local work items and show one work-item record from the initialized workspace state root. | - |
| [task.watchtower_work_item_lifecycle.validate_watchtower_work_item_lifecycle_flow](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/.wt/tasks/validate_watchtower_work_item_lifecycle_flow/task.json) | `completed` | `high` | `repository_maintainer` | Cover work-item inspection and completion with CLI tests, exercise the commands against the initialized WatchTower repo, and refresh repo guidance. | task.watchtower_work_item_lifecycle.add_watchtower_work_item_inspection_flows, task.watchtower_work_item_lifecycle.add_watchtower_work_item_completion_flow |

## Dependencies and Risks
- Task `task.watchtower_work_item_lifecycle.add_watchtower_work_item_completion_flow` depends on `task.watchtower_work_item_lifecycle.add_watchtower_work_item_inspection_flows`.
- Task `task.watchtower_work_item_lifecycle.validate_watchtower_work_item_lifecycle_flow` depends on `task.watchtower_work_item_lifecycle.add_watchtower_work_item_inspection_flows`, `task.watchtower_work_item_lifecycle.add_watchtower_work_item_completion_flow`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `3`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
