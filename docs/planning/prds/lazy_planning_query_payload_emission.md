---
trace_id: trace.lazy_planning_query_payload_emission
id: prd.lazy_planning_query_payload_emission
title: Lazy Planning Query Payload Emission PRD
summary: Remove unnecessary full JSON payload construction from the human planning,
  initiative, and coordination query paths so large planning projections do not pay
  serialization cost unless JSON output is requested, without changing payload fidelity.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T20:51:21Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/tests/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
---

# Lazy Planning Query Payload Emission PRD

## Record Metadata
- `Trace ID`: `trace.lazy_planning_query_payload_emission`
- `PRD ID`: `prd.lazy_planning_query_payload_emission`
- `Status`: `active`
- `Linked Decisions`: `decision.lazy_planning_query_payload_emission_direction`
- `Linked Designs`: `design.features.lazy_planning_query_payload_emission`
- `Linked Implementation Plans`: `design.implementation.lazy_planning_query_payload_emission`
- `Updated At`: `2026-03-12T20:51:21Z`

## Summary
Remove unnecessary full JSON payload construction from the human planning, initiative, and coordination query paths so large planning projections do not pay serialization cost unless JSON output is requested, without changing payload fidelity.

## Problem Statement
The planning-oriented CLI query handlers still build their full JSON payloads before
they check whether the caller actually requested JSON output. That is cheap for small
surfaces, but it is materially wasteful for the repository's largest planning
projections.

Direct instrumentation of the live handlers showed that:

- `watchtower-core query planning` in human mode still invoked
  `serialize_planning_catalog_entry()` once per returned result. A bounded `--limit 3`
  call performed `3` serializer calls before printing the human summary.
- `watchtower-core query initiatives` in human mode still invoked
  `serialize_initiative_entry()` once per returned result. A bounded `--limit 3` call
  performed `3` serializer calls before printing the human summary.
- `watchtower-core query coordination` follows the same eager payload pattern for the
  initiative results path and therefore pays the same cost whenever the human path
  returns active entries.

Those serializers expand nested planning sections, active task summaries, IDs, and
related-path payloads that the human path never uses. As the planning corpus grows, that
becomes unnecessary CPU and allocation work on the default operator path.

## Goals
- Stop the human `query planning` path from building serialized planning-catalog result
  payloads.
- Stop the human `query initiatives` and non-empty human `query coordination` paths from
  building serialized initiative payloads.
- Preserve current JSON output fidelity and current human-readable output.

## Non-Goals
- Redesign the planning catalog, initiative index, or coordination index data model.
- Change CLI flags, output schemas, or human text formatting beyond removing wasted
  internal work.
- Refactor every CLI handler in the repository in the same slice.

## Requirements
- `req.lazy_planning_query_payload_emission.001`: Human `watchtower-core query planning`
  must not invoke the planning-catalog serializer unless `--format json` is requested.
- `req.lazy_planning_query_payload_emission.002`: Human `watchtower-core query
  initiatives` and human `watchtower-core query coordination` must not invoke initiative
  serialization unless `--format json` is requested.
- `req.lazy_planning_query_payload_emission.003`: JSON output for the affected commands
  must remain unchanged.
- `req.lazy_planning_query_payload_emission.004`: The change must be protected with
  regressions, measured on the affected human paths, and closed with the normal
  repository validation baseline plus a clean adjacent-surface follow-up review.

## Acceptance Criteria
- `ac.lazy_planning_query_payload_emission.001`: The trace publishes the authored planning
  chain, accepted direction decision, refreshed acceptance contract, refreshed evidence
  artifact, and a bounded closed task set for this optimization slice.
- `ac.lazy_planning_query_payload_emission.002`: Human `query planning` performs zero
  planning-entry serializer calls on the measured path.
- `ac.lazy_planning_query_payload_emission.003`: Human `query initiatives` and non-empty
  human `query coordination` perform zero initiative-entry serializer calls on the
  measured path, while JSON output remains intact.
- `ac.lazy_planning_query_payload_emission.004`: Targeted regressions, repository
  validation, tests, mypy, and ruff all pass after the change.
- `ac.lazy_planning_query_payload_emission.005`: A follow-up review of adjacent CLI query
  and planning-projection surfaces finds no additional actionable issues.

## Risks and Dependencies
- A lazy-emission change can accidentally drift the JSON payload shape if the handlers
  fork their payload logic instead of sharing the same serializer path.
- The slice depends on keeping the optimization bounded to the high-cost planning query
  handlers so it does not grow into a broad CLI refactor.

## References
- `core/python/src/watchtower_core/cli/handler_common.py`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py`
- `core/python/tests/unit/test_route_and_query_handlers.py`
