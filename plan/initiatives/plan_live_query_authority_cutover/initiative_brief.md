# Plan Live Query Authority Cutover

## Summary
Cuts planning query authority over to the live plan workspace indexes and exposes the missing readiness, discrepancy, and project query surfaces required by requirements.md and decisions.md.

## Identity
- `initiative_id`: `initiative.plan_live_query_authority_cutover`
- `trace_id`: `trace.plan_live_query_authority_cutover`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_live_query_authority_cutover.reroot_public_planning_queries_onto_live_plan_indexes`: Move the public coordination, initiatives, tasks, and authority query path from legacy docs-backed planning indexes to the authoritative plan/.wt indexes and rendered surfaces.
- `task.plan_live_query_authority_cutover.add_readiness_discrepancy_and_project_query_commands`: Expose the live readiness, discrepancy, and project index surfaces through first-class query commands and payloads.
- `task.plan_live_query_authority_cutover.refresh_docs_and_validate_live_query_cutover`: Update command docs, authority guidance, and regression coverage so the public query surface matches the plan/.wt authority model.
