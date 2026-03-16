---
id: "task.core_export_readiness_and_optimization.pack_interfaces.001"
trace_id: "trace.core_export_readiness_and_optimization"
title: "Publish generic pack-facing interfaces"
summary: "Add generic pack-facing schemas, examples, and validation hooks for work-item notes, extraction outputs, promoted knowledge, promotion records, and pack indexes without starting domain-pack implementation."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T06:42:17Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/schemas/interfaces/"
  - "core/control_plane/examples/"
  - "core/control_plane/registries/schema_catalog/"
  - "core/python/src/watchtower_core/"
related_ids:
  - "prd.core_export_readiness_and_optimization"
  - "design.features.core_export_ready_architecture"
  - "design.implementation.core_export_readiness_execution"
depends_on:
  - "task.core_export_readiness_and_optimization.repo_ops_boundary.001"
  - "task.core_export_readiness_and_optimization.workspace_injection.001"
---

# Publish generic pack-facing interfaces

## Summary
Add generic pack-facing schemas, examples, and validation hooks for work-item notes, extraction outputs, promoted knowledge, promotion records, and pack indexes without starting domain-pack implementation.

## Context
- Future WatchTower product work needs stable generic contracts before a CTF-oriented pack can be built cleanly.
- The contracts have to land after the reusable versus repo-ops boundary is explicit so they are placed in the right core layer.

## Scope
- Add pack-facing interface schemas, examples, and catalog updates under `core/control_plane/`.
- Add only generic shared contracts and provenance fields, not domain-pack runtime content or scaffolding.
- Update validation surfaces that need to understand the new contracts.

## Done When
- The future pack-facing interface set exists as governed control-plane surfaces with examples.
- The interfaces are generic enough to support future CTF product work without importing domain-specific content into shared core.

## Links
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_export_readiness_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_readiness_execution.md)
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md)

## Updated At
- `2026-03-10T06:42:17Z`
