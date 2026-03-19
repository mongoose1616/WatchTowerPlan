# Plan Routing Engine Export Foundation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_routing_engine_export_foundation`
- `trace_id`: `trace.plan_routing_engine_export_foundation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T23:58:50Z`

## Scope and Non-Goals
Publishes a reusable routing engine package so route selection is available through a stable runtime API instead of only query helpers and CLI handlers.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add reusable routing engine: Publish a stable watchtower_core.routing package for route selection by request text or task type.
- Add routing engine boundary tests: Prove the exported routing engine selects governed routes and remains distinct from CLI wiring.
- Reconcile routing requirements: Update requirements.md only if the exported routing engine satisfies the reusable runtime contract.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_routing_engine_export_foundation.add_reusable_routing_engine](/plan/initiatives/plan_routing_engine_export_foundation/.wt/tasks/add_reusable_routing_engine/task.json) | `completed` | `high` | `repository_maintainer` | Publish a stable watchtower_core.routing package for route selection by request text or task type. |
| [task.plan_routing_engine_export_foundation.add_routing_engine_boundary_tests](/plan/initiatives/plan_routing_engine_export_foundation/.wt/tasks/add_routing_engine_boundary_tests/task.json) | `completed` | `high` | `repository_maintainer` | Prove the exported routing engine selects governed routes and remains distinct from CLI wiring. |
| [task.plan_routing_engine_export_foundation.reconcile_routing_requirements](/plan/initiatives/plan_routing_engine_export_foundation/.wt/tasks/reconcile_routing_requirements/task.json) | `completed` | `high` | `repository_maintainer` | Update requirements.md only if the exported routing engine satisfies the reusable runtime contract. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `3`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/plan_routing_engine_export_foundation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_routing_engine_export_foundation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_routing_engine_export_foundation/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_routing_engine_export_foundation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_routing_engine_export_foundation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_routing_engine_export_foundation/summary.md)
