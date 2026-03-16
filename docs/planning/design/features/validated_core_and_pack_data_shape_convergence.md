---
trace_id: trace.validated_core_pack_data_shape_convergence
id: design.features.validated_core_pack_data_shape_convergence
title: Validated Core and Pack Data Shape Convergence Feature Design
summary: Defines the technical design boundary for Validated Core and Pack Data Shape
  Convergence.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-16T05:47:10Z'
audience: shared
authority: authoritative
---

# Validated Core and Pack Data Shape Convergence Feature Design

## Record Metadata
- `Trace ID`: `trace.validated_core_pack_data_shape_convergence`
- `Design ID`: `design.features.validated_core_pack_data_shape_convergence`
- `Design Status`: `active`
- `Linked PRDs`: `prd.validated_core_pack_data_shape_convergence`
- `Linked Decisions`: `decision.validated_core_pack_data_shape_convergence_direction`
- `Linked Implementation Plans`: `design.implementation.validated_core_pack_data_shape_convergence`
- `Updated At`: `2026-03-16T05:47:10Z`

## Summary
Defines the technical design boundary for Validated Core and Pack Data Shape Convergence.

## Source Request
- Review STEP1_FINAL and convert the current repo data shape toward that pack-ready standard.

## Scope and Feature Boundary
- This design covers the validated startup boundary between shared core and WatchTowerPlan as a plan and implementation domain pack, centered on `pack_settings`, flat registries, typed loader access, and explicit classification of current repo-local data families.
- This design intentionally excludes the later migration of all repo-local planning families into generic pack artifacts and excludes pack-specific execution adapters such as shell, SSH, and airgapped transports.

## Current-State Context
- `core/control_plane` already publishes reusable schemas for pack settings, governed surfaces, work notes, extraction outputs, and artifact indexes.
- `watchtower_core.control_plane.loader` still carries repository-local assumptions, nested registry paths, and transition-era contracts that do not fit the future core-plus-domain-pack boundary cleanly.
- The repository also carries a large set of current planning indexes, evidence ledgers, and schema examples that are useful today but should not be mistaken for the reusable-core startup contract.

## Foundations References Applied
- `STEP1_FINAL`: Sets the future standard that packs own their schemas, runtime state, artifact families, and semantic meaning while shared core owns generic validation, query, sync, and indexing machinery.

## Internal Standards and Canonical References Applied
- `core/control_plane/README.md`: Shared core must keep authored schemas, manifests, registries, contracts, indexes, and ledgers under `core/control_plane` without turning the tree into pack-owned mutable runtime storage.
- `docs/planning/design/features/core_export_ready_architecture.md`: The repository already committed to injected workspace boundaries plus a repo-local `repo_ops` layer; this design extends that direction by making startup configuration explicit.

## Design Goals and Constraints
- Make the reusable startup contract explicit before wider data-family migration begins.
- Keep the implementation additive and fail-closed so current repo behavior remains intact while the new boundary lands.
- Distinguish current pack-local source artifacts and derived projections from the reusable-core load root so follow-on cleanup can delete old shapes instead of wrapping them.
- Preserve the rule that pack-specific semantics and execution adapters stay outside shared core.

## Options Considered
### Option 1
- Move current planning data, registries, and indexes directly to new pack families in one large refactor.
- Reaches the future shape faster on paper.
- Too risky because startup, query, sync, validation, and planning semantics would all move at once.

### Option 2
- Introduce a validated `pack_settings` load root and consume it from shared core before migrating additional families.
- Creates a reusable contract boundary that later slices can build on safely.
- Leaves planning-specific typed models and loader methods in place for one more transition phase.

## Recommended Design
### Architecture
- Use `pack_settings.json` as the governed load root and pair it with flat registry artifacts under `core/control_plane/registries/`.
- Expose those artifacts through typed pack-settings, registry, and PackContext loader APIs rather than through a standalone runtime-manifest bridge.
- Remove retired policy and prototype interface families instead of carrying them as compatibility shims.
- Keep current planning, query, sync, closeout, and environment behavior under `repo_ops` until later slices replace repo-local data families with pack-facing ones.

### Current-To-Future Surface Mapping
| Current Surface Family | Future Role |
|---|---|
| `docs/planning/**` | Pack-owned human source artifacts for the plan and implementation domain. |
| `core/control_plane/manifests/pack_settings.json` | Reusable-core load root for one domain pack. |
| `core/control_plane/registries/schema_catalog.json`, `validator_registry.json`, `governance_surface_map.json`, `path_pattern_registry.json`, `status_registry.json`, `actor_registry.json` | Retained reusable-core governance and validation surfaces that `PackContext` loads directly. |
| `core/control_plane/registries/authority_map.json`, `workflow_metadata_registry.json` | Current pack-owned governance metadata retained during transition; not yet the future generic pack artifact or workflow index model. |
| `core/control_plane/indexes/commands/`, `routes/`, `repository_paths/` | Derived helper indexes that support reusable-core lookup and routing behavior. |
| `core/control_plane/indexes/prds/`, `decisions/`, `design_documents/`, `tasks/`, `initiatives/`, `planning/`, `coordination/`, `traceability/` | Current plan-domain pack projections derived from local planning artifacts; they remain repo-local and are outside `PackContext`. |
| `the retired control-plane example corpus` | Transitional schema-proof fixtures; useful for current validation but not part of the pack load root. |
| `core/control_plane/ledgers/**` | Transitional pack-local history and evidence surfaces; retained for current governance flows but not part of the reusable-core contract. |

### Data and Interface Impacts
- New pack-settings-driven load root plus supporting registries for path patterns, statuses, actors, governance surfaces, validators, workflows, and schema lookup.
- Updated schema catalog and validator registry reflecting the reduced active contract set.
- Removed runtime-manifest, policy-catalog, release-policy, and retired prototype interface families.
- Explicit classification of current planning indexes as repo-local derived pack projections and of current examples or ledgers as transitional support surfaces rather than startup inputs.

### Execution Flow
1. Shared core loads `pack_settings.json` and the declared registries through the schema catalog.
2. `PackContext` materializes the retained governed surfaces that reusable core needs without depending on a separate runtime-manifest bridge.
3. Existing repo-local orchestration continues to run on top of that boundary while planning indexes, evidence, and fixtures stay explicit pack-local projections or support surfaces.
4. Later slices can replace those pack-local projections with newer pack artifact families without reopening the shared-core startup contract.

### Invariants and Failure Cases
- The repository must remain valid and queryable while legacy control-plane contracts are removed and the simplified pack-settings boundary becomes canonical.
- Invalid or incomplete pack-settings and registry documents must fail clearly instead of silently falling back to guessed domain-pack semantics.
- No current planner, validator, or query service may infer that examples or ledgers belong to `PackContext` just because they still exist under `core/control_plane`.

## Affected Surfaces
- `core/control_plane/schemas/artifacts/`
- `core/control_plane/manifests/`
- `core/control_plane/registries/schema_catalog.json`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/tests/unit/`
- `docs/planning/`

## Design Guardrails
- Do not move current repo-local planning semantics into shared core in this slice.
- Do not turn `pack_settings` into a monolithic authority blob; schema catalog, validator registry, and the remaining registries stay separate governed surfaces.

## Risks
- The load root could become a dumping ground for domain-pack semantics if future slices fail to keep family meaning, validators, and environment behavior in pack-local code.
- The contract cutover is only the first step; later slices still need to reduce planning-specific typed exports and named loader methods.

## References
- /home/j/mvp_reference/STEP1_FINAL.md
