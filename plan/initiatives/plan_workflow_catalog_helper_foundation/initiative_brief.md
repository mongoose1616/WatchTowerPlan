# Plan Workflow Catalog Helper Foundation

## Summary
Adds a reusable workflow catalog helper that joins workflow metadata, companion workflow relationships, and route membership through one typed surface.

## Identity
- `initiative_id`: `initiative.plan_workflow_catalog_helper_foundation`
- `trace_id`: `trace.plan_workflow_catalog_helper_foundation`
- `scope_type`: `pack_wide`

## Scope
- Add a reusable `WorkflowCatalogHelper` under `watchtower_core.control_plane` for joined workflow metadata lookup.
- Resolve companion workflows and route bindings from the governed workflow and route indexes through one typed helper.
- Define workflow compatibility in this slice as shared route membership, not ad hoc naming heuristics.

## Out Of Scope
- Do not introduce generic workflow execution, route selection, or new workflow registries in this slice.
- Do not mark broader routing or workflow-execution requirement rows `Current` without new runtime seams beyond the catalog helper.

## Initial Task Set
- `task.plan_workflow_catalog_helper_foundation.add_workflow_catalog_helper`: Publish a reusable helper that resolves workflow metadata, companions, and route bindings.
- `task.plan_workflow_catalog_helper_foundation.add_workflow_catalog_tests`: Prove workflow metadata, companion workflow joins, and route-derived compatibility through focused tests.
- `task.plan_workflow_catalog_helper_foundation.reconcile_workflow_helper_requirements`: Update requirements.md only if the new workflow catalog helper satisfies the reusable-core contract.
