# Repository Tech Debt Reduction Program Implementation Slice

## Summary
Makes tech-debt reduction the active repository priority, starting with legacy residue removal, integration-tail reduction, and stale compatibility cleanup across core, host, and pack-owned code.

## Work Breakdown
- `task.repository_tech_debt_reduction_program.bootstrap_repository_tech_debt_reduction_program`
  - Author the initiative package.
  - Confirm and approve the authored inputs.
  - Seed the detailed execution tasks.
- `task.repository_tech_debt_reduction_program.inventory_high_cost_technical_debt`
  - Profile the current integration-tail cost.
  - Inventory stale compatibility shims, migration residue, and duplicate authority surfaces.
  - Rank the first removal slices by cost and cleanup value.
- `task.repository_tech_debt_reduction_program.reduce_integration_tail_and_tier_tests`
  - Remove or downgrade redundant integration and end-to-end cases.
  - Reuse cached or prepared baselines more aggressively.
  - Define a clearer fast-versus-slow suite boundary if the remaining tail still justifies it.
- `task.repository_tech_debt_reduction_program.remove_stale_compatibility_and_migration_residue`
  - Remove stale compatibility imports, migration-era helpers, and dead edge-case paths that no longer protect active contracts.
  - Keep remaining compatibility surfaces only when they still defend a real boundary.
- `task.repository_tech_debt_reduction_program.reconcile_duplicate_registry_and_contract_declarations`
  - Identify duplicated validator, schema, or registry declarations between `core` and `plan`.
  - Collapse them where one authority surface should remain canonical.
  - Document any required duplication that cannot yet be removed.
- `task.repository_tech_debt_reduction_program.validate_and_close_first_tech_debt_tranche`
  - Run the full repo gate.
  - Record removed debt and explicit deferrals.
  - Close the initiative on the final green tree.

## Commit Boundaries
- Commit 1: bootstrap, authored inputs, machine confirmation, approval, and task seeding.
- Commit 2: debt inventory and evidence capture.
- Commit 3: integration-tail reduction and test-tier cleanup.
- Commit 4: stale compatibility and migration residue removal.
- Commit 5: registry or contract authority cleanup.
- Commit 6: final validation, summary, and initiative closeout.

## Validation Strategy
- Before execution:
  - `./core/python/.venv/bin/watchtower-core plan confirm-inputs --initiative-slug repository_tech_debt_reduction_program --write --format json`
  - `./core/python/.venv/bin/watchtower-core plan approve --initiative-slug repository_tech_debt_reduction_program --write --format json`
- After each slice:
  - targeted `ruff`
  - targeted `mypy`
  - targeted unit and integration tests for the touched seam
  - focused runtime or test-duration comparison when runtime debt is involved
- Final gate:
  - `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/tests/unit`
  - `./core/python/.venv/bin/ruff check plan/python/src/watchtower_plan core/python/tests/integration`
  - `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
  - `./core/python/.venv/bin/mypy plan/python/src/watchtower_plan`
  - `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
  - `./core/python/.venv/bin/pytest core/python/tests/unit core/python/tests/integration -q`

## Exit Conditions
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
- The first tranche closes only after the highest-cost debt slices are either removed or explicitly deferred with evidence and rationale.
