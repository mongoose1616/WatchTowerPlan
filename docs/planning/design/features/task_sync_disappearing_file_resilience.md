---
trace_id: trace.task_sync_disappearing_file_resilience
id: design.features.task_sync_disappearing_file_resilience
title: Task Sync Disappearing File Resilience Feature Design
summary: Defines the technical design boundary for Task Sync Disappearing File Resilience.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-12T12:53:02Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/sync/task_index.py
- core/python/src/watchtower_core/repo_ops/sync/task_tracking.py
- core/python/tests/unit/
---

# Task Sync Disappearing File Resilience Feature Design

## Record Metadata
- `Trace ID`: `trace.task_sync_disappearing_file_resilience`
- `Design ID`: `design.features.task_sync_disappearing_file_resilience`
- `Design Status`: `active`
- `Linked PRDs`: `prd.task_sync_disappearing_file_resilience`
- `Linked Decisions`: `decision.task_sync_disappearing_file_resilience_direction`
- `Linked Implementation Plans`: `design.implementation.task_sync_disappearing_file_resilience`
- `Updated At`: `2026-03-12T12:53:02Z`

## Summary
Defines the technical design boundary for Task Sync Disappearing File Resilience.

## Source Request
- A comprehensive project review reproduced `FileNotFoundError` during live `watchtower-core task update --write` execution when governed task files were moved between discovery and load inside shared task-sync paths.

## Scope and Feature Boundary
- Covers the shared task-document iterator boundary, the task-index and task-tracking sync surfaces that consume it, and regression coverage for the disappearing-file scenario.
- Excludes broad synchronization primitives, unrelated planning-document iterators, and any weakening of validation for task documents that still exist.

## Current-State Context
- `iter_task_documents(...)` currently glob-discoveries task files and loads each one eagerly, assuming the task directory remains stable for the entire iteration.
- `TaskLifecycleService.update(...)` can move task files between `open/` and `closed/`, and coordination refresh rebuilds task-derived surfaces immediately after each write, so overlapping lifecycle operations can expose a transient path that no longer exists by load time.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the design should fail closed for real invalid task documents while remaining robust to transient repository-state churn caused by valid lifecycle operations.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task lifecycle state must stay reliable and queryable through the generated task and coordination surfaces even when tasks transition between open and closed storage roots.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the fix should stay inside the canonical Python workspace and land with automated regression coverage.

## Design Goals and Constraints
- Localize the fix to the task iterator so every task-sync consumer benefits without duplicating retry logic.
- Keep exception handling narrow to `FileNotFoundError` for vanished task paths only.
- Preserve deterministic ordering and strict validation for every surviving task document.

## Options Considered
### Option 1
- Require callers to serialize task lifecycle updates or implement retries around failed sync commands.
- Strength: little internal code change.
- Tradeoff: pushes brittle behavior onto every caller and leaves the shared iterator boundary unsafe.

### Option 2
- Harden `iter_task_documents(...)` so it skips paths that disappear before load while still surfacing all other validation failures.
- Strength: fixes the reproduced defect once at the shared iterator boundary and keeps the surviving task set fully validated.
- Tradeoff: a transiently missing task is omitted from that one sync pass until the repository settles and the next refresh runs.

### Option 3
- Add global task-lifecycle locking around every write and sync operation.
- Strength: could eliminate a broader class of concurrent file-move races.
- Tradeoff: materially increases orchestration complexity for a reproduced defect that only needs iterator-level resilience.

## Recommended Design
### Architecture
- Keep `TaskLifecycleService` responsible for task moves and writes.
- Harden `iter_task_documents(...)` in [task_documents.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/task_documents.py) so the shared task enumeration path tolerates a vanished file during load.
- Preserve downstream task-index and task-tracking sync logic unchanged so they continue to consume one deterministic tuple of surviving task documents.

### Data and Interface Impacts
- No schema or command-surface contract changes are required.
- The behavior change is operational only: disappearing task paths become a skipped transient instead of a fatal sync crash.

### Execution Flow
1. Enumerate the governed task paths in deterministic order.
2. Attempt to load each task document; if the path vanished before load, skip it and continue.
3. Return the surviving task documents to task-index, task-tracking, and coordination sync, while preserving existing validation for every successfully loaded document.

### Invariants and Failure Cases
- Front-matter, semantic, and structural validation errors for surviving task documents must still raise normally.
- A task path that vanishes before load must not crash the entire sync pass.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/sync/task_index.py
- core/python/src/watchtower_core/repo_ops/sync/task_tracking.py
- core/python/tests/unit/

## Design Guardrails
- Catch only `FileNotFoundError` at the iterator boundary; do not suppress `ValueError` or schema-validation failures for existing task documents.
- Keep command docs unchanged unless the implementation materially changes CLI behavior visible to operators.

## Risks
- The main risk is over-broad exception handling; regression coverage must prove only the vanished-path case is tolerated.

## References
- docs/planning/prds/task_sync_disappearing_file_resilience.md
- core/python/src/watchtower_core/repo_ops/task_documents.py
- docs/standards/governance/task_tracking_standard.md
