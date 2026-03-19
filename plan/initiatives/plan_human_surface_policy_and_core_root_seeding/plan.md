# Plan Human Surface Policy and Core Root Seeding Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_human_surface_policy_and_core_root_seeding`
- `trace_id`: `trace.plan_human_surface_policy_and_core_root_seeding`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T15:06:10Z`

## Scope and Non-Goals
Adds the governed human-surface policy contract, the helper and validation path that resolve those rules, and the missing core-owned human roots that requirements.md declares as required.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add human-surface policy contract and helper: Add the human_surface_policy_registry schema, registry, typed loader support, and a helper that resolves required, optional, and forbidden human surfaces by root.
- Seed missing core human roots and router surfaces: Create the missing core/, core/docs/, and core/workflows/ entrypoint surfaces and any thin router files required by the new human-surface policy.
- Validate human-surface policy and root compliance: Add focused tests and validation coverage proving the registry, helper, and current repo roots conform to requirements.md and decisions.md.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_human_surface_policy_and_core_root_seeding.add_human_surface_policy_contract_and_helper](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/.wt/tasks/add_human_surface_policy_contract_and_helper/task.json) | `completed` | `high` | `repository_maintainer` | Add the human_surface_policy_registry schema, registry, typed loader support, and a helper that resolves required, optional, and forbidden human surfaces by root. | - |
| [task.plan_human_surface_policy_and_core_root_seeding.seed_missing_core_human_roots_and_router_surfaces](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/.wt/tasks/seed_missing_core_human_roots_and_router_surfaces/task.json) | `completed` | `high` | `repository_maintainer` | Create the missing core/, core/docs/, and core/workflows/ entrypoint surfaces and any thin router files required by the new human-surface policy. | - |
| [task.plan_human_surface_policy_and_core_root_seeding.validate_human_surface_policy_and_root_compliance](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/.wt/tasks/validate_human_surface_policy_and_root_compliance/task.json) | `completed` | `high` | `repository_maintainer` | Add focused tests and validation coverage proving the registry, helper, and current repo roots conform to requirements.md and decisions.md. | task.plan_human_surface_policy_and_core_root_seeding.add_human_surface_policy_contract_and_helper, task.plan_human_surface_policy_and_core_root_seeding.seed_missing_core_human_roots_and_router_surfaces |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.discrepancy_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/discrepancy_index.json.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_human_surface_policy_and_core_root_seeding/plan.md.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_human_surface_policy_and_core_root_seeding/progress.md.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_human_surface_policy_and_core_root_seeding/summary.md.
- Discrepancy `discrepancy.plan_human_surface_policy_and_core_root_seeding.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.
- Task `task.plan_human_surface_policy_and_core_root_seeding.validate_human_surface_policy_and_root_compliance` depends on `task.plan_human_surface_policy_and_core_root_seeding.add_human_surface_policy_contract_and_helper`, `task.plan_human_surface_policy_and_core_root_seeding.seed_missing_core_human_roots_and_router_surfaces`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_human_surface_policy_and_core_root_seeding/summary.md)
