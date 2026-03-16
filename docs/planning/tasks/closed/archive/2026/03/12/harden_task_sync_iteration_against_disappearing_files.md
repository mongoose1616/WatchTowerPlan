---
id: task.task_sync_disappearing_file_resilience.implementation.001
trace_id: trace.task_sync_disappearing_file_resilience
title: Harden task sync iteration against disappearing files
summary: Make shared task iteration skip vanished task files during live task moves
  while preserving validation for the surviving task set.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T13:00:27Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/sync/task_index.py
- core/python/src/watchtower_core/repo_ops/sync/task_tracking.py
- core/python/tests/unit/
related_ids:
- prd.task_sync_disappearing_file_resilience
- design.features.task_sync_disappearing_file_resilience
- design.implementation.task_sync_disappearing_file_resilience
- decision.task_sync_disappearing_file_resilience_direction
- contract.acceptance.task_sync_disappearing_file_resilience
---

# Harden task sync iteration against disappearing files

## Summary
Make shared task iteration skip vanished task files during live task moves while preserving validation for the surviving task set.

## Scope
- Harden iter_task_documents to skip only FileNotFoundError from a task path that vanished after enumeration.
- Keep task-index, task-tracking, and coordination refresh behavior unchanged for surviving task documents.
- Add regression coverage for the disappearing-file boundary.

## Done When
- Task sync no longer crashes when a discovered task file disappears before load.
- Surviving task documents still validate strictly.
- Regression coverage locks the disappearing-file behavior in place.
