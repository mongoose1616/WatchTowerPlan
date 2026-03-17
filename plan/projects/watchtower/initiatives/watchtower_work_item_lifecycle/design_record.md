# WatchTower Work Item Lifecycle Design Record

## Summary
Adds local-first work-item inspection and completion flows so operators can see current work and close it cleanly inside an initialized WatchTower workspace.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/projects/watchtower/initiatives/watchtower_work_item_lifecycle/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The project container must stay valid and current before a project-scoped initiative may execute.
- Work-item inspection should read only from `.watchtower/work_items/*.json` and fail clearly when the workspace manifest is missing.
- `watchtower work list` should return a stable sorted view of local work items so repeated runs stay predictable for humans and agents.
- `watchtower work show` should return one record plus its resolved path without silently creating missing state.
- Completing a work item should update the existing record in place, switch `status` to `completed`, stamp `completed_at`, and optionally persist one closeout summary field.
- The slice should reuse the current lightweight JSON file store instead of introducing a database, daemon, or extra runtime service.
