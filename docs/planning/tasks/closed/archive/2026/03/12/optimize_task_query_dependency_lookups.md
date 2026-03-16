---
id: task.task_query_dependency_lookup_hardening.reverse_dependency_batching.002
trace_id: trace.task_query_dependency_lookup_hardening
title: Optimize task query dependency lookups
summary: Skip reverse-dependency recomputation when dependency details are not requested
  and batch the detailed path through one precomputed reverse-dependency map.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T20:12:31Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/
related_ids:
- prd.task_query_dependency_lookup_hardening
- design.implementation.task_query_dependency_lookup_hardening
- decision.task_query_dependency_lookup_hardening_direction
- contract.acceptance.task_query_dependency_lookup_hardening
depends_on:
- task.task_query_dependency_lookup_hardening.bootstrap.001
---

# Optimize task query dependency lookups

## Summary
Skip reverse-dependency recomputation when dependency details are not requested and batch the detailed path through one precomputed reverse-dependency map.

## Scope
- Eliminate unnecessary reverse-dependency work from the default query-tasks path.
- Batch reverse-dependency lookup once when dependency details are requested.
- Preserve task query payload fidelity and result ordering.

## Done When
- The default query-tasks path performs no reverse-dependency work when dependency details are omitted.
- The detailed query-tasks path computes reverse dependencies through one batched map instead of per-result rescans.
- Targeted regression coverage and measurement demonstrate the optimization without payload drift.
