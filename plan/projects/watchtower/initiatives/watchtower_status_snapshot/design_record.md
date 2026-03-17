# WatchTower Status Snapshot Design Record

## Summary
Adds one local-first status command so operators can see workspace readiness and current work-item counts from a single WatchTower entrypoint.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/projects/watchtower/initiatives/watchtower_status_snapshot/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The project container must stay valid and current before a project-scoped initiative may execute.
- `watchtower status` should stay distinct from `watchtower doctor`: doctor reports bootstrap diagnostics, while status reports operator-facing workspace and work-item state.
- The status payload should work before and after initialization, returning zero counts and a missing-workspace state when `.watchtower/workspace.json` does not exist yet.
- The command should summarize local work items from `.watchtower/work_items/*.json` without mutating them.
- The slice should not introduce dashboards, watch mode, or timeline history beyond the current local record set.
