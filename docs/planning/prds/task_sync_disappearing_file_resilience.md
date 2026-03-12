---
trace_id: trace.task_sync_disappearing_file_resilience
id: prd.task_sync_disappearing_file_resilience
title: Task Sync Disappearing File Resilience PRD
summary: Harden task and coordination sync against task documents disappearing during
  live task moves or concurrent lifecycle updates.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T13:02:49Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/sync/task_index.py
- core/python/src/watchtower_core/repo_ops/sync/task_tracking.py
- core/python/tests/unit/
---

# Task Sync Disappearing File Resilience PRD

## Record Metadata
- `Trace ID`: `trace.task_sync_disappearing_file_resilience`
- `PRD ID`: `prd.task_sync_disappearing_file_resilience`
- `Status`: `active`
- `Linked Decisions`: `decision.task_sync_disappearing_file_resilience_direction`
- `Linked Designs`: `design.features.task_sync_disappearing_file_resilience`
- `Linked Implementation Plans`: `design.implementation.task_sync_disappearing_file_resilience`
- `Updated At`: `2026-03-12T13:02:49Z`

## Summary
Harden task and coordination sync against task documents disappearing during live task moves or concurrent lifecycle updates.

## Problem Statement
The comprehensive project review reproduced a live orchestration defect in the governed task lifecycle: `watchtower-core task update --write` can fail with `FileNotFoundError` during coordination refresh when a task document is discovered under `docs/planning/tasks/open/` or `docs/planning/tasks/closed/` and then disappears before `load_task_document(...)` reads it. The reproduced failure path runs through `iter_task_documents(...)`, which is shared by task-index and task-tracking sync. As a result, otherwise valid task moves can fail under concurrent or near-concurrent lifecycle operations even though the repository converges to a valid final state.

## Goals
- Make task-document iteration resilient when a task path vanishes between directory enumeration and document load during live task moves.
- Preserve strict validation for every task document that still exists at load time.
- Add durable regression coverage so task-index, task-tracking, and coordination refreshes do not regress on this disappearing-file scenario.

## Non-Goals
- Introduce cross-process locking, filesystem leases, or broad serialization requirements around task updates.
- Relax schema or semantic validation for existing governed task documents.
- Generalize the fix across unrelated document families that do not currently reproduce the task-move defect.

## Requirements
- `req.task_sync_disappearing_file_resilience.001`: Task-document iteration must tolerate a task file disappearing between directory discovery and document load so task-index, task-tracking, and coordination refresh can continue on the surviving task set.
- `req.task_sync_disappearing_file_resilience.002`: The fix must remain fail-closed for task documents that still exist; it must not suppress front-matter, semantic, or structural validation errors for stable task files.
- `req.task_sync_disappearing_file_resilience.003`: Regression coverage must reproduce the disappearing-file boundary and prove the iterator skips only the vanished path while preserving deterministic output for the remaining task documents.

## Acceptance Criteria
- `ac.task_sync_disappearing_file_resilience.001`: The trace carries a fully authored planning chain, accepted direction decision, acceptance contract, evidence artifact, and bounded closed task set for this task-sync hardening slice.
- `ac.task_sync_disappearing_file_resilience.002`: `iter_task_documents(...)` and the task sync surfaces it feeds continue successfully when one discovered task file vanishes before load, without weakening validation for surviving task documents.
- `ac.task_sync_disappearing_file_resilience.003`: Regression coverage proves the iterator skips only the vanished task path and keeps surviving task-document validation fail-closed.
- `ac.task_sync_disappearing_file_resilience.004`: Repository validation, full-suite checks, and a follow-up expansive review pass complete without new issues in the reviewed planning/task orchestration area.

## Risks and Dependencies
- Skipping vanished paths too broadly could mask real repository corruption if the implementation catches more than the transient disappearance case.
- The fix depends on keeping the task iterator boundary narrow so the change does not alter other governed document families without evidence.
- Because the failure reproduced during real command execution, the final review pass must include live lifecycle/sync validation rather than test-only confidence.

## References
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/sync/task_index.py
- core/python/src/watchtower_core/repo_ops/sync/task_tracking.py
- docs/standards/governance/task_tracking_standard.md
- docs/foundations/engineering_design_principles.md
