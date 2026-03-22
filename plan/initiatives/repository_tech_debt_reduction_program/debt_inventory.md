# Repository Tech Debt Inventory

## Summary
- Captured on `2026-03-22` for the first execution tranche of `repository_tech_debt_reduction_program`.
- The highest current debt cost is still the Python integration-tail runtime, concentrated in the shared plan-workspace integration family.
- The highest cleanup-value structural debt after test runtime is stale compatibility shims in `watchtower_plan` and duplicated shared validator authority between `core` and `plan`.

## Measured Runtime Hotspots
- `core/python/tests/integration/test_plan_workspace_coordination.py`
  - `test_plan_workspace_coordination_surfaces_recent_closeouts_after_terminal_closeout`: `52.18s`
  - `test_validate_packwide_preserves_closing_lifecycle_while_rebuilding_stale_surfaces`: `18.84s`
  - `test_plan_workspace_stale_surface_drift_blocks_readiness_until_explicit_rebuild`: `14.03s`
  - `test_plan_workspace_sync_treats_task_complete_ready_initiatives_as_closeout`: `12.36s`
- `core/python/tests/integration/test_plan_workspace_indexes.py`
  - `test_plan_workspace_sync_includes_project_scoped_initiatives_in_pack_indexes`: `26.20s`
  - `test_plan_workspace_sync_writes_indexes_views_and_query_surfaces`: `15.26s`
  - `test_plan_workspace_sync_uses_latest_task_state_timestamp_for_indexes`: `12.76s`
- `core/python/tests/integration/test_task_workflow_end_to_end.py`
  - `test_packwide_initiative_closeout_requires_terminal_live_tasks`: `22.76s`
  - `test_task_management_flow_updates_queries_trackers_and_initiative_views`: `19.18s`

## Runtime Tail Findings
- The slowest current family is the shared helper-backed workspace suite in [plan_workspace_integration_cases.py](/home/j/WatchTowerPlan/core/python/tests/integration/plan_workspace_integration_cases.py).
- The file copies large repo subsets, bootstraps initiatives or projects from scratch, and repeatedly rebuilds broad plan-workspace surfaces even when individual assertions only need one derived family.
- The wrapper modules [test_plan_workspace_coordination.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_plan_workspace_coordination.py) and [test_plan_workspace_indexes.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_plan_workspace_indexes.py) are structurally clean, but they expose a helper family that still pays full setup cost per test.
- The task end-to-end file is no longer the worst hotspot, but it still performs expensive whole-pack workflow setup for coverage that overlaps cheaper service-level integration cases.

## Stale Compatibility And Migration Residue
- The legacy top-level workspace shims have been removed; callers now import the owned workspace seams under `watchtower_plan.workspace.*`.
- Artifact-index callers now import [artifacts.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/workspace/artifacts.py) instead of a top-level `watchtower_plan.artifact_index` shim.
- Terminology callers now use [TerminologyHelper](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/terminology.py) directly instead of the retired `PlanningVocabularyHelper` alias.
- [workspace.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/_pack_contract/workspace.py) still merges legacy root fields into `domain_roots`, which preserves migration-era shape support that may no longer defend an active contract.

## Duplicate Authority Findings
- `core/control_plane/registries/validator_registry.json` currently defines `39` shared validator IDs.
- `plan/.wt/registries/validator_registry.json` currently defines `84` validator IDs.
- `39` validator IDs are duplicated between the two registries, while `45` are plan-specific.
- `SchemaCatalog.merge(...)` and `ValidatorRegistry.merge(...)` already exist in the reusable model layer, which means the current loader behavior is lagging the model capability.
- [loader_surfaces.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/loader_surfaces.py) already returns a merged schema catalog through `loader.schema_store.catalog`, but `load_validator_registry()` still loads only the current registry path instead of merging the shared core registry with the active pack registry.

## Ranked Removal Order
1. Reduce integration-tail cost in the plan-workspace family.
   - Reuse prepared repo baselines.
   - Stop rebuilding broad workspace surfaces when a narrower sync or query path is enough.
   - Keep one real end-to-end closeout or coordination proof per family and downgrade the rest to cheaper prepared-state variants.
2. Remove stale compatibility and migration residue.
   - Completed: tests and callers moved off `watchtower_plan.plan_workspace` and `watchtower_plan.artifact_index`, and the compatibility shims were deleted.
   - Completed: terminology callers moved off the `PlanningVocabularyHelper` alias.
   - Remaining: remove legacy migration support only after targeted contract validation shows no active caller depends on it.
3. Reconcile duplicated validator authority.
   - Merge core and active-pack validator registries in loader behavior.
   - Shrink the plan registry to plan-specific validators plus any still-required pack-local declarations.
   - Keep schema and validator behavior unchanged at the public query and validation surfaces.

## Execution Notes
- The first execution slice should focus on runtime-heavy integration tests because that debt is both operator-visible and measurable.
- Compatibility and validator cleanup should follow immediately after the test-tail reduction so the tranche removes both runtime drag and stale structural residue.
