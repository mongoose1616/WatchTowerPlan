---
trace_id: trace.lazy_planning_query_payload_emission
id: decision.lazy_planning_query_payload_emission_direction
title: Lazy Planning Query Payload Emission Direction Decision
summary: Records the initial direction decision for Lazy Planning Query Payload Emission.
type: decision_record
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

# Lazy Planning Query Payload Emission Direction Decision

## Record Metadata
- `Trace ID`: `trace.lazy_planning_query_payload_emission`
- `Decision ID`: `decision.lazy_planning_query_payload_emission_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.lazy_planning_query_payload_emission`
- `Linked Designs`: `design.features.lazy_planning_query_payload_emission`
- `Linked Implementation Plans`: `design.implementation.lazy_planning_query_payload_emission`
- `Updated At`: `2026-03-12T20:51:21Z`

## Summary
Records the initial direction decision for Lazy Planning Query Payload Emission.

## Decision Statement
Adopt a shared lazy JSON-emission helper for the high-cost planning query handlers so
human output skips payload construction while JSON output continues to use the existing
serializers unchanged.

## Trigger or Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Current Context and Constraints
- The repository's planning and initiative projections now carry enough nested data that
  eager JSON payload shaping is a real cost on human-mode queries.
- The existing serializer helpers are already the JSON payload authority and should remain
  the single shaping path.
- A repository-wide CLI refactor would be broader than this measured optimization needs.

## Applied References and Implications
- `docs/standards/engineering/python_workspace_standard.md`: Keeps the change scoped to
  the canonical Python CLI surface and requires standard workspace validation.
- `docs/standards/governance/task_handling_threshold_standard.md`: Requires a traced task
  cycle and explicit closeout for this non-trivial optimization.
- `foundation.engineering_design_principles`: Favors explicit, deterministic operator
  paths over hidden wasted work.

## Affected Surfaces
- core/python/src/watchtower_core/cli/
- core/python/tests/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/

## Options Considered
### Option 1
- Add a shared lazy JSON-emission helper and apply it to `query planning`, `query
  initiatives`, and `query coordination`.
- Preserves one serializer authority path while removing wasted human-mode work.
- Leaves smaller handlers on the eager path until they demonstrate the same need.

### Option 2
- Keep `_print_payload()` unchanged and hand-roll format checks directly in each affected
  handler.
- Avoids adding a new shared helper.
- Spreads the same control-flow logic across multiple handlers and makes later reuse
  harder.

## Chosen Outcome
Choose Option 1. Add one shared lazy-emission helper and route the heavy planning query
handlers through it.

## Rationale and Tradeoffs
- This fixes the measured cost where it matters without widening the slice into an
  all-handler refactor.
- The helper keeps JSON shaping centralized, which reduces payload drift risk.
- The tradeoff is one additional helper in the CLI common layer, but it is small and
  directly reusable if adjacent handlers later show the same pattern.

## Consequences and Follow-Up Impacts
- The affected handlers will separate query execution from JSON payload shaping more
  explicitly.
- Adjacent query handlers remain candidates for the same optimization only if a later
  review shows comparable wasted work.

## Risks, Dependencies, and Assumptions
- Human coordination output has more branching than planning or initiatives, so regression
  coverage must protect both empty and non-empty result paths.

## References
- `docs/planning/prds/lazy_planning_query_payload_emission.md`
- `docs/planning/design/features/lazy_planning_query_payload_emission.md`
- `core/python/src/watchtower_core/cli/handler_common.py`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
