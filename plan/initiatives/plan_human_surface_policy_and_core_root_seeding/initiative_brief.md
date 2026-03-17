# Plan Human Surface Policy and Core Root Seeding

## Summary
Adds the governed `human_surface_policy_registry`, the helper and validation path that resolve those rules, and the missing `core/`, `core/docs/`, and `core/workflows/` human roots that [requirements.md](/home/j/WatchTowerPlan/requirements.md) declares as required.

## Identity
- `initiative_id`: `initiative.plan_human_surface_policy_and_core_root_seeding`
- `trace_id`: `trace.plan_human_surface_policy_and_core_root_seeding`
- `scope_type`: `pack_wide`

## Authority
- [requirements.md](/home/j/WatchTowerPlan/requirements.md) and [decisions.md](/home/j/WatchTowerPlan/decisions.md) are the authoritative implementation contract for this initiative.
- Existing standards, references, and helper docs may shape validation and file structure only where they do not materially conflict with those two sources.
- This slice specifically implements the missing `human_surface_policy_registry` called out in [requirements.md](/home/j/WatchTowerPlan/requirements.md#L563) and the explicit human-root obligations listed in [requirements.md](/home/j/WatchTowerPlan/requirements.md#L626).

## Acceptance Boundary
- Add a governed machine-readable policy surface at `plan/.wt/registries/human_surface_policy_registry.json` with a matching schema, schema-catalog entry, validator entry, and pack-settings declaration.
- Add typed loader and helper support so plan-pack code can resolve whether a root requires, allows, or forbids `README.md`, `AGENTS.md`, routed workflow docs, and rendered visibility files.
- Seed the missing `core/`, `core/docs/`, and `core/workflows/` router surfaces that the new policy would otherwise fail immediately.
- Add validation and tests that prove the current repository satisfies the declared policy for the roots covered in this slice.

## Initial Task Set
- `task.plan_human_surface_policy_and_core_root_seeding.add_human_surface_policy_contract_and_helper`: Add the human_surface_policy_registry schema, registry, typed loader support, and a helper that resolves required, optional, and forbidden human surfaces by root.
- `task.plan_human_surface_policy_and_core_root_seeding.seed_missing_core_human_roots_and_router_surfaces`: Create the missing core/, core/docs/, and core/workflows/ entrypoint surfaces and any thin router files required by the new human-surface policy.
- `task.plan_human_surface_policy_and_core_root_seeding.validate_human_surface_policy_and_root_compliance`: Add focused tests and validation coverage proving the registry, helper, and current repo roots conform to requirements.md and decisions.md.
