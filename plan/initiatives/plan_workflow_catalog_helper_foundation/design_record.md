# Plan Workflow Catalog Helper Foundation Design Record

## Summary
Adds a reusable workflow catalog helper that joins workflow metadata, companion workflow relationships, and route membership through one typed surface.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_workflow_catalog_helper_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Design Notes
- The helper should load the governed workflow index, route index, and workflow metadata registry through the reusable control-plane loader.
- Companion workflow resolution should fail closed when a declared companion id is missing from the workflow index.
- Route relationships should be derived from `required_workflow_ids` rather than duplicating route data into another registry.
- Compatibility in this slice means other workflows that participate in at least one of the same routed task types as the target workflow.
