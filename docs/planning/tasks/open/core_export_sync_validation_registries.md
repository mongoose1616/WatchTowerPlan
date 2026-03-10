---
id: "task.core_export_readiness_and_optimization.sync_validation_registries.001"
trace_id: "trace.core_export_readiness_and_optimization"
title: "Replace manual sync and validation enumerations with registries"
summary: "Introduce governed sync-family and validation-family registries so orchestration, listing, and coverage checks no longer depend on duplicated manual enumerations."
type: "task"
status: "active"
task_status: "backlog"
task_kind: "feature"
priority: "medium"
owner: "repository_maintainer"
updated_at: "2026-03-10T04:28:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/sync/"
  - "core/python/src/watchtower_core/validation/"
  - "docs/commands/core_python/"
related_ids:
  - "prd.core_export_readiness_and_optimization"
  - "design.features.core_export_ready_architecture"
  - "design.implementation.core_export_readiness_execution"
depends_on:
  - "task.core_export_readiness_and_optimization.command_registry.001"
---

# Replace manual sync and validation enumerations with registries

## Summary
Introduce governed sync-family and validation-family registries so orchestration, listing, and coverage checks no longer depend on duplicated manual enumerations.

## Context
- `sync all` and `validate all` currently centralize maintenance through manual family lists.
- The same authority pattern needed for command registration should also reduce duplication in sync and validation orchestration.

## Scope
- Add sync-family and validation-family registries.
- Move orchestration, coverage checks, and related docs alignment to registry-backed flows.
- Preserve current deterministic execution order and fail-closed validation behavior.

## Done When
- New sync and validation families are registered through one canonical path.
- Aggregate sync and validation flows no longer require parallel manual enumerations to stay correct.

## Links
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_export_readiness_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_readiness_execution.md)
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md)

## Updated At
- `2026-03-10T04:28:34Z`
