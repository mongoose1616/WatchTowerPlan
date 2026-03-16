---
id: "task.core_export_readiness_and_optimization.workspace_injection.001"
trace_id: "trace.core_export_readiness_and_optimization"
title: "Inject workspace config and artifact adapters"
summary: "Replace implicit repo-root discovery with injected workspace configuration, artifact sources, and artifact stores so reusable services can run against non-WatchTowerPlan layouts."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T05:58:19Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/control_plane/"
  - "core/python/src/watchtower_core/"
  - "core/python/tests/"
related_ids:
  - "prd.core_export_readiness_and_optimization"
  - "design.features.core_export_ready_architecture"
  - "design.implementation.core_export_readiness_execution"
depends_on:
  - "task.core_export_readiness_and_optimization.repo_ops_boundary.001"
---

# Inject workspace config and artifact adapters

## Summary
Replace implicit repo-root discovery with injected workspace configuration, artifact sources, and artifact stores so reusable services can run against non-WatchTowerPlan layouts.

## Context
- The current loader and path helpers still assume the `WatchTowerPlan` repository shape directly.
- Export readiness depends on proving that reusable services can be constructed against injected boundaries instead of one fixed repo layout.

## Scope
- Add workspace and artifact adapter interfaces.
- Refactor reusable services to consume those interfaces instead of direct repo discovery.
- Add tests that instantiate reusable services against temporary or synthetic workspace layouts.

## Done When
- Reusable services can run without implicit repo-root discovery.
- Loader and coordination behavior is validated against injected workspace configuration in tests.

## Links
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_export_readiness_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_readiness_execution.md)
- [control_plane_loaders_and_schema_store.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/control_plane_loaders_and_schema_store.md)

## Updated At
- `2026-03-10T05:58:19Z`
