---
id: "task.local_task_tracking.github_sync.001"
trace_id: "trace.local_task_tracking"
title: "Add GitHub task sync support"
summary: "Adds one-way GitHub sync support so local task records can publish to GitHub issues and project items without changing local task identity."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "medium"
owner: "repository_maintainer"
updated_at: "2026-03-09T16:14:14Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/tasks/task_index.v1.json"
  - "core/python/src/watchtower_core/sync/"
related_ids:
  - "design.features.local_task_tracking_and_github_sync"
aliases:
  - "github task sync"
  - "github issue sync"
---

# Add GitHub task sync support

## Summary
Adds one-way GitHub sync support so local task records can publish to GitHub issues and project items without changing local task identity.

## Context
- The repository now has a local-first task model, but GitHub remains the likely shared execution surface once multiple engineers need a hosted board.
- The local task records already reserve optional GitHub foreign-key fields, but there is no sync workflow yet.

## Scope
- Define the first GitHub push-only sync contract from local task records to GitHub issues and project items.
- Keep local task records as the authoritative source of truth during the first sync phase.

## Done When
- A documented sync design exists.
- The repository can push local task metadata to GitHub without rewriting local task IDs.
- Sync mappings between local task status and GitHub status fields are explicit.

## Links
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)

## Updated At
- `2026-03-09T16:14:14Z`
