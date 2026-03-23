# Copy-Forward Pack Runtime Hardening Implementation Slice

## Summary
Hardens reusable core for copied-core host scenarios by discovering unbootstrapped hosted packs from manifests, structuring stale-registry failures, and keeping current shared workspace contracts explicit.

## Work Breakdown
- `task.copy_forward_pack_runtime_hardening.bootstrap_copy_forward_pack_runtime_hardening`
  - Confirm the initiative package, authored inputs, approval state, and execution scope.
- `task.copy_forward_pack_runtime_hardening.implement_effective_pack_discovery`
  - Add reusable runtime support for an effective hosted-pack view that merges valid authored registry entries with manifest-discovered bootstrap-mode entries.
- `task.copy_forward_pack_runtime_hardening.harden_selected_pack_commands`
  - Update pack list, describe, validate, and selected namespace discovery so stale donor registry entries degrade structurally and discovered packs remain operable.
- `task.copy_forward_pack_runtime_hardening.cover_copy_forward_bootstrap_mode`
  - Add or extend reusable-core tests for copied-core repos carrying a first-party/root pack before local bootstrap rewiring.
- `task.copy_forward_pack_runtime_hardening.refresh_docs_and_contract_language`
  - Update the shared Python-workspace and pack-interface docs so bootstrap-mode fallback and steady-state authored registration are both explicit.
- `task.copy_forward_pack_runtime_hardening.validate_and_close`
  - Run targeted and broad validation, record outcomes, update closeout surfaces, and close the initiative.

## Commit Plan
1. `feat(pack-runtime): add bootstrap-mode effective pack discovery`
   - Runtime helpers, host CLI resolution, and regression tests for stale authored registry handling.
2. `docs(pack-runtime): document copy-forward bootstrap mode`
   - Standards, references, README updates, initiative closeout surfaces, and any final reconciliation.

## Validation Commands
- `./core/python/.venv/bin/pytest core/python/tests/unit/test_cli_pack_commands.py core/python/tests/unit/test_pack_integration_runtime.py core/python/tests/integration/test_pack_externalization.py -q`
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/src/watchtower_host core/python/tests/unit core/python/tests/integration`
- `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
- `./core/python/.venv/bin/pytest core/python/tests/unit core/python/tests/integration -q`

## Closeout Criteria
- The effective hosted-pack runtime view is manifest-driven and deterministic.
- Copied-core bootstrap-mode behavior no longer fails purely because the authored donor registry is stale for the consuming repository.
- Current internal `plan` behavior remains intact in `WatchTowerPlan`.
- Shared docs explain the distinction between copied-core bootstrap mode and steady-state authored registration.
- The initiative package is validated, closed, and committed.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
