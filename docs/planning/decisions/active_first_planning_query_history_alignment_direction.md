---
trace_id: trace.active_first_planning_query_history_alignment
id: decision.active_first_planning_query_history_alignment_direction
title: Active-First Planning Query History Alignment Direction Decision
summary: Records the initial direction decision for Active-First Planning Query History
  Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T20:42:11Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- docs/commands/core_python/
- docs/planning/
---

# Active-First Planning Query History Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.active_first_planning_query_history_alignment`
- `Decision ID`: `decision.active_first_planning_query_history_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.active_first_planning_query_history_alignment`
- `Linked Designs`: `design.features.active_first_planning_query_history_alignment`
- `Linked Implementation Plans`: `design.implementation.active_first_planning_query_history_alignment`
- `Updated At`: `2026-03-13T20:42:11Z`

## Summary
Records the initial direction decision for Active-First Planning Query History Alignment.

## Decision Statement
Adopt an active-default browse policy for filterless `watchtower-core query planning` and `watchtower-core query initiatives` calls, expose the applied default in their JSON payloads, and keep explicit trace and historical lookup unchanged through explicit filters.

## Trigger or Source Request
- Do another comprehensive internal project review for refactor under one stable planning-navigation theme until no new actionable issues remain.
- Address the remaining active-vs-history planning navigation drift identified by the March 13, 2026 refactor audit.

## Current Context and Constraints
- The authority map, planning README, and initiative-family README already frame planning navigation as active-first: coordination is the start-here surface, planning is the deep trace view, and initiatives is the compact family or history view.
- The current runtime behavior still lets unfiltered planning and initiative queries fall straight into completed-history rows when no active initiatives exist, which conflicts with the documented navigation model.
- Known-trace and explicit historical lookup must remain reliable because completed traces are still durable repository history, not deprecated data.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): favors explicit route-first behavior and visible defaults over implicit history browsing.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires human and machine surfaces that claim the same navigation model to stay synchronized in one change set.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): keeps deep-planning and initiative-family history accessible after the default changes.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): constrains the compact initiative-family view and preserves explicit status semantics.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- docs/commands/core_python/
- docs/planning/

## Options Considered
### Option 1
- Change only docs and leave the runtime query behavior untouched.
- Lowest implementation risk.
- Rejected because it would preserve the documented-versus-runtime mismatch that the discovery pass confirmed.

### Option 2
- Apply the `active` default only for filterless browse calls, keep query services generic, publish the applied default in JSON payloads, and align docs and tests around that boundary.
- Fixes the active-vs-history drift without removing explicit history access or changing artifact schemas.
- Requires careful handler logic so trace-specific and explicitly historical requests are not accidentally filtered away.

### Option 3
- Require explicit `--trace-id` or `--initiative-status` for all planning and initiative queries.
- Maximizes explicitness.
- Rejected because it is stricter than the repository guidance requires and would reduce usability for normal current-state browse flows.

## Chosen Outcome
Accept Option 2. The refactor will keep the initiative index and planning catalog unchanged, add the active-default browse policy only at the CLI entrypoint layer for filterless calls, emit `default_initiative_status` when that default applies, and refresh the planning navigation docs and tests to match.

## Rationale and Tradeoffs
- The confirmed issue is a navigation and entrypoint-policy mismatch, not a defect in the indexes, loaders, or query services themselves.
- A handler-layer default mirrors the existing coordination pattern and keeps the lower-level query services reusable and explicit.
- The main tradeoff is that truly filterless history browsing will now require explicit status filters, but that is desirable because the repository already documents history lookup as an explicit path.

## Consequences and Follow-Up Impacts
- `query planning` and `query initiatives` will become active-first when invoked as pure browse commands.
- Command docs and planning READMEs must describe the changed default and explicit history path in the same change set.
- Direct CLI planning-query regressions will need new coverage for filterless defaults plus preserved explicit historical lookup.

## Risks, Dependencies, and Assumptions
- Assumes the bounded issue can be resolved without changing the initiative index or planning catalog artifacts themselves.
- Risks suppressing intentional history browsing if the default is applied beyond truly filterless calls.
- Depends on targeted live-query probes and regression tests to prove both current-state and history paths remain correct.

## References
- March 13, 2026 refactor audit
- [active_first_planning_query_history_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/active_first_planning_query_history_alignment.md)
