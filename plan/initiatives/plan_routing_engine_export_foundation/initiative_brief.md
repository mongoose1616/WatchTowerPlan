# Plan Routing Engine Export Foundation

## Summary
Publishes a reusable routing engine package so route selection is available through a stable runtime API instead of only query helpers and CLI handlers.

## Identity
- `initiative_id`: `initiative.plan_routing_engine_export_foundation`
- `trace_id`: `trace.plan_routing_engine_export_foundation`
- `scope_type`: `pack_wide`

## Scope
- Add a stable `watchtower_core.routing` package that selects governed routes by request text or explicit task type.
- Keep the runtime contract typed and reusable instead of routing callers through CLI handlers.
- Reconcile only the routing requirement rows that the exported runtime package and focused tests actually prove.

## Out Of Scope
- Do not introduce workflow execution, new routing metadata, or pack-specific route policies in this slice.
- Do not widen the slice into generic workflow execution or route-authoring changes.

## Initial Task Set
- `task.plan_routing_engine_export_foundation.add_reusable_routing_engine`: Publish a stable watchtower_core.routing package for route selection by request text or task type.
- `task.plan_routing_engine_export_foundation.add_routing_engine_boundary_tests`: Prove the exported routing engine selects governed routes and remains distinct from CLI wiring.
- `task.plan_routing_engine_export_foundation.reconcile_routing_requirements`: Update requirements.md only if the exported routing engine satisfies the reusable runtime contract.
