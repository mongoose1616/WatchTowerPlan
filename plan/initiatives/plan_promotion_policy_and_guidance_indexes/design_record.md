# Plan Promotion Policy and Guidance Indexes Design Record

## Summary
Adds the missing promotion policy registry and pack-level promotion and guidance indexes so initiative-local promotion records and approved plan guidance are machine-queryable under plan/.wt.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_promotion_policy_and_guidance_indexes/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
