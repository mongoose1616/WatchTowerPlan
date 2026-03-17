# WatchTower Work Item Bootstrap Design Record

## Summary
Adds a local-first work-item record flow so operators can start bounded work inside an initialized WatchTower workspace.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/projects/watchtower/initiatives/watchtower_work_item_bootstrap/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The project container must stay valid and current before a project-scoped initiative may execute.
- Work-item state should live below the existing `.watchtower/` root so it stays grouped with the initialized workspace manifest.
- `watchtower work start` should fail clearly when the workspace manifest is missing instead of silently bootstrapping unrelated state.
- Each created record should live at `.watchtower/work_items/<slug>.json` and stay human-inspectable JSON.
- The initial status should be `planned`; later work can decide how work items transition or close.
