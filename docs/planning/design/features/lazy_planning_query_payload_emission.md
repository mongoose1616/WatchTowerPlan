---
trace_id: trace.lazy_planning_query_payload_emission
id: design.features.lazy_planning_query_payload_emission
title: Lazy Planning Query Payload Emission Feature Design
summary: Defines the technical design boundary for Lazy Planning Query Payload Emission.
type: feature_design
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

# Lazy Planning Query Payload Emission Feature Design

## Record Metadata
- `Trace ID`: `trace.lazy_planning_query_payload_emission`
- `Design ID`: `design.features.lazy_planning_query_payload_emission`
- `Design Status`: `active`
- `Linked PRDs`: `prd.lazy_planning_query_payload_emission`
- `Linked Decisions`: `decision.lazy_planning_query_payload_emission_direction`
- `Linked Implementation Plans`: `design.implementation.lazy_planning_query_payload_emission`
- `Updated At`: `2026-03-12T20:51:21Z`

## Summary
Defines the technical design boundary for Lazy Planning Query Payload Emission.

## Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope and Feature Boundary
- Covers the heavy planning-oriented CLI query handlers that currently build JSON payloads
  before checking `args.format`: `query planning`, `query initiatives`, and `query
  coordination`.
- Covers the shared handler helper needed to emit JSON lazily without duplicating
  serializer logic.
- Excludes unrelated lightweight handlers whose payload shaping is not materially costly
  in the current repository.

## Current-State Context
- The planning catalog and initiative projections now carry nested summaries for PRDs,
  decisions, designs, tasks, acceptance contracts, evidence, owners, and next-step
  coordination metadata.
- `_print_payload()` only decides whether JSON should be printed after the handler has
  already built the payload object, so human-mode handlers still pay serializer cost for
  data they never print.
- Measured instrumentation showed `3` unnecessary serializer calls on bounded human
  `query planning` and `query initiatives` runs with `--limit 3`.

## Foundations References Applied
- `foundation.engineering_design_principles`: Favors deterministic, explicit command
  behavior without hidden wasted work on default operator paths.
- `foundation.repository_standards_posture`: Requires same-change alignment between
  runtime behavior, validation coverage, and traced governance artifacts.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: Keeps the change inside the
  canonical Python workspace and validates it with the standard command set.
- `docs/standards/governance/task_handling_threshold_standard.md`: This non-trivial traced
  optimization requires explicit task handling and trace-linked closeout.

## Design Goals and Constraints
- Remove wasted payload shaping from the human planning query paths.
- Keep JSON output behavior identical by continuing to use the same serializers when JSON
  is requested.
- Avoid a broad CLI-wide rewrite; only the heavy planning-oriented handlers should change
  in this slice.

## Options Considered
### Option 1
- Add a small lazy JSON-emission helper and switch the affected handlers to build payloads
  only when `args.format == "json"`.
- Keeps the serializer path centralized and reduces handler duplication.
- Leaves other handlers unchanged until they demonstrate the same scale pressure.

### Option 2
- Inline `if args.format == "json"` branches separately in each affected handler without a
  shared helper.
- Minimizes helper changes.
- Repeats the same control-flow pattern and makes later adoption across adjacent handlers
  noisier.

## Recommended Design
### Architecture
- Extend the shared CLI handler utilities with a lazy JSON-emission path that accepts a
  payload factory.
- Route `query planning`, `query initiatives`, and `query coordination` through that
  helper so human output skips payload construction entirely.
- Preserve the existing serializer modules as the sole source for JSON payload shaping.

### Data and Interface Impacts
- No schema, contract, or CLI flag changes.
- The affected command payloads stay byte-for-byte compatible in JSON mode.
- Human output text stays unchanged while internal serializer calls drop to zero on the
  measured human paths.

### Execution Flow
1. The handler resolves its query results normally.
2. If JSON output is requested, the handler invokes the lazy emission helper, which then
   builds the payload through the existing serializers and prints it.
3. If human output is requested, the helper returns immediately and the handler prints the
   human summary without ever shaping the JSON payload.

### Invariants and Failure Cases
- JSON mode must continue to include the same fields, nested structures, and ordering as
  before the optimization.
- Human mode must not accidentally suppress empty-state messaging or recent-closeout
  summaries while skipping payload construction.

## Affected Surfaces
- core/python/src/watchtower_core/cli/
- core/python/tests/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/

## Design Guardrails
- The optimization must preserve the existing serializer functions as the JSON authority.
- The slice must stay bounded to the high-cost planning/initiative handler paths instead
  of turning into a repository-wide CLI refactor.

## Risks
- If the helper is wired incorrectly, human-mode coordination output could miss its empty
  or recent-closeout reporting.

## References
- `docs/planning/prds/lazy_planning_query_payload_emission.md`
- `core/python/src/watchtower_core/cli/handler_common.py`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py`
