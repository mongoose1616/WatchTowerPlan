# Copied Core Bootstrap And Validator Alignment Implementation Slice

## Summary
Hardens copied-core portability by reconciling stale donor discovery surfaces during pack bootstrap and tolerating identical shared validator copies during merged validator loading.

## Initial Work Breakdown
- `task.copied_core_bootstrap_and_validator_alignment.bootstrap_copied_core_bootstrap_and_validator_alignment`: Bootstrap Copied Core Bootstrap And Validator Alignment live initiative package.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.

## Execution Tasks
- `task.copied_core_bootstrap_and_validator_alignment.reconfirm_assessment_scope`
  - Reconfirm which copied-core assessment findings are already fixed in `WatchTowerPlan/core` and which still need code changes.
- `task.copied_core_bootstrap_and_validator_alignment.harden_validator_merge_for_copied_shared_entries`
  - Implement typed duplicate-validator tolerance for identical shared validators and add regression coverage for conflicting duplicates.
- `task.copied_core_bootstrap_and_validator_alignment.expand_pack_bootstrap_reconciliation`
  - Teach pack bootstrap to reconcile unusable donor hosted-pack entries and rebuild shared discovery surfaces in the same write path.
- `task.copied_core_bootstrap_and_validator_alignment.refresh_core_owned_operator_docs`
  - Update the bootstrap command page and workspace guidance for the stronger copied-core reconciliation behavior.
- `task.copied_core_bootstrap_and_validator_alignment.validate_and_closeout`
  - Run targeted validation, full relevant checks, close the initiative, and land bounded commits.

## Commit Boundaries
- Commit 1: validator-merge hardening plus regression tests.
- Commit 2: pack-bootstrap reconciliation plus copied-core bootstrap tests and docs.

## Validation Commands
- `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_control_plane_loader_cache.py core/python/tests/unit/test_validation_suite_service.py core/python/tests/unit/test_cli_pack_commands.py core/python/tests/unit/test_command_index_sync.py -q`
- `./core/python/.venv/bin/python -m mypy core/python/src/watchtower_core core/python/src/watchtower_host`
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/src/watchtower_host core/python/tests/unit`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Closeout Criteria
- Identical copied shared validators no longer break merged validator loading.
- Pack bootstrap can reconcile a copied-core consumer repo from stale donor registry state to a consistent post-bootstrap shared-core state.
- Shared command and repository-path discovery surfaces are updated in the same bootstrap write path.
- Current `WatchTowerPlan` plan-pack behavior and validation remain green.
