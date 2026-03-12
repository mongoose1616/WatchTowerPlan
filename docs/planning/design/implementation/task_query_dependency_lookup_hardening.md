---
trace_id: trace.task_query_dependency_lookup_hardening
id: design.implementation.task_query_dependency_lookup_hardening
title: Task Query Dependency Lookup Hardening Implementation Plan
summary: Breaks Task Query Dependency Lookup Hardening into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-12T20:12:31Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/
---

# Task Query Dependency Lookup Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.task_query_dependency_lookup_hardening`
- `Plan ID`: `design.implementation.task_query_dependency_lookup_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.task_query_dependency_lookup_hardening`
- `Linked Decisions`: `decision.task_query_dependency_lookup_hardening_direction`
- `Source Designs`: `design.features.task_query_dependency_lookup_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.task_query_dependency_lookup_hardening`
- `Updated At`: `2026-03-12T20:12:31Z`

## Summary
Breaks Task Query Dependency Lookup Hardening into a bounded implementation slice.

## Source Request or Design
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope Summary
- Remove wasted reverse-dependency work from the default `query tasks` path.
- Add one batched reverse-dependency lookup path for dependency-detail output.
- Exclude task-index schema changes, task lifecycle changes, or CLI surface changes.

## Assumptions and Constraints
- The task index remains the sole machine authority for dependency lookup behavior.
- Query payload fields, ordering, and dependency-detail semantics must remain unchanged.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: code and tests stay in the
  canonical Python workspace.
- `docs/standards/governance/task_tracking_standard.md`: task query behavior must keep the task
  index authoritative.
- `docs/standards/governance/traceability_standard.md`: implementation, evidence, and closeout
  work must stay traced together.

## Proposed Technical Approach
- Add a batched reverse-dependency lookup helper to `TaskQueryService` that builds one
  case-insensitive reverse-dependency map from the cached task index.
- Update the `query tasks` handler so it only requests reverse-dependency data when
  `--include-dependency-details` is enabled and reuses the batched map for the detailed path.
- Add targeted handler regressions that prove the default path performs no reverse-dependency
  work and the detailed path batches the lookup once.

## Work Breakdown
1. Author the traced planning, decision, task, acceptance, and evidence surfaces for the
   measured task-query hotspot.
2. Implement the task query service and CLI handler optimization with targeted regression
   coverage.
3. Run measurement, validation, and a follow-up review of adjacent query surfaces, then close
   the initiative cleanly.

## Risks
- A batching change could accidentally change reverse-dependency ordering or task-ID matching if
  it is not validated against the current handler behavior.

## Validation Plan
- Measure handler behavior before and after the change by counting reverse-dependency lookups
  with and without `--include-dependency-details`.
- Add targeted unit coverage for the default handler path and the dependency-detail path.
- Run `watchtower-core sync all --write --format json`,
  `watchtower-core validate acceptance --trace-id trace.task_query_dependency_lookup_hardening --format json`,
  `watchtower-core validate all --format json`, `pytest -q`,
  `python -m mypy src/watchtower_core`, and `ruff check .`.
- Perform a follow-up review of adjacent task-query and coordination surfaces and record whether
  any additional issue remains.

## References
- `docs/planning/prds/task_query_dependency_lookup_hardening.md`
- `core/control_plane/contracts/acceptance/task_query_dependency_lookup_hardening_acceptance.v1.json`
