# Copied Core Bootstrap And Validator Alignment Design Record

## Summary
Hardens copied-core portability by reconciling stale donor discovery surfaces during pack bootstrap and tolerating identical shared validator copies during merged validator loading.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/copied_core_bootstrap_and_validator_alignment/.wt/`.
- The implementation boundary is reusable core plus host-owned bootstrap handling under `core/python/src/watchtower_core/**` and `core/python/src/watchtower_host/**`, with core-owned docs updated only where the changed behavior is operator-visible.

## Runtime Model
- Shared validator merging remains a typed reusable-core operation.
- The merge logic must now compare duplicate validator IDs structurally:
  - if two entries share the same `validator_id` and all typed fields match, keep the first entry and skip the duplicate
  - if two entries share the same `validator_id` and any typed field differs, fail with a precise duplicate-conflict error
- This keeps copied shared validator registries from crashing loader-backed operations while still preventing silent semantic drift.

## Bootstrap Reconciliation Model
- `pack bootstrap` remains the explicit reconciliation command after copying `core/` into a new repository.
- The bootstrap write path should:
  - load the candidate pack settings and runtime manifest
  - detect unusable authored hosted-pack entries whose declared pack settings or runtime manifest paths no longer load in the current repository
  - replace or drop those unusable entries when they conflict with the copied repository's active hosted-pack registration story
  - write the updated shared pack registry
  - write the shared workspace registration
  - rebuild shared command discovery and repository-path discovery surfaces in the same write pass
- The result is one explicit command that turns copied donor core into a consistent shared steady state for the consumer repo.

## Compatibility Rules
- Valid authored hosted-pack entries must be preserved.
- Only unusable authored entries may be removed automatically during copied-core reconciliation.
- Current `WatchTowerPlan` behavior must remain stable because its authored `plan` pack entry is valid.
- Existing command output contracts remain JSON/human-compatible; the bootstrap payload simply reports more changed paths when the additional reconciliation writes occur.

## Validation Strategy
- Add model or loader-level tests for identical and conflicting duplicate validator IDs.
- Add bootstrap reconciliation tests on a copied-core fixture repo that starts with a stale donor `plan` entry and an unbootstrapped `oversight` root pack.
- Validate that bootstrap dry runs preview the shared governed-surface updates accurately and write mode persists them.
