---
trace_id: trace.task_query_dependency_lookup_hardening
id: design.features.task_query_dependency_lookup_hardening
title: Task Query Dependency Lookup Hardening Feature Design
summary: Defines the technical design boundary for Task Query Dependency Lookup Hardening.
type: feature_design
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

# Task Query Dependency Lookup Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.task_query_dependency_lookup_hardening`
- `Design ID`: `design.features.task_query_dependency_lookup_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.task_query_dependency_lookup_hardening`
- `Linked Decisions`: `decision.task_query_dependency_lookup_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.task_query_dependency_lookup_hardening`
- `Updated At`: `2026-03-12T20:12:31Z`

## Summary
Defines the technical design boundary for Task Query Dependency Lookup Hardening.

## Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope and Feature Boundary
- Optimize the `watchtower-core query tasks` handler and task query service so dependency-detail
  work happens only when requested and is batched when it is requested.
- Exclude changes to task indexing, task lifecycle behavior, CLI flags, or payload schema.

## Current-State Context
- `TaskQueryService.reverse_dependencies()` currently scans the full task index for one task ID
  at a time.
- The `query tasks` handler currently calls that method once per returned task even when
  `--include-dependency-details` is disabled, so the default path pays dependency-graph cost it
  never exposes in the payload.
- Direct instrumentation of the live handler showed `5` reverse-dependency scans for `5`
  results and `20` scans for the default `--limit 20` path with dependency details disabled.

## Foundations References Applied
- `docs/foundations/engineering_design_principles.md`: optimize at the local deterministic
  authority boundary instead of introducing opaque shared state.
- `docs/foundations/repository_standards_posture.md`: performance work must preserve existing
  machine-readable fidelity and same-change validation discipline.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: implementation and regression
  coverage stay in the canonical Python workspace.
- `docs/standards/governance/task_tracking_standard.md`: task query behavior must remain aligned
  with the task index as the canonical machine-readable surface.
- `docs/standards/governance/traceability_standard.md`: non-trivial optimization work should
  close with traced planning, evidence, and validation state aligned.

## Design Goals and Constraints
- Remove reverse-dependency work from the default task-query path.
- Batch reverse-dependency lookup once for the dependency-detail path.
- Preserve existing result ordering and payload fields for both the default and detailed query
  outputs.

## Options Considered
### Option 1
- Gate `reverse_dependencies()` behind `--include-dependency-details` in the CLI handler only.
- Eliminates wasted reverse-dependency work from the default path with a very small code change.
- Leaves the detailed path doing one full index scan per returned task.

### Option 2
- Add one batched reverse-dependency lookup helper to `TaskQueryService` and use it only when
  dependency details are requested.
- Fixes both the wasted default-path work and the repeated-scan detailed path while keeping the
  optimization inside the task query abstraction.
- Adds one small helper and regression surface to the query service.

## Recommended Design
### Architecture
- `TaskQueryService` remains the authority for task-query dependency lookup behavior.
- The CLI handler remains responsible for deciding whether dependency-detail work is needed for
  the requested output shape.
- The query service gains one batched reverse-dependency map helper so the handler can request
  all needed reverse links in one pass.

### Data and Interface Impacts
- No schema, CLI flag, or payload-shape changes are required.
- The optimization only changes internal control flow in the task query handler and service.

### Execution Flow
1. `query tasks` loads and filters task-index entries exactly as it does today.
2. If dependency details are not requested, the handler emits the existing payload directly with
   no reverse-dependency lookup work.
3. If dependency details are requested, the handler asks `TaskQueryService` for one batched
   reverse-dependency map covering the returned task IDs and reuses that map while building the
   detailed payload.

### Invariants and Failure Cases
- Tasks with no reverse dependencies must still return empty reverse-dependency detail lists.
- Batched reverse-dependency lookup must stay case-insensitive just like the existing
  single-task method.

## Affected Surfaces
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/

## Design Guardrails
- Keep task index loading and task dependency semantics centralized in `TaskQueryService`.
- Do not introduce long-lived caches or mutate task-index entries in place.

## Risks
- The main risk is behavioral drift in dependency-detail payloads if the batch lookup does not
  exactly mirror the existing per-task scan semantics.

## References
- `docs/planning/prds/task_query_dependency_lookup_hardening.md`
- `docs/planning/design/implementation/task_query_dependency_lookup_hardening.md`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/tasks.py`
