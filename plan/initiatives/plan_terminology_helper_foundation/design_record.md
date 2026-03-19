# Plan Terminology Helper Foundation Design Record

## Summary
Generalize the existing planning vocabulary seam into a reusable terminology helper with pack-local lookup, alias resolution, and deprecation awareness.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_terminology_helper_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
