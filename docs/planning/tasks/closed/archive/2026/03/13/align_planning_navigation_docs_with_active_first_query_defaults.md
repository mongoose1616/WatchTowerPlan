---
id: task.active_first_planning_query_history_alignment.navigation_docs_alignment.003
trace_id: trace.active_first_planning_query_history_alignment
title: Align planning navigation docs with active-first query defaults
summary: Refresh planning README and query command docs so the active-default browse
  behavior and explicit historical lookup path are documented consistently.
type: task
status: active
task_status: done
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T20:38:41Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/README.md
- docs/planning/initiatives/README.md
- docs/commands/core_python/watchtower_core_query_planning.md
- docs/commands/core_python/watchtower_core_query_initiatives.md
- docs/commands/core_python/watchtower_core_query.md
- docs/commands/core_python/watchtower_core_query_authority.md
related_ids:
- prd.active_first_planning_query_history_alignment
- design.features.active_first_planning_query_history_alignment
- design.implementation.active_first_planning_query_history_alignment
- decision.active_first_planning_query_history_alignment_direction
- contract.acceptance.active_first_planning_query_history_alignment
depends_on:
- task.active_first_planning_query_history_alignment.query_default_behavior.002
---

# Align planning navigation docs with active-first query defaults

## Summary
Refresh planning README and query command docs so the active-default browse behavior and explicit historical lookup path are documented consistently.

## Scope
- Update planning navigation READMEs and the relevant query command pages to match the active-first query behavior.
- Keep the documented deep-planning, initiative-family, and historical lookup boundaries aligned with the authority map.

## Done When
- The planning README, initiative README, and relevant query command docs describe the active-default browse path and explicit history opt-in consistently.
- The documented routing model matches the final runtime behavior with no human-versus-machine drift in the touched surfaces.
