# Plan Live Query Authority Cutover Progress

## Gate State
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`

## Task Status
- `task.plan_live_query_authority_cutover.add_readiness_discrepancy_and_project_query_commands`: `completed` (high)
- `task.plan_live_query_authority_cutover.refresh_docs_and_validate_live_query_cutover`: `completed` (high)
- `task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes`: `completed` (high)

## Discrepancies
- `discrepancy.plan_live_query_authority_cutover.coordination_index_index_drift`: `resolved` / `stale_aggregate_index`
- `discrepancy.plan_live_query_authority_cutover.initiative_index_index_drift`: `resolved` / `stale_aggregate_index`
- `discrepancy.plan_live_query_authority_cutover.plan_surface_drift`: `resolved` / `stale_rendered_surface`
- `discrepancy.plan_live_query_authority_cutover.plan_overview_surface_drift`: `resolved` / `stale_rendered_surface`
- `discrepancy.plan_live_query_authority_cutover.progress_surface_drift`: `resolved` / `stale_rendered_surface`
- `discrepancy.plan_live_query_authority_cutover.readiness_index_index_drift`: `resolved` / `stale_aggregate_index`
- `discrepancy.plan_live_query_authority_cutover.summary_surface_drift`: `resolved` / `stale_rendered_surface`
- `discrepancy.plan_live_query_authority_cutover.task_index_index_drift`: `resolved` / `stale_aggregate_index`
