# Plan Human Surface Policy and Core Root Seeding Implementation Slice

## Summary
Adds the governed human-surface policy contract, the helper and validation path that resolve those rules, and the missing core-owned human roots that requirements.md declares as required.

## Initial Work Breakdown
- `task.plan_human_surface_policy_and_core_root_seeding.add_human_surface_policy_contract_and_helper`: Add the human_surface_policy_registry schema, registry, typed loader support, and a helper that resolves required, optional, and forbidden human surfaces by root.
- `task.plan_human_surface_policy_and_core_root_seeding.seed_missing_core_human_roots_and_router_surfaces`: Create the missing core/, core/docs/, and core/workflows/ entrypoint surfaces and any thin router files required by the new human-surface policy.
- `task.plan_human_surface_policy_and_core_root_seeding.validate_human_surface_policy_and_root_compliance`: Add focused tests and validation coverage proving the registry, helper, and current repo roots conform to requirements.md and decisions.md.

## Planned Change Set
- Add `plan/.wt/schemas/artifacts/human_surface_policy_registry.schema.json`.
- Add `plan/.wt/registries/human_surface_policy_registry.json`.
- Update `plan/.wt/manifests/pack_settings.json`, `plan/.wt/registries/schema_catalog.json`, and `plan/.wt/registries/validator_registry.json`.
- Add typed model and loader support in `core/python/src/watchtower_core/control_plane/`.
- Add a helper and focused validation tests for policy resolution and compliance checks.
- Add or refresh thin human router surfaces under `core/`, `core/docs/`, `core/workflows/`, and `plan/workflows/` as required by the policy.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
