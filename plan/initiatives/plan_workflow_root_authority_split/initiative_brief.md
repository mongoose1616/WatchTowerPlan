# Plan Workflow Root Authority Split

## Summary
Moves workflow-routing and workflow-module authority out of repo-root workflows/ into core/workflows/ and plan/workflows/, with route and workflow indexes rebuilt from the split roots required by requirements.md and decisions.md.

## Identity
- `initiative_id`: `initiative.plan_workflow_root_authority_split`
- `trace_id`: `trace.plan_workflow_root_authority_split`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_workflow_root_authority_split.split_workflow_routing_and_module_roots_by_domain`: Move shared reusable workflow modules under core/workflows/ and plan-specific modules under plan/workflows/, then convert repo-root workflows/ into a thin compatibility surface.
- `task.plan_workflow_root_authority_split.rebuild_routing_and_workflow_runtime_around_split_roots`: Update route preview, route index, workflow index, repository-path inventory, and validation target discovery so the machine runtime resolves core/workflows/ and plan/workflows/ as authoritative.
- `task.plan_workflow_root_authority_split.cut_over_human_instructions_and_workflow_guidance`: Update AGENTS, README, policy, registry, and standards surfaces so human routing no longer treats repo-root workflows/ as the authoritative backend.
