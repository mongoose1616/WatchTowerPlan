# Plan Rendered Surface Builder Alignment Implementation Slice

## Summary
Extracts a reusable rendered-view builder and markdown reconciliation helper, then routes live plan and project rendered surfaces through the registry-backed boundary.

## Initial Work Breakdown
- `task.plan_rendered_surface_builder_alignment.add_reusable_rendered_view_builder`: Publish a registry-backed rendered-view builder that resolves rendered surface definitions into deterministic markdown outputs.
- `task.plan_rendered_surface_builder_alignment.refactor_live_plan_and_project_surfaces_onto_rendered_helpers`: Replace repo-local rendered markdown assembly and drift detection with the shared builder and markdown reconciliation helpers.
- `task.plan_rendered_surface_builder_alignment.validate_rendered_surface_boundary_alignment`: Add focused rebuild-boundary tests and reconcile the rendered requirements rows to the implemented reusable boundary.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
