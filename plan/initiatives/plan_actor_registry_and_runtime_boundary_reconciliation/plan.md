# Plan Actor Registry And Runtime Boundary Reconciliation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_actor_registry_and_runtime_boundary_reconciliation`
- `trace_id`: `trace.plan_actor_registry_and_runtime_boundary_reconciliation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T23:51:18Z`

## Scope and Non-Goals
Adds a reusable actor-registry helper and reconciles requirements rows for reusable-core runtime boundaries that are already implemented.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add actor registry helper: Publish a reusable helper for actor lookup and actor-type enforcement.
- Reconcile runtime boundary requirements: Update requirements rows only where reusable-core surfaces are already implemented and tested.
- Refactor live approval caller: Move initiative approval maintainer checks onto the reusable actor helper.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_actor_registry_and_runtime_boundary_reconciliation.add_actor_registry_helper](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/.wt/tasks/add_actor_registry_helper/task.json) | `completed` | `high` | `repository_maintainer` | Publish a reusable helper for actor lookup and actor-type enforcement. |
| [task.plan_actor_registry_and_runtime_boundary_reconciliation.reconcile_runtime_boundary_requirements](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/.wt/tasks/reconcile_runtime_boundary_requirements/task.json) | `completed` | `high` | `repository_maintainer` | Update requirements rows only where reusable-core surfaces are already implemented and tested. |
| [task.plan_actor_registry_and_runtime_boundary_reconciliation.refactor_live_approval_caller](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/.wt/tasks/refactor_live_approval_caller/task.json) | `completed` | `high` | `repository_maintainer` | Move initiative approval maintainer checks onto the reusable actor helper. |

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_actor_registry_and_runtime_boundary_reconciliation/summary.md)
