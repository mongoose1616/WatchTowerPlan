---
trace_id: trace.planning_query_efficiency_and_handler_modularity
id: design.features.planning_query_efficiency_and_handler_modularity
title: Planning Query Efficiency and Coordination Handler Modularity Feature Design
summary: Defines the technical design boundary for Planning Query Efficiency and Coordination
  Handler Modularity.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T23:32:17Z'
audience: shared
authority: authoritative
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

# Planning Query Efficiency and Coordination Handler Modularity Feature Design

## Record Metadata
- `Trace ID`: `trace.planning_query_efficiency_and_handler_modularity`
- `Design ID`: `design.features.planning_query_efficiency_and_handler_modularity`
- `Design Status`: `active`
- `Linked PRDs`: `prd.planning_query_efficiency_and_handler_modularity`
- `Linked Decisions`: `decision.planning_query_efficiency_and_handler_modularity_direction`
- `Linked Implementation Plans`: `design.implementation.planning_query_efficiency_and_handler_modularity`
- `Updated At`: `2026-03-13T23:32:17Z`

## Summary
Defines the technical design boundary for Planning Query Efficiency and Coordination Handler Modularity.

## Source Request
- Comprehensive redesign review for planning-surface/query-model efficiency and the remaining concentrated coordination-query handler family under one stable trace.

## Scope and Feature Boundary
- Covers the coordination-query runtime handler family, the adjacent planning and
  initiative query services, the shared query helper layer they need, direct tests,
  command docs, and the planning/evidence surfaces required to close the redesign trace.
- Excludes changes to the governed planning-catalog schema, initiative-index schema,
  traceability model, or command payload contracts unless confirmation work later proves
  a runtime-layer redesign is insufficient.

## Current-State Context
- `query_coordination_handlers.py` remains a `591`-line hotspot that owns six coordination-
  oriented subcommands plus shared payload, empty-state, and default-browse helpers.
- `query_coordination_family.py` remains a `392`-line registrar for the same family.
- `repo_ops/query/initiatives.py` and `repo_ops/query/planning.py` both implement nearly
  identical trace/status/phase/owner filtering and query scoring, while
  `repo_ops/query/coordination.py` duplicates the same pattern over the compact
  coordination projection.
- The current governed planning catalog is large at `1092237` bytes, but earlier
  `lazy_planning_query_payload_emission` work already removed the eager JSON-serialization
  cost on the human path. The remaining confirmed design pressure is structural
  duplication and hotspot concentration, not the already-fixed eager payload issue.
- The repository already provides stable compatibility facades such as
  `cli/query_handlers.py`, so a bounded internal split can preserve current imports while
  letting the actual handlers move into focused modules.

## Foundations References Applied
- `docs/foundations/engineering_design_principles.md`: the redesign should remove
  duplicated machinery and over-concentrated runtime boundaries without flattening the
  explicit planning architecture.
- `docs/foundations/repository_standards_posture.md`: human-readable docs, tests, and
  machine-readable lookup surfaces must move together when runtime ownership changes.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: keeps the redesign inside the
  canonical Python workspace with the standard validation stack.
- `docs/standards/governance/traceability_standard.md`: requires the redesign trace to
  preserve explicit planning, task, acceptance, and closeout links.
- `docs/standards/documentation/command_md_standard.md`: command docs must keep current
  source-surface ownership aligned with the runtime modules.
- `docs/standards/data_contracts/command_index_standard.md`: machine-readable command
  discovery surfaces must stay aligned if runtime ownership changes become materially
  visible.

## Design Goals and Constraints
- Reduce duplicated query-model logic across planning, initiative, and coordination
  search services.
- Reduce the concentrated coordination-query handler boundary into smaller focused
  modules.
- Preserve current query arguments, payload schemas, result ordering, active-default
  browse semantics, and historical-lookup behavior.
- Do not add a new governed planning summary family unless runtime-layer redesign fails
  to resolve the confirmed issue cluster.

## Options Considered
### Option 1
- Introduce a new governed planning-summary index or reshape the planning catalog so query
  planning can read a smaller artifact.
- Strength: could reduce future planning-artifact size directly.
- Tradeoff: adds new schema/index/docs/tests/sync surface and increases governed surface
  area before the review proves the data model is the primary bottleneck.

### Option 2
- Keep the governed planning artifacts stable and redesign only the runtime/query layer:
  shared projection-search helpers plus focused coordination-query handler modules behind
  a compatibility facade.
- Strength: addresses the confirmed current duplication and hotspot pressure without
  expanding control-plane families or changing query contracts.
- Tradeoff: does not reduce already-committed planning artifact volume by itself.

## Recommended Design
### Architecture
- Add one shared query-projection helper module in `repo_ops/query/` for the common
  trace/status/phase/owner filtering, query scoring, and result limiting behavior used by
  planning, initiative, and coordination searches.
- Refactor `InitiativeQueryService`, `PlanningCatalogQueryService`, and
  `CoordinationQueryService` to delegate the shared mechanics to that helper while keeping
  service-specific query-term expansion explicit.
- Split `query_coordination_handlers.py` into focused runtime modules for planning or
  initiative or coordination results versus authority or task or trace handlers, and keep
  `query_coordination_handlers.py` as a compatibility facade that re-exports the current
  handler functions.
- Keep `query_coordination_family.py` as the authoritative family registrar for command
  ownership unless the redesign later proves that parser registration itself is the
  remaining hotspot.

### Data and Interface Impacts
- No query flags, human output, JSON payload schemas, or governed planning schemas change.
- Command docs that currently cite `query_coordination_handlers.py` as a source surface
  must be updated to the new focused handler modules where appropriate.
- Direct tests that import the legacy handler module continue to pass through the
  compatibility facade.

### Execution Flow
1. Query commands keep their current parser shape and handler names.
2. The focused handler modules call the relevant query service and use shared render or
   payload helpers instead of concentrating everything in one file.
3. The query services use the shared projection-search helper for the duplicated common
   filter and ranking logic while still providing service-specific search terms.
4. Command docs, tests, planning trackers, and evidence surfaces are refreshed in the same
   change set.

### Invariants and Failure Cases
- The default active-only browse semantics for `coordination`, `planning`, and
  `initiatives` must stay unchanged.
- The explicit historical lookup path through `--initiative-status` and `--trace-id` must
  stay unchanged.
- If the handler split is applied incorrectly, the compatibility facade or command docs can
  drift; the redesign must guard that with direct consumer regressions and command-doc
  reconciliation.

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

## Design Guardrails
- Keep service-specific query-term selection explicit. The shared helper should only own
  the common filter/ranking machinery, not flatten all projections into one generic
  opaque query object.
- Do not introduce a new planning schema, index, or query command in this trace unless a
  reopened confirmation pass proves the runtime-layer redesign is insufficient.

## Risks
- The main risk is under-correction: the redesign could split the handler file but leave
  enough duplicated search logic behind that the same theme reappears quickly.
- A secondary risk is over-correction: too much abstraction in the shared search helper
  could make the planning and initiative services harder to review instead of easier.

## References
- docs/planning/prds/lazy_planning_query_payload_emission.md
- docs/planning/design/features/query_family_source_surface_alignment.md
- docs/planning/design/implementation/refactor_umbrella_regression_and_growth_control.md
