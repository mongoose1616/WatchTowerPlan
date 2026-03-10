---
id: "task.workflow_system_operationalization.route_preview_and_metadata.001"
trace_id: "trace.workflow_system_operationalization"
title: "Add route preview and governed workflow metadata authority"
summary: "Move workflow retrieval metadata into governed control-plane artifacts, add a derived route index, and expose executable route preview through the CLI."
type: "task"
status: "active"
task_status: "backlog"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T21:59:21Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "workflows/ROUTING_TABLE.md"
  - "core/control_plane/"
  - "core/python/src/watchtower_core/"
  - "docs/commands/core_python/"
related_ids:
  - "prd.workflow_system_operationalization"
  - "design.features.workflow_routing_and_authoring"
  - "design.implementation.workflow_system_operationalization_execution"
depends_on:
  - "task.workflow_system_operationalization.bootstrap.001"
---

# Add route preview and governed workflow metadata authority

## Summary
Move workflow retrieval metadata into governed control-plane artifacts, add a derived route index, and expose executable route preview through the CLI.

## Scope
- Add the workflow metadata registry, route index schema, sync service, loader support, and validation coverage.
- Add `watchtower-core route preview` and companion command docs.
- Update workflow-index generation to consume governed metadata instead of Python-only constants.

## Done When
- Workflow metadata is authored under `core/control_plane/`.
- A route index can be rebuilt deterministically from `ROUTING_TABLE.md`.
- `watchtower-core route preview` returns useful human and JSON output for common requests.

## Links
- [workflow_routing_and_authoring.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_routing_and_authoring.md)
- [workflow_system_operationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/workflow_system_operationalization_execution.md)

## Updated At
- `2026-03-10T21:59:21Z`
