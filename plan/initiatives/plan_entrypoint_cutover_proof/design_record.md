# Plan Entrypoint Cutover Proof Design Record

## Summary
Proves the pack-wide capture-first flow for the plan authority cutover.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_entrypoint_cutover_proof/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
