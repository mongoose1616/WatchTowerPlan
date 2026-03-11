---
trace_id: trace.derived_projection_status_semantics
id: design.features.derived_projection_status_semantics
title: Derived Projection Status Semantics Alignment Feature Design
summary: Defines the technical design boundary for Derived Projection Status Semantics
  Alignment.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T03:29:01Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/indexes/initiatives/
- core/control_plane/indexes/coordination/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/standards/
---

# Derived Projection Status Semantics Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.derived_projection_status_semantics`
- `Design ID`: `design.features.derived_projection_status_semantics`
- `Design Status`: `active`
- `Linked PRDs`: `prd.derived_projection_status_semantics`
- `Linked Decisions`: `decision.derived_projection_status_semantics_direction`
- `Linked Implementation Plans`: `design.implementation.derived_projection_status_semantics`
- `Updated At`: `2026-03-11T03:29:01Z`

## Summary
Defines the technical design boundary for Derived Projection Status Semantics Alignment.

## Source Request
- Follow-up from SUMMARY.md verification after planning-authority closeout.

## Scope and Feature Boundary
- Covers the initiative-index entry contract and the coordination-index embedded initiative-entry contract.
- Covers the sync services, typed models, query handlers, command docs, and standards that expose or explain those derived initiative-family entries.
- Excludes traceability-index field renames and unrelated lifecycle fields in other artifact families.

## Current-State Context
- The canonical deep-planning path now lives in the planning catalog and is discoverable through the authority map.
- `watchtower-core query initiatives` and `watchtower-core query coordination` still expose derived initiative entries with `status` plus `initiative_status`, which creates a misleading machine contract for closed initiatives.
- The initiative and coordination indexes are both derived projections, so they can be made more explicit without changing the underlying traceability source model.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): explicit field naming should make machine authority and lifecycle semantics easier to consume without extra inference.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): companion schemas, docs, code, and tests need to move together when a governed contract changes.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): this work stays inside the governed core and planning substrate rather than expanding into future product-pack behavior.

## Internal Standards and Canonical References Applied
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): the initiative index is the primary contract being clarified in this slice.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): the coordination index inherits the initiative-entry contract and must remain aligned with it.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): the canonical planning path already uses explicit status naming and sets the direction for the derived projection cleanup.

## Design Goals and Constraints
- Make lifecycle meaning obvious in derived initiative-family payloads.
- Keep the change local to initiative-family projections instead of reopening root artifact or traceability contracts.
- Preserve one clear distinction:
  - `artifact_status` describes the lifecycle of the projected governing artifact.
  - `initiative_status` describes the initiative closeout outcome.
  - `task_status` continues to describe task execution state.

## Options Considered
### Option 1
- Keep the current `status` field and add more documentation about how it differs from `initiative_status`.
- Lowest implementation cost and no contract migration.
- Leaves the ambiguous payload shape in place for machine consumers and keeps the summary finding valid.

### Option 2
- Rename the per-entry field in initiative-family projections from `status` to `artifact_status` while leaving root artifact `status` unchanged.
- Removes the ambiguity directly and matches the explicit field naming already used in the planning catalog.
- Requires schema, sync, model, query, doc, and test updates in one bounded contract change.

## Recommended Design
### Architecture
- The initiative-index schema becomes the source of truth for the entry-field rename from `status` to `artifact_status`.
- The coordination-index schema inherits the same entry shape, so embedded initiative entries become explicit automatically once the shared initiative-entry contract changes.
- Sync services emit `artifact_status` for derived initiative entries, and typed models plus CLI query handlers read and print the renamed field consistently.

### Data and Interface Impacts
- `core/control_plane/schemas/artifacts/initiative_index.v1.schema.json`
- `core/control_plane/schemas/artifacts/coordination_index.v1.schema.json`
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`
- `core/control_plane/indexes/coordination/coordination_index.v1.json`
- `core/python/src/watchtower_core/control_plane/models/coordination.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
- `core/python/src/watchtower_core/repo_ops/query/initiatives.py`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- initiative and coordination command docs, standards, and tests

### Execution Flow
1. Rename the initiative-entry schema field and update all derived artifact producers that materialize initiative-family entries.
2. Update typed loaders, query output handlers, docs, and tests to consume and describe `artifact_status`.
3. Rebuild derived artifacts and verify that closed-initiative payloads now publish explicit lifecycle semantics without regressing coordination behavior.

### Invariants and Failure Cases
- Root artifact documents for the initiative and coordination indexes keep their top-level lifecycle `status` field unchanged.
- Traceability remains authoritative for initiative closeout state and still publishes `initiative_status` separately.
- Validation must fail closed if a derived initiative entry still uses the old `status` field after the schema change.

## Affected Surfaces
- core/control_plane/indexes/initiatives/
- core/control_plane/indexes/coordination/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/standards/

## Design Guardrails
- Do not keep both `status` and `artifact_status` on initiative-family entries; the point of this slice is to remove ambiguity rather than add aliases.
- Do not rename task-entry or traceability-entry lifecycle fields in this initiative.

## Risks
- Any local consumer expecting entry-level `status` in initiative-family JSON will need to move with this repository change.
- The coordination index depends on the initiative-entry schema shape, so the sync and validation updates must land together.

## References
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md)
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md)
