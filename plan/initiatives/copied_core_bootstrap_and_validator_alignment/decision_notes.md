# Copied Core Bootstrap And Validator Alignment Decision Notes

## Summary
Locks the reusable-core decisions for copied-core bootstrap reconciliation and duplicate-validator handling.

## Decisions
- The duplicated shared-validator problem is fixed in reusable core, not in copied consumer repos alone.
- Identical duplicate validator definitions are allowed during merged validator loading.
- Conflicting duplicate validator definitions remain a hard failure.
- `watchtower-core pack bootstrap --write` is the copied-core reconciliation boundary for shared governed discovery surfaces.
- Bootstrap reconciliation must update:
  - `core/control_plane/registries/pack_registry.json`
  - `core/python/pyproject.toml`
  - `core/control_plane/indexes/commands/command_index.json`
  - `core/control_plane/indexes/repository_paths/repository_path_index.json`
- Bootstrap must not preserve authored hosted-pack entries that are provably unusable in the current copied repository when a new active pack is being reconciled into place.
- This slice must not weaken `WatchTowerPlan` steady-state plan behavior just to make copied-core portability easier.

## Deferred Decisions
- Whether shared `core/python/pyproject.toml` should eventually become fully pack-neutral with zero predeclared hosted-pack dependencies is deferred.
- Whether discovery query services should prefer in-memory effective indexes over persisted indexes in broader bootstrap-mode scenarios is deferred unless this slice proves it is required.
