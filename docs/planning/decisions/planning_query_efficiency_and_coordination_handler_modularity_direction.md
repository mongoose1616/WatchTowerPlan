---
trace_id: trace.planning_query_efficiency_and_handler_modularity
id: decision.planning_query_efficiency_and_handler_modularity_direction
title: Planning Query Efficiency and Coordination Handler Modularity Direction Decision
summary: Records the initial direction decision for Planning Query Efficiency and
  Coordination Handler Modularity.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T23:32:17Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_projection_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_family.py
- core/python/src/watchtower_core/repo_ops/query/common.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/control_plane/models/planning_catalog.py
- docs/commands/core_python/
---

# Planning Query Efficiency and Coordination Handler Modularity Direction Decision

## Record Metadata
- `Trace ID`: `trace.planning_query_efficiency_and_handler_modularity`
- `Decision ID`: `decision.planning_query_efficiency_and_handler_modularity_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.planning_query_efficiency_and_handler_modularity`
- `Linked Designs`: `design.features.planning_query_efficiency_and_handler_modularity`
- `Linked Implementation Plans`: `design.implementation.planning_query_efficiency_and_handler_modularity`
- `Updated At`: `2026-03-13T23:32:17Z`

## Summary
Records the initial direction decision for Planning Query Efficiency and Coordination Handler Modularity.

## Decision Statement
Pursue a bounded runtime-layer redesign: unify the duplicated planning or initiative or
coordination query-search mechanics and split the concentrated coordination-query handler
hotspot behind compatibility facades, while keeping the governed planning catalog and
query contracts stable in this trace.

## Trigger or Source Request
- Comprehensive redesign review for planning-surface/query-model efficiency and the remaining concentrated coordination-query handler family under one stable trace.

## Current Context and Constraints
- The umbrella refactor review explicitly left this redesign boundary open after fixing the
  broader process regression.
- The live repository still has a `591`-line coordination-query handler hotspot plus
  duplicated query-search mechanics across planning, initiative, and coordination query
  services.
- The governed planning catalog is large, but prior lazy payload work already removed the
  last confirmed eager-serialization performance issue from the human path.
- Adding a new governed planning summary family would increase schema, sync, docs, and
  validation surface area in the exact area the umbrella review just stabilized.

## Applied References and Implications
- `docs/planning/design/implementation/refactor_umbrella_regression_and_growth_control.md`: the accepted umbrella direction was to stop disconnected refactor slices and only open a
  new redesign effort when a still-live root boundary remained.
- `docs/planning/prds/lazy_planning_query_payload_emission.md`: the eager human-path
  planning payload problem is already fixed, so the remaining issue is structural
  duplication and hotspot concentration.
- `docs/planning/design/features/query_family_source_surface_alignment.md`: earlier work
  explicitly deferred splitting `query_coordination_handlers.py` unless a later pass
  proved it remained a live issue. This trace is that later pass.

## Affected Surfaces
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_projection_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_family.py
- core/python/src/watchtower_core/repo_ops/query/common.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/control_plane/models/planning_catalog.py
- docs/commands/core_python/

## Options Considered
### Option 1
- Redesign the governed planning model by adding a new planning-summary index or reshaping
  the planning catalog.
- Strength: could reduce future artifact size directly.
- Tradeoff: adds governed surface and schema churn before the current evidence proves that
  the data model, rather than the runtime query layer, is the root problem.

### Option 2
- Keep the governed planning artifacts stable and redesign the runtime/query layer only:
  shared projection-search helpers plus focused handler modules behind compatibility
  facades.
- Strength: addresses the confirmed duplication and concentration with lower drift risk and
  no new governed family.
- Tradeoff: does not shrink already-committed planning corpus size by itself.

## Chosen Outcome
Accept Option 2. This trace will redesign the runtime/query layer, not the governed
planning catalog shape.

## Rationale and Tradeoffs
- The current evidence shows that the live root issue is duplicated runtime search logic
  and a concentrated handler boundary, not a proven failure in the governed planning
  catalog contract.
- A runtime-layer redesign addresses the same theme while avoiding new indexes, schemas,
  and machine-readable surfaces in an already large planning corpus.
- If repeated confirmation passes still find the governed planning model itself to be the
  bottleneck after this redesign lands, that should become a new explicitly justified
  follow-up rather than being conflated with the current hotspot.

## Consequences and Follow-Up Impacts
- Query services will share a new internal search-helper layer.
- The coordination-query handler hotspot will be split into smaller focused modules.
- Command docs and direct consumer tests will need reconciliation because handler ownership
  becomes more granular.
- No new governed planning artifact family should appear in this trace.

## Risks, Dependencies, and Assumptions
- The redesign depends on preserving current import compatibility and command behavior.
- The redesign assumes the existing planning catalog, initiative index, and coordination
  index remain the correct governed authorities for this trace.
- A later follow-up may still be needed if confirmation work proves the data-model layer is
  the next bottleneck after the runtime redesign lands.

## References
- docs/planning/prds/lazy_planning_query_payload_emission.md
- docs/planning/design/features/query_family_source_surface_alignment.md
- docs/planning/design/implementation/refactor_umbrella_regression_and_growth_control.md
