# Core Removable Plan Reference Cleanup Implementation Slice

## Summary
Removes non-essential plan-specific wording and examples from shared core docs, host help, and reusable-core boundaries while preserving only references required by the current repository contract.

## Work Breakdown
- `task.core_removable_plan_reference_cleanup.bootstrap_core_removable_plan_reference_cleanup`
- `task.core_removable_plan_reference_cleanup.remove_shared_docs_and_help_residue`
- `task.core_removable_plan_reference_cleanup.refresh_reusable_core_boundary_language`
- `task.core_removable_plan_reference_cleanup.reconcile_tests_and_generated_surfaces`
- `task.core_removable_plan_reference_cleanup.validate_and_close`

## Execution Order
1. Remove donor-style plan examples from shared docs and host help.
2. Rewrite reusable-core boundary guidance and fail-closed messages to generic pack language.
3. Update affected tests and regenerate machine-readable companion surfaces.
4. Run validation and close the initiative.

## Commit Shape
- Commit 1: shared docs and host help deplanification.
- Commit 2: reusable-core boundary language and test adjustments.
- Commit 3: generated-surface reconciliation, validation, and initiative closeout if needed.

## Validation Commands
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/src/watchtower_host core/python/tests`
- `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
- targeted `pytest` for wording/help/README contract tests that change
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
