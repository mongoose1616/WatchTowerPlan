# Plan Path And ID Helper Foundation Implementation Slice

## Summary
Adds reusable path and id helpers so plan initiative, project, task, and companion artifact naming stops living in scattered repo-local string conventions.

## Initial Work Breakdown
- `task.plan_path_and_id_helper_foundation.add_path_and_id_helper`: Implement a reusable-core helper for canonical slugs, ids, and plan-workspace root paths.
- `task.plan_path_and_id_helper_foundation.refactor_plan_runtime_callers`: Adopt the helper in initiative, project, and related runtime surfaces that currently hand-roll canonical names and paths.
- `task.plan_path_and_id_helper_foundation.validate_helper_and_reconcile_requirements`: Add focused tests for the helper and align requirements.md with the implemented runtime seam.

## Expected Touchpoints
- `core/python/src/watchtower_core/control_plane/`: new helper module plus package exports and runtime-boundary documentation.
- `core/python/src/watchtower_core/repo_ops/initiative_packages.py`: move initiative slug, id, root-path, and companion-artifact id derivation onto the shared helper.
- `core/python/src/watchtower_core/repo_ops/project_workspace.py`: move project-root, initiative-root, project-id, and repository-id derivation onto the shared helper where the rules are canonical.
- `core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py` and `core/python/src/watchtower_core/repo_ops/task_lifecycle_support.py`: reuse the shared slug normalization instead of maintaining separate local variants.
- `core/python/tests/unit/` and targeted integration coverage: prove canonical derivation, fail-closed validation, and caller adoption.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
