# Plan Project Surface Policy Registry Implementation Slice

## Summary
Adds the missing project-surface policy registry plus helper-backed project validation so project containers follow a declared surface contract instead of hardcoded assumptions.

## Initial Work Breakdown
- `task.plan_project_surface_policy_registry.publish_project_surface_policy_registry_schema`: Add the governed schema contract for the plan-owned project surface policy registry.
- `task.plan_project_surface_policy_registry.seed_project_surface_policy_entries`: Seed active policy entries covering required machine artifacts, rendered project views, and allowed optional project-local roots.
- `task.plan_project_surface_policy_registry.wire_helper_and_project_validation`: Add typed loader support, a project surface policy helper, and validation coverage that uses the new registry.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
