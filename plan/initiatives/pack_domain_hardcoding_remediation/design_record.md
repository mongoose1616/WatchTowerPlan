# Pack Domain Hardcoding Remediation Design Record

## Summary
Verify and remove remaining pack-domain hardcoding, reorganize lingering legacy artifacts, and prove the pack-driven endstate.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/pack_domain_hardcoding_remediation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- `watchtower_core.control_plane` is the reusable pack-agnostic contract and loader boundary. It is not a duplicate of `watchtower_core.plan_runtime`, which remains the residual repo-local planning orchestration layer that still needs to move behind a plan-owned Python boundary under `plan/**`.
