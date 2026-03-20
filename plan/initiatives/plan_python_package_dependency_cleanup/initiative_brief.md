# Plan Python Package Dependency Cleanup

## Summary
Make plan/python an installable workspace package and remove the last repo-local import shim from reusable core.

## Identity
- `initiative_id`: `initiative.plan_python_package_dependency_cleanup`
- `trace_id`: `trace.plan_python_package_dependency_cleanup`
- `scope_type`: `pack_wide`

## Problem
- The current core-versus-domain split is functionally correct but still relies on `watchtower_core.repo_local_bootstrap` mutating `sys.path` so `watchtower_core` can import `watchtower_plan`.
- That shim keeps repository-specific package-loading knowledge inside reusable core and leaves one avoidable boundary leak after the broader hard cutover.
- The shared Python workspace already owns the environment, lockfile, and command contract, so `plan/python/` should participate as an installable package instead of as an ad hoc source-path append.

## Goals
- Make `plan/python/` a real installable package in the shared `core/python/` workspace.
- Remove repo-local path bootstrapping from `watchtower_core`.
- Keep a single shared environment model under `core/python/.venv/`.
- Preserve the explicit core-versus-domain split: reusable behavior in `watchtower_core`, plan-domain behavior in `watchtower_plan`.

## Non-Goals
- Do not create a second virtual environment under `plan/python/`.
- Do not move runtime implementation into `plan/.wt/`.
- Do not widen `watchtower_plan` with pack-agnostic helpers that should live in reusable core.

## Planned Task Set
- `task.plan_python_package_dependency_cleanup.bootstrap`: Capture and approve the cleanup package so execution can start cleanly.
- `task.plan_python_package_dependency_cleanup.make_plan_python_installable`: Add package metadata and shared-workspace installation wiring for `watchtower_plan`.
- `task.plan_python_package_dependency_cleanup.remove_repo_local_bootstrap`: Remove the last repo-local import shim from `watchtower_core` and keep runtime imports working through the installed plan package.
- `task.plan_python_package_dependency_cleanup.validate_workspace_closeout`: Validate the final tree, run one more residue pass, and close the initiative.
