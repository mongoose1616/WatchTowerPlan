---
trace_id: trace.planning_query_efficiency_and_handler_modularity
id: prd.planning_query_efficiency_and_handler_modularity
title: Planning Query Efficiency and Coordination Handler Modularity PRD
summary: Reviews and hardens the planning query model and coordination-query handler
  family so planning lookup stays efficient without adding new disconnected refactor
  slices or weakening query fidelity.
type: prd
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

# Planning Query Efficiency and Coordination Handler Modularity PRD

## Record Metadata
- `Trace ID`: `trace.planning_query_efficiency_and_handler_modularity`
- `PRD ID`: `prd.planning_query_efficiency_and_handler_modularity`
- `Status`: `active`
- `Linked Decisions`: `decision.planning_query_efficiency_and_handler_modularity_direction`
- `Linked Designs`: `design.features.planning_query_efficiency_and_handler_modularity`
- `Linked Implementation Plans`: `design.implementation.planning_query_efficiency_and_handler_modularity`
- `Updated At`: `2026-03-13T23:32:17Z`

## Summary
Reviews and hardens the planning query model and coordination-query handler family so planning lookup stays efficient without adding new disconnected refactor slices or weakening query fidelity.

## Problem Statement
The umbrella refactor review closed the process-level regression that kept spawning
disconnected same-theme traces, but it intentionally left one redesign boundary open:
the planning/coordination query layer. The live repository still shows two same-theme
pressure points in that boundary.

- The query-model layer duplicates structured filter and ranking logic across
  `repo_ops/query/initiatives.py`, `repo_ops/query/planning.py`, and
  `repo_ops/query/coordination.py`, even though those services search adjacent
  projections with nearly the same trace, status, owner, and query semantics.
- The runtime coordination-query handler family remains concentrated in
  `core/python/src/watchtower_core/cli/query_coordination_handlers.py` at `591` lines,
  with `query_coordination_family.py` at `392` lines, even after earlier lazy-payload
  and source-surface fixes.

The planning surface itself is also large. The current planning corpus contains `439`
planning documents, `200` closed task files, and `56` acceptance contracts plus `56`
validation-evidence ledgers. The current derived planning catalog is `1092237` bytes,
compared with `295669` bytes for the initiative index and `295254` bytes for the
traceability index. A single `query planning --trace-id` JSON response is about `18321`
bytes, compared with `5669` bytes for `query coordination`.

Those measurements do not yet prove that the governed planning catalog schema itself is
wrong. They do show that the runtime query layer and handler boundary are the current
high-leverage redesign target if we want better efficiency and maintainability without
adding another round of disconnected refactor work or expanding governed artifact
families unnecessarily.

## Goals
- Remove duplicated structured search mechanics from the planning, initiative, and
  coordination query services.
- Reduce the concentration of the coordination-query handler boundary while preserving
  import compatibility and current CLI behavior.
- Keep planning-query efficiency improvements inside the runtime/query layer unless the
  review proves that the governed planning catalog shape itself is the root cause.
- Preserve capability, fidelity, determinism, output contracts, and performance.

## Non-Goals
- Redesigning the planning-catalog schema or introducing a new governed summary index in
  this trace.
- Changing existing query flags, payload schemas, or human-readable command behavior.
- Reopening already-closed refactor slices that this redesign can consume as settled
  inputs.
- Flattening traceability, initiative coordination, or acceptance/evidence governance
  into simpler but less explicit surfaces.

## Requirements
- `req.planning_query_efficiency_and_handler_modularity.001`: The trace must publish one
  coverage map and findings ledger for the redesign boundary spanning the planning
  catalog, initiative index, coordination index, query services, CLI handler family,
  docs, tests, and adjacent governed surfaces.
- `req.planning_query_efficiency_and_handler_modularity.002`: Planning, initiative, and
  coordination query services must share the duplicated common filter/ranking mechanics
  through one explicit runtime-layer abstraction while preserving existing search
  semantics and result ordering.
- `req.planning_query_efficiency_and_handler_modularity.003`: The concentrated
  coordination-query CLI handler surface must be split into smaller focused modules while
  preserving current handler imports or compatibility facades for existing internal
  consumers and tests.
- `req.planning_query_efficiency_and_handler_modularity.004`: Command docs, tests,
  trackers, indexes, and planning surfaces touched by the redesign must stay aligned in
  the same change set, and the trace must not introduce a new governed planning artifact
  family unless the review later proves it is necessary.
- `req.planning_query_efficiency_and_handler_modularity.005`: Targeted validation, full
  repository validation, repeated confirmation passes, and the final closeout state must
  show no new actionable issue under the same redesign theme.

## Acceptance Criteria
- `ac.planning_query_efficiency_and_handler_modularity.001`: The planning corpus for
  `trace.planning_query_efficiency_and_handler_modularity` contains the active PRD,
  accepted direction decision, active feature design, active implementation plan,
  acceptance contract, evidence ledger, bounded task chain, coverage map, and findings
  ledger for this redesign review.
- `ac.planning_query_efficiency_and_handler_modularity.002`: Initiative, planning, and
  coordination query services consume one shared search-helper layer for the duplicated
  trace/status/owner/query filtering mechanics, and targeted regressions prove their
  behavior remains stable.
- `ac.planning_query_efficiency_and_handler_modularity.003`: The coordination-query
  handler hotspot is split behind a compatibility facade, and direct handler, CLI, and
  command-doc consumers remain aligned.
- `ac.planning_query_efficiency_and_handler_modularity.004`: The trace closes without
  adding a new governed planning artifact family, and the final decision record explains
  why the runtime-layer redesign was chosen over a broader schema/index redesign.
- `ac.planning_query_efficiency_and_handler_modularity.005`: Targeted validation, full
  validation, repeated confirmation passes, and adversarial checks all pass on the final
  closed tree.

## Risks and Dependencies
- Splitting the handler hotspot can create source-surface drift unless command docs,
  compatibility facades, and direct consumer tests are updated together.
- A shared search-helper abstraction can accidentally flatten meaningful differences
  between initiative, coordination, and planning search semantics if the service-specific
  query-term boundaries are not kept explicit.
- The redesign depends on the earlier lazy payload-emission and active-first browse work
  remaining correct so this trace does not reopen already-solved performance issues.

## References
- docs/planning/prds/lazy_planning_query_payload_emission.md
- docs/planning/design/features/query_family_source_surface_alignment.md
- docs/planning/design/implementation/refactor_umbrella_regression_and_growth_control.md
