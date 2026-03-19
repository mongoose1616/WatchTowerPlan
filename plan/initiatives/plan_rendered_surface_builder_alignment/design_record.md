# Plan Rendered Surface Builder Alignment Design Record

## Summary
Extracts a reusable rendered-view builder and markdown reconciliation helper, then routes live plan and project rendered surfaces through the registry-backed boundary.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_rendered_surface_builder_alignment/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
