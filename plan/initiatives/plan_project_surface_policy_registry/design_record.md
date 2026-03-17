# Plan Project Surface Policy Registry Design Record

## Summary
Adds the missing project-surface policy registry plus helper-backed project validation so project containers follow a declared surface contract instead of hardcoded assumptions.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_project_surface_policy_registry/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
