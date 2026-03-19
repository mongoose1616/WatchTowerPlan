# Plan Routing Engine Export Foundation Implementation Slice

## Summary
Publishes a reusable routing engine package so route selection is available through a stable runtime API instead of only query helpers and CLI handlers.

## Initial Work Breakdown
- `task.plan_routing_engine_export_foundation.add_reusable_routing_engine`: Publish a stable watchtower_core.routing package for route selection by request text or task type.
- `task.plan_routing_engine_export_foundation.add_routing_engine_boundary_tests`: Prove the exported routing engine selects governed routes and remains distinct from CLI wiring.
- `task.plan_routing_engine_export_foundation.reconcile_routing_requirements`: Update requirements.md only if the exported routing engine satisfies the reusable runtime contract.

## Planned Touch Points
- `core/python/src/watchtower_core/routing/`
- `core/python/tests/unit/`
- `requirements.md`

## Validation Plan
- Add focused unit tests for request-text and explicit task-type routing through the exported package.
- Re-run route-preview and package-boundary tests so the new runtime API stays aligned with the existing governed route data.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
