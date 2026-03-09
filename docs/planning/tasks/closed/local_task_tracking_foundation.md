---
id: "task.local_task_tracking_foundation.001"
trace_id: "trace.local_task_tracking"
title: "Establish local-first task tracking foundation"
summary: "Establishes governed local task records, a generated human tracker, a generated machine index, and Python query and sync commands for task coordination."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-09T14:41:51Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/tasks/task_index.v1.json"
  - "core/python/src/watchtower_core/query/"
  - "core/python/src/watchtower_core/sync/"
related_ids:
  - "design.features.local_task_tracking_and_github_sync"
aliases:
  - "task tracking bootstrap"
---

# Establish local-first task tracking foundation

## Summary
Establishes governed local task records, a generated human tracker, a generated machine index, and Python query and sync commands for task coordination.

## Context
- The planning corpus had PRD, design, decision, and traceability tracking, but no active task execution layer.
- Multiple engineers or agents need a local task view that can be reviewed in git and later mapped to GitHub without changing the repository's planning model.

## Scope
- Add one-task-per-file local task records under `docs/planning/tasks/`.
- Add a generated task tracker and a generated task index.
- Add Python query and sync commands for task lookup and rebuild.

## Done When
- Local task records exist as a governed document family.
- `task_tracking.md` and `task_index.v1.json` are derived from the task records.
- `watchtower-core` can query tasks and rebuild the task tracker and task index.

## Links
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)

## Updated At
- `2026-03-09T14:41:51Z`
