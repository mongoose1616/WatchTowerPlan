# Plan Discrepancy Helper Foundation Design Record

## Summary
Extracts a reusable discrepancy helper for governed discrepancy records and refactors live plan initiative and workspace drift handling onto it so requirements.md and decisions.md no longer rely on ad hoc repo-local discrepancy logic.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_discrepancy_helper_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
