# Plan Actor Registry And Runtime Boundary Reconciliation Implementation Slice

## Summary
Adds a reusable actor-registry helper and reconciles requirements rows for reusable-core runtime boundaries that are already implemented.

## Initial Work Breakdown
- `task.plan_actor_registry_and_runtime_boundary_reconciliation.add_actor_registry_helper`: Publish a reusable helper for actor lookup and actor-type enforcement.
- `task.plan_actor_registry_and_runtime_boundary_reconciliation.refactor_live_approval_caller`: Move initiative approval maintainer checks onto the reusable actor helper.
- `task.plan_actor_registry_and_runtime_boundary_reconciliation.reconcile_runtime_boundary_requirements`: Update requirements rows only where reusable-core surfaces are already implemented and tested.

## Planned Touch Points
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/repo_ops/initiative_packages.py`
- `core/python/tests/unit/`
- `core/python/tests/integration/`
- `requirements.md`

## Validation Plan
- Add focused unit tests for the new actor helper.
- Re-run the existing initiative approval integration coverage that depends on authorized maintainer checks.
- Re-run the reusable-core boundary tests that prove query and sync exports before updating the requirement rows.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
