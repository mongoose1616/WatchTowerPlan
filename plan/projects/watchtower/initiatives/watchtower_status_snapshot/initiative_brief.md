# WatchTower Status Snapshot

## Summary
Adds one local-first status command so operators can see workspace readiness and current work-item counts from a single WatchTower entrypoint.

## Identity
- `initiative_id`: `initiative.watchtower_status_snapshot`
- `trace_id`: `trace.watchtower_status_snapshot`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`

## Initial Task Set
- `task.watchtower_status_snapshot.add_watchtower_status_snapshot_flow`: Add a top-level CLI path that reports workspace state and summarized work-item counts from the local .watchtower store.
- `task.watchtower_status_snapshot.validate_watchtower_status_snapshot_flow`: Cover the status command with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Bounded Slice
- Add `watchtower status` as the operator-facing snapshot entrypoint for the current local workspace.
- Report whether the workspace is initialized, how many local work items exist, and how many are `planned` or `completed`.
- Include a compact current-work summary so operators do not have to combine `doctor` and `work list` manually.
- Keep the status surface local-first and read-only; do not add daemon state, background polling, or remote dependencies.
