---
id: task.active_first_planning_query_history_alignment.query_default_behavior.002
trace_id: trace.active_first_planning_query_history_alignment
title: Align filterless planning and initiative query defaults
summary: Apply active-first default browse behavior and default-status payload signaling
  to the planning and initiative query entrypoints while preserving explicit historical
  lookup.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T20:38:41Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_family.py
- core/python/tests/unit/test_cli_planning_query_commands.py
related_ids:
- prd.active_first_planning_query_history_alignment
- design.features.active_first_planning_query_history_alignment
- design.implementation.active_first_planning_query_history_alignment
- decision.active_first_planning_query_history_alignment_direction
- contract.acceptance.active_first_planning_query_history_alignment
---

# Align filterless planning and initiative query defaults

## Summary
Apply active-first default browse behavior and default-status payload signaling to the planning and initiative query entrypoints while preserving explicit historical lookup.

## Scope
- Update the planning and initiative query handlers so filterless browse calls default to active without changing explicit trace or explicit history lookups.
- Add regression coverage for the new default behavior and preserved explicit historical path.

## Done When
- Unfiltered query planning and query initiatives calls apply the intended active default only in the bounded browse case.
- JSON payloads expose the applied default and explicit historical or trace-specific lookups still return the expected completed traces.
