---
trace_id: trace.active_first_planning_query_history_alignment
id: design.features.active_first_planning_query_history_alignment
title: Active-First Planning Query History Alignment Feature Design
summary: Defines the technical design boundary for Active-First Planning Query History
  Alignment.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T20:42:11Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- docs/commands/core_python/
- docs/planning/
---

# Active-First Planning Query History Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.active_first_planning_query_history_alignment`
- `Design ID`: `design.features.active_first_planning_query_history_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.active_first_planning_query_history_alignment`
- `Linked Decisions`: `decision.active_first_planning_query_history_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.active_first_planning_query_history_alignment`
- `Updated At`: `2026-03-13T20:42:11Z`

## Summary
Defines the technical design boundary for Active-First Planning Query History Alignment.

## Source Request
- Do another comprehensive internal project review for refactor under one stable planning-navigation theme until no new actionable issues remain.
- Address the remaining active-vs-history planning navigation drift identified by the March 13, 2026 refactor audit.

## Scope and Feature Boundary
- Covers the active-vs-history behavior boundary for `watchtower-core query planning` and `watchtower-core query initiatives`, including their CLI registration, runtime handlers, structured output, and direct regression tests.
- Covers the companion planning navigation surfaces that explain or route those commands: `docs/planning/README.md`, `docs/planning/initiatives/README.md`, `docs/commands/core_python/watchtower_core_query_planning.md`, `docs/commands/core_python/watchtower_core_query_initiatives.md`, and adjacent query-family guidance when needed for coherence.
- Covers adjacent reviewed surfaces that constrain the slice but are expected to remain structurally unchanged: the authority map, initiative index, planning catalog, control-plane loader, and query services.
- Excludes schema changes, new query subcommands, planning-family consolidation, and broader command-family or workflow-family rationalization beyond this active-first navigation seam.

## Current-State Context
- `watchtower-core query authority --domain planning --format json` already distinguishes three roles clearly: `query coordination` for current state, `query planning` for one deep trace-linked planning record, and `query initiatives` for compact initiative-family or history browsing.
- `watchtower-core query coordination` already defaults `--initiative-status` to `active` and publishes `default_initiative_status` in JSON output, so its runtime behavior matches the authority guidance and current-state README notes.
- `watchtower-core query planning --format json` and `watchtower-core query initiatives --format json` currently return completed traces when invoked without a trace ID or explicit status, because their handlers pass no default filter even though the companion docs frame them as follow-on views rather than default history boards.
- The initiative index, planning catalog, loaders, and query services are already explicit and deterministic. The mismatch is centered in how the CLI entrypoints choose default browse behavior and how their companion docs explain that choice.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): requires route-first, inspectable behavior with explicit human-and-machine parity rather than hidden default history browsing.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires thin start-here entrypoints and synchronized companion-surface updates when behavior expectations change.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): keeps deep planning and initiative views explicitly linked to trace state while preserving the authority hierarchy across planning projections.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): constrains how initiative-family browsing, phase state, and historical lookup remain available after the active-default browse change.
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md): reinforces that lifecycle `status` must not be overloaded with initiative outcome semantics, so the design should continue using explicit `initiative_status`.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): requires the query command docs to describe the changed default and historical opt-in path explicitly.

## Design Goals and Constraints
- Make filterless planning and initiative browse behavior consistent with the active-first planning navigation model.
- Preserve deterministic explicit lookup for completed traces and historical statuses; known-trace and explicitly filtered calls must not be broken by the new default.
- Keep the initiative index, planning catalog, loader APIs, and query-service filtering logic stable unless the review loop proves they are part of the same issue.

## Options Considered
### Option 1
- Leave runtime behavior alone and update only the README and command-doc guidance.
- Lowest-risk implementation footprint.
- Rejected because the machine behavior would still contradict the authority guidance and continue to present closed history by default.

### Option 2
- Apply an `active` default only for filterless browse invocations of `query planning` and `query initiatives`, mirror the applied default in JSON payloads, and update companion docs and tests to describe explicit history opt-in.
- Fixes the live runtime/docs mismatch while preserving trace-specific and explicit historical lookup.
- Requires careful defaulting rules so the active default applies only when the user has not already supplied meaningful history or trace filters.

### Option 3
- Require explicit `--trace-id` or `--initiative-status` for all `query planning` and `query initiatives` calls.
- Maximizes clarity around current-vs-history intent.
- Rejected because it would turn a low-friction query surface into a stricter contract than the audit or foundations require and would break legitimate explicit searches unnecessarily.

## Recommended Design
### Architecture
- Keep the initiative and planning query services generic and unchanged; they should continue to honor whatever filter set they are given without embedding navigation policy.
- Add the active-default browse decision in the CLI handler layer, where command-intent defaults already live for coordination.
- Mirror the applied default into JSON payloads through the existing `default_initiative_status` field pattern already used by `query coordination`.
- Align the planning README and command-doc family so the human guidance matches the new filterless browse behavior and explicit history lookup path.

### Data and Interface Impacts
- No control-plane schema or index-artifact change is expected; the initiative index, planning catalog, and authority map remain the authoritative machine data sources.
- The CLI JSON payloads for `query planning` and `query initiatives` will gain `default_initiative_status` when the filterless active-default path is applied.
- Human output will gain more explicit empty-state guidance when the active-default path yields no current matches.

### Execution Flow
1. Detect filterless browse invocations for `query planning` and `query initiatives` in the CLI handler layer and apply `initiative_status="active"` only in that bounded case.
2. Preserve explicit trace, query-text, and history-filtered lookups by skipping the default when the user has already expressed a narrower intent.
3. Emit the applied default in JSON payloads and refresh the companion docs and README routing notes so history lookup remains explicit.
4. Extend the direct CLI planning-query tests to cover the new default behavior and the preserved explicit history path.

### Invariants and Failure Cases
- Explicit `--trace-id`, `--initiative-status`, or intentionally specific filters must remain authoritative and must not be silently overridden by the active-default policy.
- The implementation should fail closed toward clarity: if no active initiatives exist, unfiltered planning and initiative queries should return zero results plus explicit default-status signaling rather than silently falling back to historical rows.
- The refactor fails if it changes loader, sync, or artifact-generation behavior instead of staying within the bounded query-entrypoint seam.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- docs/commands/core_python/
- docs/planning/
- core/python/tests/unit/test_cli_planning_query_commands.py

## Design Guardrails
- Keep the active-default policy in the CLI entrypoint layer so the underlying query services remain reusable and explicit.
- Do not weaken or hide explicit historical browsing; the design must make history opt-in clearer, not harder to reach once asked for.

## Risks
- Applying the default too broadly could suppress legitimate historical searches that currently rely on unfiltered browse behavior.
- Applying it too narrowly would leave the authority/runtime mismatch mostly intact.

## References
- March 13, 2026 refactor audit
- [active_first_planning_query_history_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/active_first_planning_query_history_alignment.md)
