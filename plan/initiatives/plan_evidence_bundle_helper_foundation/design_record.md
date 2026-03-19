# Plan Evidence Bundle Helper Foundation Design Record

## Summary
Broaden watchtower_core.evidence with a reusable evidence-bundle helper, then route live plan evidence bootstrap and indexing through that boundary.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_evidence_bundle_helper_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
