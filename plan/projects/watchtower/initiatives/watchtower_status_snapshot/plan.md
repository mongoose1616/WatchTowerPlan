# WatchTower Status Snapshot Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_status_snapshot`
- `trace_id`: `trace.watchtower_status_snapshot`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:20Z`

## Scope and Non-Goals
Adds one local-first status command so operators can see workspace readiness and current work-item counts from a single WatchTower entrypoint.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add WatchTower status snapshot flow: Add a top-level CLI path that reports workspace state and summarized work-item counts from the local .watchtower store.
- Validate WatchTower status snapshot flow: Cover the status command with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_status_snapshot.add_watchtower_status_snapshot_flow](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/.wt/tasks/add_watchtower_status_snapshot_flow/task.json) | `completed` | `high` | `repository_maintainer` | Add a top-level CLI path that reports workspace state and summarized work-item counts from the local .watchtower store. | - |
| [task.watchtower_status_snapshot.validate_watchtower_status_snapshot_flow](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/.wt/tasks/validate_watchtower_status_snapshot_flow/task.json) | `completed` | `high` | `repository_maintainer` | Cover the status command with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance. | task.watchtower_status_snapshot.add_watchtower_status_snapshot_flow |

## Dependencies and Risks
- Task `task.watchtower_status_snapshot.validate_watchtower_status_snapshot_flow` depends on `task.watchtower_status_snapshot.add_watchtower_status_snapshot_flow`.

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
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_status_snapshot/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
