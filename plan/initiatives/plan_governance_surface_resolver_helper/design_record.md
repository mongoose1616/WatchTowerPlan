# Plan Governance Surface Resolver Helper Design Record

## Summary
Adds the missing governance surface resolver helper so pack and core governed surfaces can be resolved through one typed query surface instead of scattered loader and registry logic.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_governance_surface_resolver_helper/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
