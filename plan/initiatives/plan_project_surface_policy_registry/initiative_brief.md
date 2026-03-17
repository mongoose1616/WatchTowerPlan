# Plan Project Surface Policy Registry

## Summary
Adds the missing project-surface policy registry plus helper-backed project validation so project containers follow a declared surface contract instead of hardcoded assumptions.

## Identity
- `initiative_id`: `initiative.plan_project_surface_policy_registry`
- `trace_id`: `trace.plan_project_surface_policy_registry`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_project_surface_policy_registry.publish_project_surface_policy_registry_schema`: Add the governed schema contract for the plan-owned project surface policy registry.
- `task.plan_project_surface_policy_registry.seed_project_surface_policy_entries`: Seed active policy entries covering required machine artifacts, rendered project views, and allowed optional project-local roots.
- `task.plan_project_surface_policy_registry.wire_helper_and_project_validation`: Add typed loader support, a project surface policy helper, and validation coverage that uses the new registry.
