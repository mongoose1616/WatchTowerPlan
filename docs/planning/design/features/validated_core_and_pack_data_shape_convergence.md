---
trace_id: trace.validated_core_pack_data_shape_convergence
id: design.features.validated_core_pack_data_shape_convergence
title: Validated Core and Pack Data Shape Convergence Feature Design
summary: Defines the technical design boundary for Validated Core and Pack Data Shape
  Convergence.
type: feature_design
status: draft
owner: repository_maintainer
updated_at: '2026-03-16T04:32:27Z'
audience: shared
authority: authoritative
---

# Validated Core and Pack Data Shape Convergence Feature Design

## Record Metadata
- `Trace ID`: `trace.validated_core_pack_data_shape_convergence`
- `Design ID`: `design.features.validated_core_pack_data_shape_convergence`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.validated_core_pack_data_shape_convergence`
- `Linked Decisions`: `decision.validated_core_pack_data_shape_convergence_direction`
- `Linked Implementation Plans`: `design.implementation.validated_core_pack_data_shape_convergence`
- `Updated At`: `2026-03-16T04:32:27Z`

## Summary
Defines the technical design boundary for Validated Core and Pack Data Shape Convergence.

## Source Request
- Review STEP1_FINAL and convert the current repo data shape toward that pack-ready standard.

## Scope and Feature Boundary
- This design covers the validated startup boundary between shared core and a pack-shaped repository surface, including the runtime manifest, typed loader access, and workspace-prefix injection.
- This design intentionally excludes the later migration of all repo-local planning families into generic pack artifacts and excludes pack-specific execution adapters such as shell, SSH, and airgapped transports.

## Current-State Context
- `core/control_plane` already publishes generic pack-facing schemas for work notes, manifests, extraction outputs, promoted knowledge, promotion records, and pack-local indexes.
- `watchtower_core.control_plane.workspace` and `watchtower_core.control_plane.loader` still hardcode the current repository's logical workspace prefixes and named planning-family loader methods, which keeps startup behavior WatchTowerPlan-led instead of contract-led.

## Foundations References Applied
- `STEP1_FINAL`: Sets the future standard that packs own their schemas, runtime state, artifact families, and semantic meaning while shared core owns generic validation, query, sync, and indexing machinery.

## Internal Standards and Canonical References Applied
- `core/control_plane/README.md`: Shared core must keep authored schemas, manifests, registries, contracts, policies, indexes, and ledgers under `core/control_plane` without turning the tree into pack-owned mutable runtime storage.
- `docs/planning/design/features/core_export_ready_architecture.md`: The repository already committed to injected workspace boundaries plus a repo-local `repo_ops` layer; this design extends that direction by making startup configuration explicit.

## Design Goals and Constraints
- Make the reusable startup contract explicit before wider data-family migration begins.
- Keep the implementation additive and fail-closed so current repo behavior remains intact while the new boundary lands.
- Preserve the rule that pack-specific semantics and execution adapters stay outside shared core.

## Options Considered
### Option 1
- Move current planning data, registries, and indexes directly to new pack families in one large refactor.
- Reaches the future shape faster on paper.
- Too risky because startup, query, sync, validation, and planning semantics would all move at once.

### Option 2
- Introduce a validated runtime manifest and consume it from shared core before migrating additional families.
- Creates a reusable contract boundary that later slices can build on safely.
- Leaves planning-specific typed models and loader methods in place for one more transition phase.

## Recommended Design
### Architecture
- Add a governed `pack_runtime_manifest` artifact family under `core/control_plane/schemas/artifacts/` and `core/control_plane/manifests/`.
- Expose that artifact through a typed `PackRuntimeManifest` model and `ControlPlaneLoader.load_pack_runtime_manifest()`.
- Extend `WorkspaceConfig` so logical control-plane and Python-workspace prefixes can be loaded from the runtime manifest rather than only from hardcoded defaults.
- Keep current planning, query, sync, closeout, and environment behavior under `repo_ops` until later slices replace repo-local data families with pack-facing ones.

### Data and Interface Impacts
- New artifact schema and manifest for the pack-runtime boundary.
- Updated schema catalog and manifest directory inventory.
- New typed control-plane model surface for the runtime manifest.
- New workspace construction path that accepts a validated runtime manifest document.

### Execution Flow
1. Shared core loads the schema catalog and validates the pack-runtime manifest as a governed artifact.
2. Callers build `WorkspaceConfig` from the runtime manifest when they want manifest-declared logical roots instead of default repository assumptions.
3. Existing repo-local orchestration continues to run on top of that injected workspace while later slices move pack models, queries, and indexes toward the future standard.

### Invariants and Failure Cases
- The repository must remain valid and queryable when the new manifest exists but is not yet the only startup path.
- Invalid or incomplete runtime-manifest documents must fail clearly instead of silently falling back to guessed pack semantics.

## Affected Surfaces
- `core/control_plane/schemas/artifacts/`
- `core/control_plane/manifests/`
- `core/control_plane/registries/schema_catalog/schema_catalog.v1.json`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/tests/unit/`
- `docs/planning/`

## Design Guardrails
- Do not move current repo-local planning semantics into shared core in this slice.
- Do not treat the pack-runtime manifest as a replacement for schema catalog, validator registry, or other existing core registries; it is a startup boundary, not a new monolithic authority.

## Risks
- The manifest could become a dumping ground for pack semantics if future slices fail to keep family meaning, validators, and environment behavior in pack-local code.
- The runtime contract is only the first step; later slices still need to reduce planning-specific typed exports and named loader methods.

## References
- /home/j/mvp_reference/STEP1_FINAL.md
