# Plan Rendered Surface Builder Alignment Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_rendered_surface_builder_alignment`
- `trace_id`: `trace.plan_rendered_surface_builder_alignment`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-18T02:44:00Z`

## Scope and Non-Goals
Extracts a reusable rendered-view builder and markdown reconciliation helper, then routes live plan and project rendered surfaces through the registry-backed boundary.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add reusable rendered view builder: Publish a registry-backed rendered-view builder that resolves rendered surface definitions into deterministic markdown outputs.
- Refactor live plan and project surfaces onto rendered helpers: Replace repo-local rendered markdown assembly and drift detection with the shared builder and markdown reconciliation helpers.
- Validate rendered surface boundary alignment: Add focused rebuild-boundary tests and reconcile the rendered requirements rows to the implemented reusable boundary.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_rendered_surface_builder_alignment.add_reusable_rendered_view_builder](/plan/initiatives/plan_rendered_surface_builder_alignment/.wt/tasks/add_reusable_rendered_view_builder/task.json) | `completed` | `high` | `repository_maintainer` | Publish a registry-backed rendered-view builder that resolves rendered surface definitions into deterministic markdown outputs. | - |
| [task.plan_rendered_surface_builder_alignment.refactor_live_plan_and_project_surfaces_onto_rendered_helpers](/plan/initiatives/plan_rendered_surface_builder_alignment/.wt/tasks/refactor_live_plan_and_project_surfaces_onto_rendered_helpers/task.json) | `completed` | `high` | `repository_maintainer` | Replace repo-local rendered markdown assembly and drift detection with the shared builder and markdown reconciliation helpers. | task.plan_rendered_surface_builder_alignment.add_reusable_rendered_view_builder |
| [task.plan_rendered_surface_builder_alignment.validate_rendered_surface_boundary_alignment](/plan/initiatives/plan_rendered_surface_builder_alignment/.wt/tasks/validate_rendered_surface_boundary_alignment/task.json) | `completed` | `high` | `repository_maintainer` | Add focused rebuild-boundary tests and reconcile the rendered requirements rows to the implemented reusable boundary. | task.plan_rendered_surface_builder_alignment.refactor_live_plan_and_project_surfaces_onto_rendered_helpers |

## Dependencies and Risks
- Task `task.plan_rendered_surface_builder_alignment.refactor_live_plan_and_project_surfaces_onto_rendered_helpers` depends on `task.plan_rendered_surface_builder_alignment.add_reusable_rendered_view_builder`.
- Task `task.plan_rendered_surface_builder_alignment.validate_rendered_surface_boundary_alignment` depends on `task.plan_rendered_surface_builder_alignment.refactor_live_plan_and_project_surfaces_onto_rendered_helpers`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_rendered_surface_builder_alignment/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_rendered_surface_builder_alignment/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_rendered_surface_builder_alignment/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_rendered_surface_builder_alignment/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_rendered_surface_builder_alignment/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_rendered_surface_builder_alignment/summary.md)
