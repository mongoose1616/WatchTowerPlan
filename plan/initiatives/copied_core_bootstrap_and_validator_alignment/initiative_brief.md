# Copied Core Bootstrap And Validator Alignment

## Summary
Hardens copied-core portability by reconciling stale donor discovery surfaces during pack bootstrap and tolerating identical shared validator copies during merged validator loading.

## Identity
- `initiative_id`: `initiative.copied_core_bootstrap_and_validator_alignment`
- `trace_id`: `trace.copied_core_bootstrap_and_validator_alignment`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.copied_core_bootstrap_and_validator_alignment.bootstrap_copied_core_bootstrap_and_validator_alignment`: Bootstrap Copied Core Bootstrap And Validator Alignment live initiative package.

## Problem
- The copied-core assessment against `WatchTowerOversight` shows that runtime bootstrap discovery is now ahead of the governed shared-core surfaces.
- The two reusable-core defects with the highest integration cost are:
  - copied shared validators in a consumer pack still crash merged validator loading instead of deduplicating identical shared definitions
  - `watchtower-core pack bootstrap` updates only the shared pack registry and shared workspace pyproject, which leaves stale donor command and repository-path discovery surfaces behind after a core copy
- The copied-core assessment also shows stale donor entries surviving in the shared hosted-pack registry after copy-forward. The bootstrap story is therefore incomplete: it registers the new hosted pack, but it does not fully reconcile invalid donor state into a usable post-copy steady state.

## Desired Outcome
- Identical shared validator copies in a consumer pack no longer break merged validator loading.
- Conflicting duplicate validator definitions still fail closed with a precise error.
- One `watchtower-core pack bootstrap --write` run on a copied-core repository can reconcile stale donor hosted-pack registry state, sync the shared workspace registration, and rebuild the shared command and repository-path discovery surfaces.
- The copied-core fix improves downstream portability without changing `WatchTowerPlan` steady-state plan ownership, live plan commands, or current plan pack behavior.

## In Scope
- `core/python/src/watchtower_core/control_plane/models/catalog_core.py`
- `core/python/src/watchtower_core/control_plane/loader_cache.py`
- `core/python/src/watchtower_core/control_plane/loader_surfaces.py`
- `core/python/src/watchtower_core/pack_integration/bootstrap.py`
- `core/python/src/watchtower_core/pack_integration/runtime_registry.py`
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- core-owned command docs and workspace guidance touched by the updated bootstrap behavior
- shared-core unit and integration tests needed to prove copied-core reconciliation and validator merge tolerance

## Out Of Scope
- Oversight-owned artifact fixes under `/home/j/WatchTowerOversight/oversight/**`
- Removing the live `plan` hosted pack from `WatchTowerPlan`
- Replacing every remaining `watchtower_plan` import in the shared-core test suite
- Reworking generic query services to stop using persisted indexes outside the specific copied-core bootstrap alignment needed in this slice

## Operator Requirements
- A copied-core consumer must be able to bootstrap its active first-party pack and end up with a consistent shared hosted-pack registry, shared workspace registration, command discovery surface, and repository-path discovery surface.
- Shared validation must tolerate copied shared validators only when the duplicate definitions are byte-for-byte equivalent at the typed contract level.
- Shared validation must still fail closed when a consumer pack redefines a shared validator ID with different content.

## Acceptance Criteria
- `ValidatorRegistry.merge(...)` deduplicates identical validator definitions while still rejecting conflicting duplicates.
- `watchtower-core pack bootstrap --write` removes or replaces unusable donor registry entries when bootstrapping the copied repository's active pack, instead of preserving broken donor entries as if they were still valid hosted packs.
- `watchtower-core pack bootstrap --write` rebuilds the shared command index and repository path index in the same write path so copied-core discovery surfaces align immediately after bootstrap.
- The bootstrap dry-run and write results report the additional changed paths and next-step behavior accurately.
- Targeted reusable-core tests prove the copied-core bootstrap reconciliation flow and duplicate-validator tolerance flow.

## Non Goals
- This initiative does not try to make copied-core repositories fully self-healing without any explicit bootstrap or sync step.
- This initiative does not remove current-repo facts from `WatchTowerPlan` docs or machine surfaces when those facts remain true in this repository.
