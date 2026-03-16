---
id: task.planning_query_efficiency_and_handler_modularity.coordination_handler_split.002
trace_id: trace.planning_query_efficiency_and_handler_modularity
title: Split coordination-query handlers behind focused modules
summary: Reduce the coordination-query handler hotspot by moving the current subcommand
  behaviors into focused modules behind a compatibility facade and aligned command
  docs.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T23:24:35Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_projection_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_family.py
- core/python/src/watchtower_core/cli/query_handlers.py
- docs/commands/core_python/
related_ids:
- prd.planning_query_efficiency_and_handler_modularity
- design.features.planning_query_efficiency_and_handler_modularity
- design.implementation.planning_query_efficiency_and_handler_modularity
- decision.planning_query_efficiency_and_handler_modularity_direction
depends_on:
- task.planning_query_efficiency_and_handler_modularity.query_projection_search.001
---

# Split coordination-query handlers behind focused modules

## Summary
Reduce the coordination-query handler hotspot by moving the current subcommand behaviors into focused modules behind a compatibility facade and aligned command docs.

## Scope
- Split the concentrated coordination-query handler module into focused modules while preserving current handler imports and runtime behavior.
- Reconcile command docs and direct consumer tests with the new source-surface ownership model.

## Done When
- The handler hotspot is reduced to a compatibility facade plus focused modules and the touched docs and tests stay aligned.
