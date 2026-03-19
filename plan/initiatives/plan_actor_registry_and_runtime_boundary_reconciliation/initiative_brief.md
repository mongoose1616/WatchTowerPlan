# Plan Actor Registry And Runtime Boundary Reconciliation

## Summary
Adds a reusable actor-registry helper and reconciles requirements rows for reusable-core runtime boundaries that are already implemented.

## Identity
- `initiative_id`: `initiative.plan_actor_registry_and_runtime_boundary_reconciliation`
- `trace_id`: `trace.plan_actor_registry_and_runtime_boundary_reconciliation`
- `scope_type`: `pack_wide`

## Scope
- Add a reusable `ActorRegistryHelper` under `watchtower_core.control_plane` for governed actor lookup and enforcement.
- Refactor live initiative approval checks onto that helper instead of inlining actor-type and role assertions.
- Reconcile `requirements.md` rows only where reusable-core surfaces already exist, are exported at the intended boundary, and are covered by focused tests.

## Out Of Scope
- Do not mark `routing_engine`, `workflow_execution_harness`, `rebuild_harness`, `terminology_helper`, or other still-thin seams as `Current` without new runtime coverage.
- Do not broaden this slice into status-registry cleanup or other pack-vocabulary redesign beyond the actor helper and requirements reconciliation.

## Initial Task Set
- `task.plan_actor_registry_and_runtime_boundary_reconciliation.add_actor_registry_helper`: Publish a reusable helper for actor lookup and actor-type enforcement.
- `task.plan_actor_registry_and_runtime_boundary_reconciliation.refactor_live_approval_caller`: Move initiative approval maintainer checks onto the reusable actor helper.
- `task.plan_actor_registry_and_runtime_boundary_reconciliation.reconcile_runtime_boundary_requirements`: Update requirements rows only where reusable-core surfaces are already implemented and tested.
