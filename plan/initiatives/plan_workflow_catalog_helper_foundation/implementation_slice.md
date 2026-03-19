# Plan Workflow Catalog Helper Foundation Implementation Slice

## Summary
Adds a reusable workflow catalog helper that joins workflow metadata, companion workflow relationships, and route membership through one typed surface.

## Initial Work Breakdown
- `task.plan_workflow_catalog_helper_foundation.add_workflow_catalog_helper`: Publish a reusable helper that resolves workflow metadata, companions, and route bindings.
- `task.plan_workflow_catalog_helper_foundation.add_workflow_catalog_tests`: Prove workflow metadata, companion workflow joins, and route-derived compatibility through focused tests.
- `task.plan_workflow_catalog_helper_foundation.reconcile_workflow_helper_requirements`: Update requirements.md only if the new workflow catalog helper satisfies the reusable-core contract.

## Planned Touch Points
- `core/python/src/watchtower_core/control_plane/`
- `core/python/tests/unit/`
- `requirements.md`

## Validation Plan
- Add focused unit tests for workflow metadata lookup, companion workflow resolution, route membership, and shared-route compatibility.
- Re-run the existing reusable query and route-preview tests so the helper lands without drifting adjacent workflow surfaces.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
