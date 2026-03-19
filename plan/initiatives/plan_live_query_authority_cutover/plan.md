# Plan Live Query Authority Cutover Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_live_query_authority_cutover`
- `trace_id`: `trace.plan_live_query_authority_cutover`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T19:38:14Z`

## Scope and Non-Goals
Cuts planning query authority over to the live plan workspace indexes and exposes the missing readiness, discrepancy, and project query surfaces required by requirements.md and decisions.md.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add readiness discrepancy and project query commands: Expose the live readiness, discrepancy, and project index surfaces through first-class query commands and payloads.
- Refresh docs and validate live query cutover: Update command docs, authority guidance, and regression coverage so the public query surface matches the plan/.wt authority model.
- Reroot public planning queries onto live plan indexes: Move the public coordination, initiatives, tasks, and authority query path from legacy docs-backed planning indexes to the authoritative plan/.wt indexes and rendered surfaces.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_live_query_authority_cutover.add_readiness_discrepancy_and_project_query_commands](/plan/initiatives/plan_live_query_authority_cutover/.wt/tasks/add_readiness_discrepancy_and_project_query_commands/task.json) | `completed` | `high` | `repository_maintainer` | Expose the live readiness, discrepancy, and project index surfaces through first-class query commands and payloads. | task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes |
| [task.plan_live_query_authority_cutover.refresh_docs_and_validate_live_query_cutover](/plan/initiatives/plan_live_query_authority_cutover/.wt/tasks/refresh_docs_and_validate_live_query_cutover/task.json) | `completed` | `high` | `repository_maintainer` | Update command docs, authority guidance, and regression coverage so the public query surface matches the plan/.wt authority model. | task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes, task.plan_live_query_authority_cutover.add_readiness_discrepancy_and_project_query_commands |
| [task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes](/plan/initiatives/plan_live_query_authority_cutover/.wt/tasks/reroot_public_planning_queries_onto_live_plan_indexes/task.json) | `completed` | `high` | `repository_maintainer` | Move the public coordination, initiatives, tasks, and authority query path from legacy docs-backed planning indexes to the authoritative plan/.wt indexes and rendered surfaces. | - |

## Dependencies and Risks
- Discrepancy `discrepancy.plan_live_query_authority_cutover.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.plan_live_query_authority_cutover.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.plan_live_query_authority_cutover.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_live_query_authority_cutover/plan.md.
- Discrepancy `discrepancy.plan_live_query_authority_cutover.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.plan_live_query_authority_cutover.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_live_query_authority_cutover/progress.md.
- Discrepancy `discrepancy.plan_live_query_authority_cutover.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.plan_live_query_authority_cutover.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/plan_live_query_authority_cutover/summary.md.
- Discrepancy `discrepancy.plan_live_query_authority_cutover.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.
- Task `task.plan_live_query_authority_cutover.add_readiness_discrepancy_and_project_query_commands` depends on `task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes`.
- Task `task.plan_live_query_authority_cutover.refresh_docs_and_validate_live_query_cutover` depends on `task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes`, `task.plan_live_query_authority_cutover.add_readiness_discrepancy_and_project_query_commands`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_live_query_authority_cutover/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_live_query_authority_cutover/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_live_query_authority_cutover/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_live_query_authority_cutover/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_live_query_authority_cutover/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_live_query_authority_cutover/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_live_query_authority_cutover/summary.md)
