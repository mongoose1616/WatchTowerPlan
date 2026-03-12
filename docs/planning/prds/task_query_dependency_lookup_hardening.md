---
trace_id: trace.task_query_dependency_lookup_hardening
id: prd.task_query_dependency_lookup_hardening
title: Task Query Dependency Lookup Hardening PRD
summary: Eliminate unnecessary reverse-dependency recomputation in the task query
  surface by skipping dependency-graph work unless the caller requests dependency
  details and batching the detailed path without changing query fidelity.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T20:12:31Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/
---

# Task Query Dependency Lookup Hardening PRD

## Record Metadata
- `Trace ID`: `trace.task_query_dependency_lookup_hardening`
- `PRD ID`: `prd.task_query_dependency_lookup_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.task_query_dependency_lookup_hardening_direction`
- `Linked Designs`: `design.features.task_query_dependency_lookup_hardening`
- `Linked Implementation Plans`: `design.implementation.task_query_dependency_lookup_hardening`
- `Updated At`: `2026-03-12T20:12:31Z`

## Summary
Eliminate unnecessary reverse-dependency recomputation in the task query surface by skipping dependency-graph work unless the caller requests dependency details and batching the detailed path without changing query fidelity.

## Problem Statement
The repository's `watchtower-core query tasks` path is doing dependency-graph work even when
the caller does not request dependency details. Direct instrumentation of the live handler
showed `TaskQueryService.reverse_dependencies()` being called once per returned result with
`--include-dependency-details` disabled, producing `5` reverse-dependency scans for `5` results
and `20` scans for the default `--limit 20` path. The detailed path currently performs the same
per-result rescans instead of batching the reverse-dependency lookup once for the command.

That behavior is correct but unnecessarily expensive as the task index grows. The optimization
must preserve the existing result payload, ordering, and dependency-detail fidelity while
removing wasted reverse-dependency recomputation from the default path and collapsing the
detailed path to one bounded reverse-dependency pass.

## Goals
- Eliminate reverse-dependency work from the default task-query path when dependency details are
  not requested.
- Reduce the dependency-detail path from repeated per-result rescans to one batched
  reverse-dependency lookup per command run.
- Preserve current task-query payload fidelity, ordering, and dependency-detail semantics.

## Non-Goals
- Change the task query command surface, flags, or output schema.
- Redesign task indexing, task lifecycle semantics, or the task data contract.
- Introduce persistent caches or global state beyond one loader-backed command run.

## Requirements
- `req.task_query_dependency_lookup_hardening.001`: The default `watchtower-core query tasks`
  path must not compute reverse dependencies unless `--include-dependency-details` is enabled.
- `req.task_query_dependency_lookup_hardening.002`: When dependency details are requested, the
  task query flow must compute reverse dependencies through one batched pass instead of one scan
  per returned task.
- `req.task_query_dependency_lookup_hardening.003`: The optimization must preserve existing task
  query payload fields, dependency-detail correctness, and result ordering.
- `req.task_query_dependency_lookup_hardening.004`: The change must be covered by targeted
  regressions, measured against the current handler behavior, and closed with a full repository
  validation baseline plus a clean follow-up review of adjacent query surfaces.

## Acceptance Criteria
- `ac.task_query_dependency_lookup_hardening.001`: The trace publishes a fully-authored planning
  chain, accepted direction decision, refreshed acceptance contract, refreshed evidence
  artifact, and a bounded closed task set for the task-query optimization slice.
- `ac.task_query_dependency_lookup_hardening.002`: The default task-query path performs zero
  reverse-dependency lookups when dependency details are omitted.
- `ac.task_query_dependency_lookup_hardening.003`: The dependency-detail task-query path
  computes reverse dependencies through one batched map while preserving the existing payload.
- `ac.task_query_dependency_lookup_hardening.004`: The repository stays green on sync,
  acceptance validation, full validation, tests, mypy, and ruff after the optimization lands.
- `ac.task_query_dependency_lookup_hardening.005`: A follow-up review of adjacent task-query,
  coordination, and task-index surfaces finds no additional actionable issues.

## Risks and Dependencies
- Over-optimizing the handler could silently drop dependency-detail fields or change ordering if
  the batching path is not validated against the current payload shape.
- The change depends on keeping the task index as the machine authority for query behavior
  rather than introducing separate dependency metadata.

## References
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/tasks.py`
- `core/python/tests/unit/test_route_and_query_handlers.py`
- `core/python/tests/unit/test_cli_query_commands.py`
