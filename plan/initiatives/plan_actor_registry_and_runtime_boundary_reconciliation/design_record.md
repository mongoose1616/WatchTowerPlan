# Plan Actor Registry And Runtime Boundary Reconciliation Design Record

## Summary
Adds a reusable actor-registry helper and reconciles requirements rows for reusable-core runtime boundaries that are already implemented.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Design Notes
- `ActorRegistryHelper` should load the active governed actor registry through the same pack-aware loader flow as other reusable control-plane helpers.
- The helper should expose exact lookup plus validation helpers for actor type, role, and scope so live callers do not keep reimplementing actor-policy checks.
- `requirements.md` should only move rows from `Partial` to `Current` when the reusable-core package boundary, public exports, and focused tests already support the claimed endstate.
- This slice should prefer requirements reconciliation over new wrapper code when a reusable surface already exists and the contract is merely stale.
