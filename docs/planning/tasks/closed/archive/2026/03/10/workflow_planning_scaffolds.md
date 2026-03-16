---
id: task.workflow_system_operationalization.planning_scaffolds.001
trace_id: trace.workflow_system_operationalization
title: Add compact planning scaffold commands
summary: Expose lean CLI scaffolds for PRDs, feature designs, implementation plans,
  decisions, and initiative bootstrap using the current repo templates.
type: task
status: active
task_status: done
task_kind: feature
priority: medium
owner: repository_maintainer
updated_at: '2026-03-10T23:17:55Z'
audience: shared
authority: authoritative
applies_to:
- docs/templates/
- docs/planning/
- core/python/src/watchtower_core/
- docs/commands/core_python/
related_ids:
- prd.workflow_system_operationalization
- design.features.workflow_routing_and_authoring
- design.implementation.workflow_system_operationalization_execution
depends_on:
- task.workflow_system_operationalization.bootstrap.001
---

# Add compact planning scaffold commands

## Summary
Expose lean CLI scaffolds for PRDs, feature designs, implementation plans, decisions, and initiative bootstrap using the current repo templates.

## Scope
- Add a planning command family for bounded template-driven scaffolds.
- Keep generated output compact and aligned with current standards and templates.
- Cover the main pre-implementation planning artifact families plus one initiative-bootstrap flow.

## Done When
- The CLI can scaffold the main planning artifact families without hand-copying templates.
- The generated files use current IDs, paths, and template structure.
- Command docs and tests cover the new scaffold surface.

## Links
- [workflow_routing_and_authoring.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_routing_and_authoring.md)
- [workflow_system_operationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/workflow_system_operationalization_execution.md)

## Updated At
- `2026-03-10T23:17:55Z`
