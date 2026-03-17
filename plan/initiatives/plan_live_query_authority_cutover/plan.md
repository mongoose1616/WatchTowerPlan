# Plan Live Query Authority Cutover Plan

## Summary
Cuts planning query authority over to the live plan workspace indexes and exposes the missing readiness, discrepancy, and project query surfaces required by requirements.md and decisions.md.

## Identity
- `initiative_id`: `initiative.plan_live_query_authority_cutover`
- `trace_id`: `trace.plan_live_query_authority_cutover`
- `scope_type`: `pack_wide`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`

## Task Plan
- `task.plan_live_query_authority_cutover.add_readiness_discrepancy_and_project_query_commands`: `completed` (high)
- `task.plan_live_query_authority_cutover.refresh_docs_and_validate_live_query_cutover`: `completed` (high)
- `task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes`: `completed` (high)

## Deferred Items
- None.
