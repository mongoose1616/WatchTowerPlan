# Copied Core Discovery Surface Reconciliation Followup Implementation Slice

## Summary
Extends copied-core bootstrap so shared discovery surfaces converge beyond command and repository-path indexes, and updates copy-forward guidance to exclude runtime environment artifacts.

## Initial Work Breakdown
- `task.copied_core_discovery_surface_reconciliation_followup.bootstrap_copied_core_discovery_surface_reconciliation_followup`: Bootstrap Copied Core Discovery Surface Reconciliation Followup live initiative package.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.

## Execution Tasks
- `task.copied_core_discovery_surface_reconciliation_followup.reconfirm_neighbor_surface_gap`
  - Reconfirm which assessment findings are already fixed and capture the remaining copied-core bootstrap reconciliation gap with current evidence.
- `task.copied_core_discovery_surface_reconciliation_followup.expand_bootstrap_discovery_surface_rebuild`
  - Widen the reusable-core bootstrap write path, rollback path, and changed-path reporting to include the remaining shared discovery indexes.
- `task.copied_core_discovery_surface_reconciliation_followup.add_copied_core_regression_coverage`
  - Update copied-core fixture support and tests so the widened bootstrap contract is proven against a donor-shaped temp repo.
- `task.copied_core_discovery_surface_reconciliation_followup.refresh_copy_forward_docs`
  - Update bootstrap/operator docs and workspace guidance so future pack authors and agents copy only supported source surfaces and rely on bootstrap for convergence.
- `task.copied_core_discovery_surface_reconciliation_followup.validate_and_closeout`
  - Run targeted validation, full relevant checks, close the initiative, and land the bounded commit set.

## Commit Boundaries
- Commit 1: reusable-core bootstrap widening plus regression coverage.
- Commit 2: copy-forward/bootstrap docs refresh, validation, and initiative closeout.

## Validation Commands
- `./core/python/.venv/bin/python -m pytest plan/python/tests/unit/test_cli_pack_commands.py core/python/tests/unit/test_standard_index_sync.py core/python/tests/unit/test_workflow_index_sync.py core/python/tests/unit/test_route_index_sync.py core/python/tests/unit/test_repo_root_discovery.py core/python/tests/integration/test_validate_all_cli.py -q`
- `./core/python/.venv/bin/python -m mypy core/python/src/watchtower_core`
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/tests plan/python/tests/unit/test_cli_pack_commands.py`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Closeout Criteria
- Copied-core bootstrap rebuilds the full shared discovery surface set needed to remove donor pack residue after copy-forward.
- Dry-run and write output both reflect the broader shared changed-path set accurately.
- Rollback still restores all touched shared files on failure.
- Core-owned docs tell downstream operators not to copy `.venv`, caches, or runtime artifacts with `core/` and to rely on bootstrap for convergence.
