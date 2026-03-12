---
trace_id: trace.task_sync_disappearing_file_resilience
id: design.implementation.task_sync_disappearing_file_resilience
title: Task Sync Disappearing File Resilience Implementation Plan
summary: Breaks Task Sync Disappearing File Resilience into a bounded implementation
  slice.
type: implementation_plan
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

# Task Sync Disappearing File Resilience Implementation Plan

## Record Metadata
- `Trace ID`: `trace.task_sync_disappearing_file_resilience`
- `Plan ID`: `design.implementation.task_sync_disappearing_file_resilience`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.task_sync_disappearing_file_resilience`
- `Linked Decisions`: `decision.task_sync_disappearing_file_resilience_direction`
- `Source Designs`: `design.features.task_sync_disappearing_file_resilience`
- `Linked Acceptance Contracts`: `contract.acceptance.task_sync_disappearing_file_resilience`
- `Updated At`: `2026-03-12T12:53:02Z`

## Summary
Breaks Task Sync Disappearing File Resilience into a bounded implementation slice.

## Source Request or Design
- design.features.task_sync_disappearing_file_resilience

## Scope Summary
- Covers iterator hardening for disappearing task files, regression coverage, and final validation/closeout for the shared task sync surfaces.
- Excludes command-surface redesign, global locking, and unrelated planning-document loaders that were not reproduced in the review.

## Assumptions and Constraints
- The iterator must stay deterministic and strict for surviving files even after it becomes tolerant of vanished paths.
- The slice should remain one implementation task plus one validation/closeout task after the bootstrap task is closed.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task lifecycle state must remain reliable through the generated task and coordination views.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): the final commit should preserve the traced remediation context and bounded scope.

## Proposed Technical Approach
- Harden `iter_task_documents(...)` to ignore only `FileNotFoundError` from paths that disappeared after enumeration and before load.
- Add unit coverage that simulates a disappearing task file and proves the surviving task documents are still returned in deterministic order.
- Re-run repository sync, validation, and the manual follow-up review pass to confirm no further task-orchestration issues remain.

## Work Breakdown
1. Close the bootstrap task and implement the iterator hardening in the shared task-document loader boundary.
2. Add regression coverage for the disappearing-file scenario and verify that stable validation errors still surface normally.
3. Refresh derived surfaces, validate the full repository baseline, repeat the expansive review pass, and close the trace if no new issues remain.

## Risks
- If the iterator catches too broadly, task sync could conceal real document corruption instead of only transient path churn.

## Validation Plan
- Add a unit test that simulates a discovered task file vanishing before load and confirms the iterator returns the remaining documents without crashing.
- Run targeted task-document and task-lifecycle tests, full `watchtower-core validate all --format json`, `pytest -q`, `python -m mypy src/watchtower_core`, `ruff check .`, and a follow-up manual review pass over the affected orchestration area.

## References
- docs/planning/design/features/task_sync_disappearing_file_resilience.md
- core/python/src/watchtower_core/repo_ops/task_documents.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
