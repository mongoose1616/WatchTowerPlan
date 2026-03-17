# WatchTower Workspace Init Bootstrap Design Record

## Summary
Adds a local-first workspace manifest and init flow so later WatchTower operator work starts from a real on-disk state root.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/projects/watchtower/initiatives/watchtower_workspace_init_bootstrap/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The project container must stay valid and current before a project-scoped initiative may execute.
- The WatchTower repo will own one hidden local state root at `.watchtower/` so workspace-managed state does not leak into the top-level source tree.
- The first manifest will live at `.watchtower/workspace.json` and stay human-inspectable JSON.
- `watchtower init` should be idempotent enough for bootstrap use: create the manifest when missing and report the current initialized state when it already exists.
- `watchtower doctor` should load the manifest when present and report `workspace_initialized`; otherwise it should keep reporting the repository bootstrap state.
- The slice should keep command behavior dependency-light and filesystem-local so later operator workflows have a stable on-disk starting point.
