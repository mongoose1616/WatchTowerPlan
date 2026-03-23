# Mandatory Pack Context Loader Bootstrap Design Record

## Summary
Makes effective pack resolution the required first phase for pack-aware loader, host, validation, and runtime operations, with full `PackContext` loading reserved for consumers that actually need pack-governed surfaces.

## Design Boundary
- The initiative package remains machine-first and local to `plan/initiatives/mandatory_pack_context_loader_bootstrap/.wt/`.
- The implementation boundary is reusable core first, with plan-owned tests and fixture helpers updated only when they encode stale pack-module or pack-context assumptions.
- The architecture goal is to remove duplicated effective-pack bootstrap logic, not to add another special-case layer around copied-core bring-up.

## Runtime Model
- `ControlPlaneLoader` should own the effective pack resolution path.
- The loader should resolve:
  - effective `pack_settings_path`
  - loader activation for the effective pack
  - typed `PackContext` when the caller needs full pack-governed surfaces
  - effective runtime manifest
  - effective runtime registry entry or synthesized runtime entry
- Pack-aware callers should consume that loader-owned state instead of re-deriving partial pieces independently.

## Loader Strategy
- Add one canonical effective pack bootstrap helper on the loader side and cache the full `PackContext` result for the life of the loader instance when a caller asks for it.
- Ensure that when the effective pack is repo-local, schema-store augmentation and declared surface activation happen as part of loader activation, not as ad hoc command-local work.
- Keep the existing ability to derive a loader for another explicit `pack_settings_path`, but make the derived loader bootstrap through the same activation path and only materialize the full `PackContext` when the derived caller actually needs it.

## Neighbor Surface Strategy
- Rewire pack-aware neighbors to consume the loader-owned context first:
  - default-pack activation and governed surface resolution
  - runtime integration loading
  - runtime registry default selection
  - validation context construction
  - doctor/default-pack host helpers
  - sync harness runtime-loader creation
- Preserve pack-neutral shared-core seams and keep plan-owned runtime assumptions behind the pack boundary.
- Allow runtime-only copied-pack fixtures to remain minimal by stopping at loader activation when the seam does not consume the heavier pack-governed surface set.

## Test Strategy
- Add reusable-core regression coverage for loader-side effective pack context caching and default-pack context activation.
- Keep copied-core regressions that prove:
  - pack-local schema catalogs participate before default-pack governed artifacts load
  - stale imported `watchtower_<pack>` modules are purged when the current repo root differs
- Harden plan-owned tests that intentionally exercise externalized pack reloads so they patch current module/import boundaries rather than stale collection-time modules.

## Documentation Strategy
- Update core-owned engineering and pack-authoring docs so future developers and agents treat effective pack activation as Phase 0 for pack-aware behavior and reserve full `PackContext` loading for governed-surface consumers.
- Keep the split between shared-core generic tests and pack-owned tests explicit in the guidance.

## Validation Strategy
- Run targeted unit and integration coverage around loader/runtime/validation seams while refactoring.
- Finish with the broad shared-plus-plan pytest sweep and `watchtower-core validate all --skip-acceptance --format json`.
- Re-close the initiative only after coordination returns to `ready_for_bootstrap`.
