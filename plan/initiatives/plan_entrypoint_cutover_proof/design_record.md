# Plan Entrypoint Cutover Proof Design Record

## Summary
Proves the pack-wide capture-first flow for the plan authority cutover.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_entrypoint_cutover_proof/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The plan-domain human start-here should become visible inside `plan/` even before the full workflow-root migration is complete.
- `plan/workflows/` should exist as the human workflow entrypoint for the plan domain, but this slice should keep the actual routing table and workflow modules at the repo root to avoid mixing a documentation cutover with a larger workflow-runtime move.
- Root router surfaces may point humans toward `plan/**`, but they must not stop acknowledging the current canonical routing backend at `workflows/ROUTING_TABLE.md`.
