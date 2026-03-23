# Mandatory Pack Context Loader Bootstrap

## Summary
Makes effective pack resolution and PackContext activation the required first phase for pack-aware loader, host, validation, and runtime operations.

## Identity
- `initiative_id`: `initiative.mandatory_pack_context_loader_bootstrap`
- `trace_id`: `trace.mandatory_pack_context_loader_bootstrap`
- `scope_type`: `pack_wide`

## Problem
- Repeated copied-core portability loops keep uncovering the same class of failure in different neighbors: one code path reads default-pack governed surfaces first, another resolves runtime manifests first, another imports `watchtower_<pack>` first, and another derives validation context separately.
- Shared core already has a typed `PackContext`, but it is not the mandatory Phase 0 bootstrap for pack-aware behavior. Callers still reconstruct partial pack state ad hoc through `default_pack_settings_path()`, `_ensure_default_pack_settings_activated()`, `load_pack_runtime_manifest()`, and runtime-registry helpers.
- That fragmentation makes copied-pack bring-up fragile, makes test order matter, and allows pack-local schema catalogs or registries to participate too late in the loader lifecycle.

## Desired Outcome
- Shared core has one canonical loader-owned effective pack bootstrap path.
- Any host, validation, sync, query, or runtime operation that is pack-aware resolves and activates the effective pack settings path before touching pack-local governed surfaces or importing pack runtime modules.
- Consumers that actually need pack-governed surfaces build the typed `PackContext` through that same loader-owned path instead of re-deriving partial state.
- Default-pack governed surface reads, runtime pack registry composition, and pack runtime imports all use the same effective pack identity and the same cached context.
- Future packs can be scaffolded, bootstrapped, validated, and iterated without rediscovering plan-shaped loader assumptions one command at a time.

## In Scope
- `core/python/src/watchtower_core/control_plane/**` loader, pack-context, and validation-context seams
- `core/python/src/watchtower_core/pack_integration/**` runtime and runtime-registry seams
- pack-aware host entrypoints such as `doctor`, command-group discovery, and any default-pack helper that should load through the shared context first
- shared-core regression coverage plus affected plan-owned pack-boundary tests
- core-owned standards and authoring docs that need to state the PackContext-first invariant
- the normal initiative package, validation, traceability refresh, and closeout surfaces for this change

## Out Of Scope
- redesigning all pack-owned runtime descriptors or command payloads
- changing Oversight-owned files directly in this tranche
- moving plan-owned orchestration into reusable core
- treating every pack-owned test as reusable-core coverage; shared-core and plan-owned boundaries remain separate

## Operator Requirements
- A copied repo with a valid hosted pack must be able to resolve the effective pack context before any pack-aware command or validation path loads pack-local governed surfaces.
- Generic host commands must not rely on persisted donor defaults when discovered runtime pack selection has already moved ahead.
- Shared-core tests that need pack-aware behavior must use the typed loader/runtime seams rather than bypassing them through stale module imports.

## Acceptance Criteria
- `ControlPlaneLoader` exposes one canonical effective pack activation path plus a cached `load_active_pack_context()` path for full governed-surface consumers.
- Default-pack governed surface helpers, pack runtime loading, validation context loading, and pack-aware host helpers all use the loader-owned activation path instead of reconstructing pack identity independently.
- Copied-core doctor/default-pack schema resolution remains green and no longer depends on command-local lazy activation hacks.
- Broad shared-plus-plan validation passes after the refactor.
- Core-owned engineering and pack-authoring docs state that effective pack context bootstrap is Phase 0 for pack-aware behavior.

## Non Goals
- inventing a second parallel pack runtime context type when `PackContext` already exists
- forcing runtime-only minimal fixture packs to declare every governance surface that full `PackContext` consumers need
- weakening real pack-contract validation or making malformed pack manifests silently pass
- reintroducing live `plan` assumptions into `core/**` test or runtime seams

## Task Set
- `task.mandatory_pack_context_loader_bootstrap.bootstrap_mandatory_pack_context_loader_bootstrap`: bootstrap, confirm, approve, execute, and close the initiative package
- `task.mandatory_pack_context_loader_bootstrap.centralize_effective_pack_context_bootstrap`: add the loader-owned effective pack context bootstrap and cache path
- `task.mandatory_pack_context_loader_bootstrap.rewire_pack_aware_runtime_neighbors`: route host, validation, runtime, and sync seams through the shared bootstrap path
- `task.mandatory_pack_context_loader_bootstrap.refresh_pack_context_invariant_docs`: update core-owned engineering and pack-authoring guidance so future work preserves the invariant
- `task.mandatory_pack_context_loader_bootstrap.validate_and_closeout`: run broad validation, verify copied-core behavior, and close the initiative cleanly
