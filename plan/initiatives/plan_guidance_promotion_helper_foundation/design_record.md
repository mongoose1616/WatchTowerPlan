# Plan Guidance Promotion Helper Foundation Design Record

## Summary
Adds governed promotion-policy and guidance-promotion helpers, then extracts approved initiative-local outputs into durable plan/docs guidance surfaces so requirements.md and decisions.md no longer stop at promotion shells.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_guidance_promotion_helper_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
