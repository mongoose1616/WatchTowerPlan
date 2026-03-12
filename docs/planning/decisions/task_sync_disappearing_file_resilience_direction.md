---
trace_id: trace.task_sync_disappearing_file_resilience
id: decision.task_sync_disappearing_file_resilience_direction
title: Task Sync Disappearing File Resilience Direction Decision
summary: Records the initial direction decision for Task Sync Disappearing File Resilience.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T12:53:02Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/sync/task_index.py
- core/python/src/watchtower_core/repo_ops/sync/task_tracking.py
- core/python/tests/unit/
---

# Task Sync Disappearing File Resilience Direction Decision

## Record Metadata
- `Trace ID`: `trace.task_sync_disappearing_file_resilience`
- `Decision ID`: `decision.task_sync_disappearing_file_resilience_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.task_sync_disappearing_file_resilience`
- `Linked Designs`: `design.features.task_sync_disappearing_file_resilience`
- `Linked Implementation Plans`: `design.implementation.task_sync_disappearing_file_resilience`
- `Updated At`: `2026-03-12T12:53:02Z`

## Summary
Records the initial direction decision for Task Sync Disappearing File Resilience.

## Decision Statement
Harden the shared task-document iterator so disappearing task files are skipped at load time while all surviving task documents continue to validate strictly.

## Trigger or Source Request
- A comprehensive project review reproduced `FileNotFoundError` during live task lifecycle writes when coordination refresh loaded a task file that had already been moved out of its discovered path.

## Current Context and Constraints
- Shared task sync currently assumes the task directory remains stable for the entire enumeration-and-load pass.
- The repository already relies on immediate task-index, task-tracking, and coordination refresh after task writes, so the smallest coherent fix is to harden the iterator boundary rather than require external serialization everywhere.

## Applied References and Implications
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task-derived tracking surfaces should remain reliable through legitimate lifecycle transitions between open and closed task storage roots.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): fix the reproduced failure at the narrow shared boundary and keep fail-closed behavior for real invalid data.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/sync/task_index.py
- core/python/src/watchtower_core/repo_ops/sync/task_tracking.py
- core/python/tests/unit/

## Options Considered
### Option 1
- Require callers or operators to serialize task lifecycle writes and retry failed coordination refreshes manually.
- Strength: avoids touching iterator code.
- Tradeoff: leaves the shared sync boundary brittle and pushes operational complexity onto every caller.

### Option 2
- Catch `FileNotFoundError` inside `iter_task_documents(...)`, skip the vanished path, and preserve strict validation for every remaining task document.
- Strength: fixes the reproduced defect centrally for task-index, task-tracking, and coordination sync without changing public command contracts.
- Tradeoff: one transient sync pass may omit the moved task until the next stable refresh.

### Option 3
- Introduce locking or a broader orchestration layer around all task mutations and derived-surface rebuilds.
- Strength: could address a wider class of concurrent filesystem races.
- Tradeoff: disproportionate complexity for a narrowly reproduced disappearing-file defect.

## Chosen Outcome
Option 2 is accepted.

## Rationale and Tradeoffs
- The failure was reproduced at the shared iterator boundary, so the most coherent fix is to harden that boundary once instead of scattering retries across callers.
- Catching only `FileNotFoundError` keeps the repository fail-closed for genuine invalid task documents.

## Consequences and Follow-Up Impacts
- `task_documents.py` will change, and regression coverage must prove only transient disappearance is tolerated.
- Task-sync and coordination surfaces should become resilient to live task moves without any visible CLI contract change.

## Risks, Dependencies, and Assumptions
- The implementation must not suppress validation failures for surviving task documents.
- The final review pass should confirm no additional orchestration issues remain in adjacent task-sync paths.

## References
- docs/planning/prds/task_sync_disappearing_file_resilience.md
- docs/planning/design/features/task_sync_disappearing_file_resilience.md
- core/python/src/watchtower_core/repo_ops/task_documents.py
