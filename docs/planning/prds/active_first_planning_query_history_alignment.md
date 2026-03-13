---
trace_id: trace.active_first_planning_query_history_alignment
id: prd.active_first_planning_query_history_alignment
title: Active-First Planning Query History Alignment PRD
summary: Align planning and initiative query entrypoints with the active-first planning
  navigation model so unfiltered deep or initiative browse commands no longer default
  to terminal-history results while explicit trace and history lookup remain deterministic.
type: prd
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

# Active-First Planning Query History Alignment PRD

## Record Metadata
- `Trace ID`: `trace.active_first_planning_query_history_alignment`
- `PRD ID`: `prd.active_first_planning_query_history_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.active_first_planning_query_history_alignment_direction`
- `Linked Designs`: `design.features.active_first_planning_query_history_alignment`
- `Linked Implementation Plans`: `design.implementation.active_first_planning_query_history_alignment`
- `Updated At`: `2026-03-13T20:42:11Z`

## Summary
Align planning and initiative query entrypoints with the active-first planning navigation model so unfiltered deep or initiative browse commands no longer default to terminal-history results while explicit trace and history lookup remain deterministic.

## Problem Statement
- The March 13, 2026 refactor audit left a live planning-navigation gap after the earlier coordination and authority-surface traces: the repository now documents an active-first start-here path, but the deeper planning and initiative query entrypoints still behave like history browsers when invoked without an explicit filter.
- `watchtower-core query authority --domain planning --format json` explicitly says current planning state should start with `query coordination`, deeper trace context should use `query planning` after coordination identifies the trace, and compact historical browsing should use `query initiatives`.
- In the current runtime state, `watchtower-core query planning --format json` and `watchtower-core query initiatives --format json` both return completed traces by default when no active initiatives exist, even though their surrounding README and authority guidance frame them as active-first follow-on entrypoints rather than default closed-history listings.
- The mismatch creates avoidable navigation drift: human and machine users receive one policy answer from the authority map and planning READMEs, but a different default experience from the CLI query entrypoints themselves.

## Goals
- Align unfiltered `query planning` and `query initiatives` behavior with the repository's active-first planning navigation model.
- Preserve deterministic explicit historical lookup through `--initiative-status`, `--trace-id`, and other explicit query filters.
- Make the default filter behavior visible in structured output and companion docs so machine and human consumers can tell when the active-default path was applied.
- Complete the refactor under one stable traced loop with durable discovery evidence, validation, post-fix review, repeated confirmation passes, and clean closeout.

## Non-Goals
- Changing the initiative index, planning catalog, traceability index, or coordination index schemas or derived artifact shapes.
- Collapsing planning artifact families, removing history access, or changing the canonical authority map hierarchy established by earlier traces.
- Reopening task-threshold or traceability-policy questions from `RF-STD-002`; this trace is about active-vs-history query navigation, not planning-governance volume policy.
- Broad CLI family restructuring beyond the planning and initiative query entrypoints plus their direct companion docs and tests.

## Requirements
- `req.active_first_planning_query_history_alignment.001`: The trace must publish and follow an explicit coverage map plus findings ledger across planning query handlers, direct query services, command docs, planning navigation READMEs, regression tests, and traced governance surfaces before remediation begins.
- `req.active_first_planning_query_history_alignment.002`: Unfiltered browse invocations of `watchtower-core query planning` and `watchtower-core query initiatives` must align with the active-first planning navigation model instead of defaulting to terminal-history results, while explicit trace or historical lookup remains available and deterministic.
- `req.active_first_planning_query_history_alignment.003`: The planning and initiative query payloads plus human-facing command and README guidance must make the active-default behavior and explicit historical opt-in path clear to both machine and human consumers.
- `req.active_first_planning_query_history_alignment.004`: The implementation must preserve current loader, index, and query service fidelity by limiting behavior changes to the bounded query-entrypoint seam unless the review loop confirms a direct same-theme issue elsewhere.
- `req.active_first_planning_query_history_alignment.005`: Targeted validation, full repository validation, a post-fix review pass, a second independent no-new-issues review, and an adversarial confirmation pass must all complete cleanly before closeout.

## Acceptance Criteria
- `ac.active_first_planning_query_history_alignment.001`: The planning corpus for `trace.active_first_planning_query_history_alignment` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, bounded execution tasks, and the explicit coverage map plus findings ledger for the slice.
- `ac.active_first_planning_query_history_alignment.002`: Unfiltered `watchtower-core query planning` and `watchtower-core query initiatives` now apply the intended active-default browse behavior, while explicit trace or historical lookups still return the expected completed traces.
- `ac.active_first_planning_query_history_alignment.003`: Structured planning and initiative query payloads expose the applied default initiative-status when the active-default path is used, and human output or docs no longer leave the default browse behavior implicit.
- `ac.active_first_planning_query_history_alignment.004`: Planning navigation READMEs and the relevant query command pages explain the active-first routing model, explicit history lookup path, and deep-planning-vs-initiative-family boundary consistently.
- `ac.active_first_planning_query_history_alignment.005`: Targeted tests, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation all complete with no new actionable issue under the same active-vs-history planning-navigation theme.

## Risks and Dependencies
- An over-broad default filter could break explicit deep-history workflows if it suppresses trace-specific or intentionally filtered historical lookups.
- A docs-only change would leave the runtime browse experience inconsistent with the authority map and planning entrypoint guidance.
- The slice depends on keeping command docs, planning READMEs, direct query handlers, and regression tests aligned in the same change so the active-default behavior is explicit everywhere it matters.

## References
- March 13, 2026 refactor audit
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md)
