# WatchTower Work Item Begin Flow Design Record

## Summary
Adds a local-first begin command so operators can mark one WatchTower work item as actively in progress before completion.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/projects/watchtower/initiatives/watchtower_work_item_begin_flow/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The project container must stay valid and current before a project-scoped initiative may execute.
- The begin flow should update the existing work-item record in place, switch `status` to `in_progress`, and preserve the original `created_at`.
- The first begin transition should stamp `started_at`; later repeated begins should keep the existing `started_at` and return a stable no-op response.
- `watchtower work next` should continue to treat `in_progress` items as unfinished candidates, so no separate selector state is introduced in this slice.
