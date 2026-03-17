# Plan Workflow Root Authority Split Plan

## Summary
Moves workflow-routing and workflow-module authority out of repo-root workflows/ into core/workflows/ and plan/workflows/, with route and workflow indexes rebuilt from the split roots required by requirements.md and decisions.md.

## Identity
- `initiative_id`: `initiative.plan_workflow_root_authority_split`
- `trace_id`: `trace.plan_workflow_root_authority_split`
- `scope_type`: `pack_wide`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`

## Task Plan
- `task.plan_workflow_root_authority_split.cut_over_human_instructions_and_workflow_guidance`: `completed` (high)
- `task.plan_workflow_root_authority_split.rebuild_routing_and_workflow_runtime_around_split_roots`: `completed` (high)
- `task.plan_workflow_root_authority_split.split_workflow_routing_and_module_roots_by_domain`: `completed` (high)

## Deferred Items
- None.
