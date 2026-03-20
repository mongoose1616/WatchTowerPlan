# Plan Python Package Dependency Cleanup Decision Notes

## Summary
Make `plan/python/` installable instead of preserving a repo-local import shim inside reusable core.

## Decisions
- Reject moving plan Python into `.wt/`; `.wt/` remains machine state only.
- Reject keeping `watchtower_core.repo_local_bootstrap` as an accepted permanent boundary adapter.
- Prefer an installable `watchtower_plan` package under `plan/python/` that participates in the shared `core/python/` workspace.
- Keep the single-environment model under `core/python/.venv/`; this cleanup must not create a second venv or a second command root.
