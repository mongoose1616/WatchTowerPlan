# Plan Python Package Dependency Cleanup Implementation Slice

## Summary
Make plan/python an installable workspace package and remove the last repo-local import shim from reusable core.

## Work Breakdown
- `task.plan_python_package_dependency_cleanup.bootstrap`
  Capture the cleanup package, author the design direction, and move the initiative through confirmation and approval.
- `task.plan_python_package_dependency_cleanup.make_plan_python_installable`
  Add `plan/python/pyproject.toml`, wire the shared workspace dependency contract in `core/python/pyproject.toml`, update the lockfile, and align onboarding docs.
- `task.plan_python_package_dependency_cleanup.remove_repo_local_bootstrap`
  Remove `watchtower_core.repo_local_bootstrap`, delete `sys.path` mutation from runtime paths, and keep CLI, closeout, validation, and tests importing `watchtower_plan` through the installed package boundary.
- `task.plan_python_package_dependency_cleanup.validate_workspace_closeout`
  Run focused regressions plus final contract validation, repeat the boundary residue pass, refresh derived surfaces, and close the initiative.

## Acceptance Focus
- Runtime imports for repo-local planning behavior resolve without ad hoc path injection.
- The shared `core/python/` environment remains the only environment contract in the repository.
- No new core-vs-domain boundary leak is introduced while removing the old shim.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
