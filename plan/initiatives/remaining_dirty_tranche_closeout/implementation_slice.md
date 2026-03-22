# Remaining Dirty Tranche Closeout Implementation Slice

## Summary
Inventories the remaining dirty worktree, lands the validated slices as coherent commits, and returns the repository to a clean state.

## Work Breakdown
- `task.remaining_dirty_tranche_closeout.bootstrap_remaining_dirty_tranche_closeout`: Bootstrap, scope, and approve the cleanup initiative package.
- `task.remaining_dirty_tranche_closeout.retained_records_closeout`: Land the retained-records conversion and ledger-family retirement slice with aligned docs, schemas, registries, loaders, validators, tests, and committed initiative package.
- `task.remaining_dirty_tranche_closeout.foundations_governance_refresh`: Land the foundations and governance refresh slice with mirrored docs, README governance pointers, indexes, and review-artifact updates.
- `task.remaining_dirty_tranche_closeout.reusable_core_refactor_closeout`: Land the reusable-core hotspot refactor slice with loader and catalog splits, shared typing fixes, and rebalanced shared tests.
- `task.remaining_dirty_tranche_closeout.plan_runtime_refactor_closeout`: Land the plan-runtime hotspot refactor slice with workspace, initiatives, tasks, promotion, plan sync/query alignment, and the final full validation gate.

## Validation Strategy
- Run slice-local validation before each commit using targeted `ruff`, `mypy`, `pytest`, and affected CLI validation commands.
- Rebuild derived planning, traceability, foundation, standard, reference, repository-path, and command-index surfaces in the same slice where their governing inputs changed.
- Run the full repository gate after the final slice:
  - `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
  - `./core/python/.venv/bin/pytest core/python/tests/unit core/python/tests/integration -q`
  - repo-targeted `ruff check` and `mypy` over both `watchtower_core` and `watchtower_plan`

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
