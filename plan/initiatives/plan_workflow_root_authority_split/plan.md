# Plan Workflow Root Authority Split Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_workflow_root_authority_split`
- `trace_id`: `trace.plan_workflow_root_authority_split`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T18:55:30Z`

## Scope and Non-Goals
Moves workflow-routing and workflow-module authority out of repo-root workflows/ into core/workflows/ and plan/workflows/, with route and workflow indexes rebuilt from the split roots required by requirements.md and decisions.md.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Cut over human instructions and workflow guidance: Update AGENTS, README, policy, registry, and standards surfaces so human routing no longer treats repo-root workflows/ as the authoritative backend.
- Rebuild routing and workflow runtime around split roots: Update route preview, route index, workflow index, repository-path inventory, and validation target discovery so the machine runtime resolves core/workflows/ and plan/workflows/ as authoritative.
- Split workflow routing and module roots by domain: Move shared reusable workflow modules under core/workflows/ and plan-specific modules under plan/workflows/, then convert repo-root workflows/ into a thin compatibility surface.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_workflow_root_authority_split.cut_over_human_instructions_and_workflow_guidance](/plan/initiatives/plan_workflow_root_authority_split/.wt/tasks/cut_over_human_instructions_and_workflow_guidance/task.json) | `completed` | `high` | `repository_maintainer` | Update AGENTS, README, policy, registry, and standards surfaces so human routing no longer treats repo-root workflows/ as the authoritative backend. | task.plan_workflow_root_authority_split.split_workflow_routing_and_module_roots_by_domain, task.plan_workflow_root_authority_split.rebuild_routing_and_workflow_runtime_around_split_roots |
| [task.plan_workflow_root_authority_split.rebuild_routing_and_workflow_runtime_around_split_roots](/plan/initiatives/plan_workflow_root_authority_split/.wt/tasks/rebuild_routing_and_workflow_runtime_around_split_roots/task.json) | `completed` | `high` | `repository_maintainer` | Update route preview, route index, workflow index, repository-path inventory, and validation target discovery so the machine runtime resolves core/workflows/ and plan/workflows/ as authoritative. | task.plan_workflow_root_authority_split.split_workflow_routing_and_module_roots_by_domain |
| [task.plan_workflow_root_authority_split.split_workflow_routing_and_module_roots_by_domain](/plan/initiatives/plan_workflow_root_authority_split/.wt/tasks/split_workflow_routing_and_module_roots_by_domain/task.json) | `completed` | `high` | `repository_maintainer` | Move shared reusable workflow modules under core/workflows/ and plan-specific modules under plan/workflows/, then convert repo-root workflows/ into a thin compatibility surface. | - |

## Dependencies and Risks
- Task `task.plan_workflow_root_authority_split.cut_over_human_instructions_and_workflow_guidance` depends on `task.plan_workflow_root_authority_split.split_workflow_routing_and_module_roots_by_domain`, `task.plan_workflow_root_authority_split.rebuild_routing_and_workflow_runtime_around_split_roots`.
- Task `task.plan_workflow_root_authority_split.rebuild_routing_and_workflow_runtime_around_split_roots` depends on `task.plan_workflow_root_authority_split.split_workflow_routing_and_module_roots_by_domain`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_workflow_root_authority_split/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_workflow_root_authority_split/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_workflow_root_authority_split/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_workflow_root_authority_split/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_workflow_root_authority_split/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_workflow_root_authority_split/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_workflow_root_authority_split/summary.md)
