---
trace_id: trace.task_query_dependency_lookup_hardening
id: decision.task_query_dependency_lookup_hardening_direction
title: Task Query Dependency Lookup Hardening Direction Decision
summary: Records the initial direction decision for Task Query Dependency Lookup Hardening.
type: decision_record
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

# Task Query Dependency Lookup Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.task_query_dependency_lookup_hardening`
- `Decision ID`: `decision.task_query_dependency_lookup_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.task_query_dependency_lookup_hardening`
- `Linked Designs`: `design.features.task_query_dependency_lookup_hardening`
- `Linked Implementation Plans`: `design.implementation.task_query_dependency_lookup_hardening`
- `Updated At`: `2026-03-12T20:12:31Z`

## Summary
Records the initial direction decision for Task Query Dependency Lookup Hardening.

## Decision Statement
Keep reverse-dependency lookup logic inside `TaskQueryService`, but only invoke it from
`query tasks` when dependency details are requested and batch that detailed lookup once per
command.

## Trigger or Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Current Context and Constraints
- The task query handler currently computes reverse dependencies once per returned task even when
  dependency details are omitted from the output.
- The optimization must preserve current task query payload shape, ordering, and dependency
  semantics.

## Applied References and Implications
- `docs/foundations/engineering_design_principles.md`: optimization should stay explicit and
  deterministic at the local authority boundary.
- `docs/standards/governance/task_tracking_standard.md`: task query behavior must remain aligned
  with the task index as the machine-readable source of truth.
- `docs/standards/governance/traceability_standard.md`: the optimization must close with traced
  planning, evidence, and validation state aligned.

## Affected Surfaces
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/

## Options Considered
### Option 1
- Add one handler-only guard so reverse-dependency lookup runs only when dependency details are
  requested.
- Solves the wasted default-path work with minimal change.
- Leaves the dependency-detail path scanning the full task index once per returned result.

### Option 2
- Add a batched reverse-dependency lookup helper to `TaskQueryService` and use it only when
  dependency details are requested.
- Solves both the wasted default-path work and the repeated-scan detailed path while preserving
  one query-service authority boundary.
- Slightly increases task-query service surface area.

## Chosen Outcome
Adopt Option 2. The handler will skip dependency-detail work unless the caller asks for it, and
the task query service will provide one batched reverse-dependency lookup path for the detailed
case.

## Rationale and Tradeoffs
- The wasted work originates in handler orchestration, but the dependency-graph semantics belong
  with the task query service.
- A batched service helper keeps the optimization reusable and avoids repeating full-index scans
  when dependency details are requested.
- The extra helper is acceptable because it preserves the existing public CLI behavior while
  reducing the scaling cost of a growing task index.

## Consequences and Follow-Up Impacts
- The task query service gains one small batched reverse-dependency helper.
- Handler regressions must now verify both the default no-details path and the dependency-detail
  path explicitly.

## Risks, Dependencies, and Assumptions
- The implementation assumes the current task index remains the canonical source for dependency
  relationships and that task IDs stay case-insensitive in query matching.

## References
- `docs/planning/prds/task_query_dependency_lookup_hardening.md`
- `docs/planning/design/features/task_query_dependency_lookup_hardening.md`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/tasks.py`
