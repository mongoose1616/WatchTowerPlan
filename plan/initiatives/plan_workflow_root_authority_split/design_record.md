# Plan Workflow Root Authority Split Design Record

## Summary
Moves workflow-routing and workflow-module authority out of repo-root workflows/ into core/workflows/ and plan/workflows/, with route and workflow indexes rebuilt from the split roots required by requirements.md and decisions.md.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_workflow_root_authority_split/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
