# Plan Project Surface Policy Registry Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_project_surface_policy_registry`
- `trace_id`: `trace.plan_project_surface_policy_registry`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T17:28:00Z`

## Scope and Non-Goals
Adds the missing project-surface policy registry plus helper-backed project validation so project containers follow a declared surface contract instead of hardcoded assumptions.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Publish project surface policy registry schema: Add the governed schema contract for the plan-owned project surface policy registry.
- Seed project surface policy entries: Seed active policy entries covering required machine artifacts, rendered project views, and allowed optional project-local roots.
- Wire helper and project validation: Add typed loader support, a project surface policy helper, and validation coverage that uses the new registry.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_project_surface_policy_registry.publish_project_surface_policy_registry_schema](/plan/initiatives/plan_project_surface_policy_registry/.wt/tasks/publish_project_surface_policy_registry_schema/task.json) | `completed` | `high` | `repository_maintainer` | Add the governed schema contract for the plan-owned project surface policy registry. | - |
| [task.plan_project_surface_policy_registry.seed_project_surface_policy_entries](/plan/initiatives/plan_project_surface_policy_registry/.wt/tasks/seed_project_surface_policy_entries/task.json) | `completed` | `high` | `repository_maintainer` | Seed active policy entries covering required machine artifacts, rendered project views, and allowed optional project-local roots. | task.plan_project_surface_policy_registry.publish_project_surface_policy_registry_schema |
| [task.plan_project_surface_policy_registry.wire_helper_and_project_validation](/plan/initiatives/plan_project_surface_policy_registry/.wt/tasks/wire_helper_and_project_validation/task.json) | `completed` | `high` | `repository_maintainer` | Add typed loader support, a project surface policy helper, and validation coverage that uses the new registry. | task.plan_project_surface_policy_registry.publish_project_surface_policy_registry_schema, task.plan_project_surface_policy_registry.seed_project_surface_policy_entries |

## Dependencies and Risks
- Task `task.plan_project_surface_policy_registry.seed_project_surface_policy_entries` depends on `task.plan_project_surface_policy_registry.publish_project_surface_policy_registry_schema`.
- Task `task.plan_project_surface_policy_registry.wire_helper_and_project_validation` depends on `task.plan_project_surface_policy_registry.publish_project_surface_policy_registry_schema`, `task.plan_project_surface_policy_registry.seed_project_surface_policy_entries`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_project_surface_policy_registry/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_project_surface_policy_registry/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_project_surface_policy_registry/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_project_surface_policy_registry/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_project_surface_policy_registry/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_project_surface_policy_registry/summary.md)
