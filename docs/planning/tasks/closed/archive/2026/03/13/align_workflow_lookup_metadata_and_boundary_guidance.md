---
id: task.workflow_route_boundary_discoverability_hardening.workflow_lookup_alignment.003
trace_id: trace.workflow_route_boundary_discoverability_hardening
title: Align workflow lookup metadata and boundary guidance
summary: Refresh workflow trigger metadata, adjacent workflow guidance, command docs,
  and derived workflow-index surfaces so workflow lookup reinforces the same route
  boundaries as route preview.
type: task
status: active
task_status: done
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T21:37:07Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/query/workflows.py
- core/control_plane/registries/workflows/workflow_metadata_registry.v1.json
- core/control_plane/indexes/workflows/workflow_index.v1.json
- docs/commands/core_python/watchtower_core_route_preview.md
- docs/commands/core_python/watchtower_core_query_workflows.md
- workflows/modules/
related_ids:
- prd.workflow_route_boundary_discoverability_hardening
- design.features.workflow_route_boundary_discoverability_hardening
- design.implementation.workflow_route_boundary_discoverability_hardening
- decision.workflow_route_boundary_discoverability_hardening_direction
- contract.acceptance.workflow_route_boundary_discoverability_hardening
depends_on:
- task.workflow_route_boundary_discoverability_hardening.bootstrap.001
---

# Align workflow lookup metadata and boundary guidance

## Summary
Refresh workflow trigger metadata, adjacent workflow guidance, command docs, and derived workflow-index surfaces so workflow lookup reinforces the same route boundaries as route preview.

## Scope
- Review the workflow-query lookup surface, the adjacent workflow modules, and the workflow metadata registry for missing boundary-discovery terms.
- Refresh the workflow metadata, workflow-query behavior or docs, and the companion command guidance so realistic adjacent-route lookup terms become discoverable.
- Keep the workflow metadata registry, derived workflow index, and direct command docs aligned in the same change set.

## Done When
- Workflow lookup surfaces can surface the adjacent reconciliation and task routes through realistic query terms used in this trace.
- The route-preview and workflow-query command docs explain the adjacent route boundaries consistently.
- Focused workflow-query and workflow-index regressions cover the updated behavior and pass.
