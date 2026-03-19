# WatchTower Workspace Init Bootstrap Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_workspace_init_bootstrap`
- `trace_id`: `trace.watchtower_workspace_init_bootstrap`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:15Z`

## Scope and Non-Goals
Adds a local-first workspace manifest and init flow so later WatchTower operator work starts from a real on-disk state root.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add WatchTower workspace init flow: Add a CLI init path that writes a local workspace manifest and establishes the managed state root.
- Validate WatchTower workspace init flow: Exercise the generated workspace manifest through CLI tests and update doctor to surface the initialized workspace state.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_workspace_init_bootstrap.add_watchtower_workspace_init_flow](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/.wt/tasks/add_watchtower_workspace_init_flow/task.json) | `completed` | `high` | `repository_maintainer` | Add a CLI init path that writes a local workspace manifest and establishes the managed state root. | - |
| [task.watchtower_workspace_init_bootstrap.validate_watchtower_workspace_init_flow](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/.wt/tasks/validate_watchtower_workspace_init_flow/task.json) | `completed` | `high` | `repository_maintainer` | Exercise the generated workspace manifest through CLI tests and update doctor to surface the initialized workspace state. | task.watchtower_workspace_init_bootstrap.add_watchtower_workspace_init_flow |

## Dependencies and Risks
- Task `task.watchtower_workspace_init_bootstrap.validate_watchtower_workspace_init_flow` depends on `task.watchtower_workspace_init_bootstrap.add_watchtower_workspace_init_flow`.

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
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
