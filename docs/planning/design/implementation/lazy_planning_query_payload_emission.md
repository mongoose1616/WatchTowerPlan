---
trace_id: trace.lazy_planning_query_payload_emission
id: design.implementation.lazy_planning_query_payload_emission
title: Lazy Planning Query Payload Emission Implementation Plan
summary: Breaks Lazy Planning Query Payload Emission into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-12T20:51:21Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/tests/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
---

# Lazy Planning Query Payload Emission Implementation Plan

## Record Metadata
- `Trace ID`: `trace.lazy_planning_query_payload_emission`
- `Plan ID`: `design.implementation.lazy_planning_query_payload_emission`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.lazy_planning_query_payload_emission`
- `Linked Decisions`: `decision.lazy_planning_query_payload_emission_direction`
- `Source Designs`: `design.features.lazy_planning_query_payload_emission`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-12T20:51:21Z`

## Summary
Breaks Lazy Planning Query Payload Emission into a bounded implementation slice.

## Source Request or Design
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope Summary
- Add a small lazy JSON-emission helper in the shared CLI handler utilities.
- Update the heavy planning-oriented query handlers to use the lazy helper for JSON mode
  and avoid payload shaping on human mode.
- Add regressions for human-mode laziness and JSON-mode fidelity on the touched commands.
- Excludes unrelated handlers outside the planning/initiative query family.

## Assumptions and Constraints
- The existing planning and initiative serializers remain the JSON payload authority.
- The human output text is already correct and should not change as part of this
  optimization.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: Constrains command
  execution, test, lint, and typecheck entrypoints.
- `docs/standards/governance/task_handling_threshold_standard.md`: Requires explicit
  traced task handling and closeout metadata for this non-trivial change.

## Proposed Technical Approach
- Add a helper such as a payload factory emitter in `handler_common.py` so handlers can
  defer payload construction until JSON mode is confirmed.
- Switch `_emit_initiative_query_results()`, `_run_query_coordination()`, and
  `_run_query_planning()` to the lazy path.
- Add unit tests that fail if the heavy serializers are invoked on human-mode paths and
  confirm JSON payloads still contain the expected fields.

## Work Breakdown
1. Update the shared CLI handler helper and the targeted planning-oriented query handlers
   to defer payload construction until JSON output is requested.
2. Add human-mode laziness regressions and JSON-mode fidelity coverage for the affected
   commands.
3. Measure the serializer-call reduction, refresh acceptance and evidence artifacts, and
   close the trace with full validation.

## Risks
- Coordination output has multiple human-only branches, so the helper integration must not
  disturb the empty-state and recent-closeout behavior.

## Validation Plan
- Run targeted query-handler tests that cover human-mode laziness and JSON-mode output.
- Run `uv run pytest -q`, `uv run mypy src/watchtower_core`, and `uv run ruff check .`.
- Run `uv run watchtower-core validate acceptance --trace-id trace.lazy_planning_query_payload_emission --format json`
  and final `uv run watchtower-core validate all --format json`.
- Record measured serializer-call counts for the affected human query paths in the
  validation evidence.

## References
- `docs/planning/design/features/lazy_planning_query_payload_emission.md`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/tests/unit/test_route_and_query_handlers.py`
