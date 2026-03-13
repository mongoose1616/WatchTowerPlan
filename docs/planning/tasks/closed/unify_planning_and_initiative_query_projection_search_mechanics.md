---
id: task.planning_query_efficiency_and_handler_modularity.query_projection_search.001
trace_id: trace.planning_query_efficiency_and_handler_modularity
title: Unify planning and initiative query projection search mechanics
summary: Refactor the duplicated planning, initiative, and coordination query filter
  and ranking logic behind one shared runtime helper.
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
- core/python/src/watchtower_core/repo_ops/query/common.py
- core/python/src/watchtower_core/repo_ops/query/initiatives.py
- core/python/src/watchtower_core/repo_ops/query/planning.py
- core/python/src/watchtower_core/repo_ops/query/coordination.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/unit/test_projection_search_common.py
related_ids:
- prd.planning_query_efficiency_and_handler_modularity
- design.features.planning_query_efficiency_and_handler_modularity
- design.implementation.planning_query_efficiency_and_handler_modularity
- decision.planning_query_efficiency_and_handler_modularity_direction
---

# Unify planning and initiative query projection search mechanics

## Summary
Refactor the duplicated planning, initiative, and coordination query filter and ranking logic behind one shared runtime helper.

## Scope
- Design one shared helper for trace/status/phase/owner filtering and query ranking across the planning, initiative, and coordination query services.
- Refactor the affected query services to consume the helper without changing query semantics, result ordering, or payload fidelity.

## Done When
- The duplicated common search mechanics live behind one explicit helper and targeted query-service regressions pass.
