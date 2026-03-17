# Plan Live Query Authority Cutover Design Record

## Summary
Cuts planning query authority over to the live plan workspace indexes and exposes the missing readiness, discrepancy, and project query surfaces required by requirements.md and decisions.md.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_live_query_authority_cutover/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
