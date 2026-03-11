---
trace_id: trace.derived_projection_status_semantics
id: decision.derived_projection_status_semantics_direction
title: Derived Projection Status Semantics Alignment Direction Decision
summary: Records the decision to use explicit artifact_status naming for derived
  initiative and coordination projection entries.
type: decision_record
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

# Derived Projection Status Semantics Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.derived_projection_status_semantics`
- `Decision ID`: `decision.derived_projection_status_semantics_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.derived_projection_status_semantics`
- `Linked Designs`: `design.features.derived_projection_status_semantics`
- `Linked Implementation Plans`: `design.implementation.derived_projection_status_semantics`
- `Updated At`: `2026-03-11T03:29:01Z`

## Summary
Records the decision to use explicit artifact_status naming for derived initiative and coordination projection entries.

## Decision Statement
Use explicit `artifact_status` naming for derived initiative and coordination projection entries while keeping root artifact lifecycle `status` and traceability contracts unchanged.

## Trigger or Source Request
- Follow-up from SUMMARY.md verification after planning-authority closeout.

## Current Context and Constraints
- The canonical planning query path already uses explicit status semantics, but the derived initiative-family projections still expose an ambiguous per-entry `status` field.
- Closed initiatives therefore publish payloads that can read as contradictory to machine consumers even though the underlying repository state is correct.
- The change should stay bounded to the derived initiative-family projections so current traceability and closeout semantics do not churn unnecessarily.

## Applied References and Implications
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): the initiative-entry contract changes directly, so the schema, examples, sync output, and docs must land together.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): coordination inherits the initiative-entry shape and therefore needs the same explicit lifecycle field naming.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): the planning catalog already models explicit lifecycle naming and provides the precedent for this bounded projection cleanup.

## Affected Surfaces
- core/control_plane/indexes/initiatives/
- core/control_plane/indexes/coordination/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/standards/

## Options Considered
### Option 1
- Keep the current field name and clarify the distinction through docs and standards only.
- Avoids a contract migration for initiative-family JSON.
- Preserves the misleading machine payload and leaves the verified summary issue unresolved.

### Option 2
- Rename the entry-level field to `artifact_status` across initiative and coordination projections and update companion contracts together.
- Makes lifecycle meaning explicit and aligns the derived projections with the canonical planning catalog vocabulary.
- Requires synchronized schema, code, docs, and test updates.

## Chosen Outcome
Option 2 is accepted. Derived initiative-family entries will use `artifact_status`, while `initiative_status` remains the initiative-outcome field and root artifact `status` remains the lifecycle field for the index artifacts themselves.

## Rationale and Tradeoffs
- The ambiguity is in the published contract, so documentation-only clarification is not sufficient.
- Renaming the derived projection field resolves the issue at the point of machine consumption without reopening broader traceability semantics.
- The cost is a bounded contract change, but the repository owns both the schemas and the primary consumers, so the migration is manageable inside one initiative.

## Consequences and Follow-Up Impacts
- Initiative-index and coordination-index schemas, generated artifacts, typed models, query handlers, docs, and tests must be updated together.
- Query examples and standards must explain the distinction between root artifact `status`, entry-level `artifact_status`, and initiative-level `initiative_status`.
- Once the rename lands and validation passes, the trace can close without further default work.

## Risks, Dependencies, and Assumptions
- Any untracked downstream consumer of initiative-family JSON will need the renamed field.
- The decision assumes the planning catalog remains the preferred deep-planning machine path and that derived initiative-family views should follow its explicit naming model where practical.

## References
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
- [planning_authority_unification_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/planning_authority_unification_direction.md)
