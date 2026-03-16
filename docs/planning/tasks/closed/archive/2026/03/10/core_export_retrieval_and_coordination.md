---
id: "task.core_export_readiness_and_optimization.retrieval_and_coordination.001"
trace_id: "trace.core_export_readiness_and_optimization"
title: "Add retrieval metadata and coordination slice orchestration"
summary: "Extend retrieval indexes with stronger authority hints and add a deterministic coordination rebuild slice for task, traceability, and initiative surfaces."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "medium"
owner: "repository_maintainer"
updated_at: "2026-03-10T06:26:48Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/indexes/repository_paths/"
  - "core/control_plane/indexes/workflows/"
  - "core/python/src/watchtower_core/sync/"
  - "core/python/src/watchtower_core/query/"
related_ids:
  - "prd.core_export_readiness_and_optimization"
  - "design.features.core_export_ready_architecture"
  - "design.implementation.core_export_readiness_execution"
depends_on:
  - "task.core_export_readiness_and_optimization.repo_ops_boundary.001"
  - "task.core_export_readiness_and_optimization.sync_validation_registries.001"
---

# Add retrieval metadata and coordination slice orchestration

## Summary
Extend retrieval indexes with stronger authority hints and add a deterministic coordination rebuild slice for task, traceability, and initiative surfaces.

## Context
- Humans and agents still depend too much on README fan-out and implicit knowledge to find authoritative surfaces quickly.
- Task, traceability, and initiative rebuilds are coherent today, but the deterministic path still lives in code rather than as an obvious orchestration slice.

## Scope
- Extend repository-path and workflow-index metadata with retrieval-oriented ranking hints.
- Add or expose a deterministic coordination rebuild command or slice for task and initiative surfaces.
- Update query behavior and operator guidance so the new metadata actually improves retrieval.

## Done When
- Retrieval surfaces distinguish authoritative entrypoints from boundary or scaffold surfaces more clearly.
- Task-state and initiative rebuild behavior has one obvious deterministic path instead of several implied steps.

## Links
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_export_readiness_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_readiness_execution.md)
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)

## Updated At
- `2026-03-10T06:26:48Z`
