# `watchtower_plan.sync`

## Summary
Repository-local sync services for live plan indexes, rendered trackers, workflow metadata materialization, and GitHub task mirrors that depend on the current WatchTowerPlan layout.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit plan-domain sync services and family modules such as `all`, `coordination`, `standard_index`, and `github_tasks`.
- `Non-Goals`: Stable public export surface through `watchtower_core.sync`.
- `Non-Goals`: Growing generic harness, dependency-ordering, or reusable rebuild behavior that now belongs under `watchtower_core.sync` or `watchtower_core.rebuild`.
- `Machine-State Boundary`: Write live plan machine state through governed `plan/.wt/**` surfaces; do not invent sidecar machine-state roots inside this package tree.

## Key Surfaces
- `all.py`: Aggregate sync orchestration.
- `coordination*.py`, `initiative*.py`, `task*.py`, and `workflow_index.py`: Family-specific rebuild logic for plan-domain indexes and trackers.
- `tracking_common.py`: Shared rendered-tracker bootstrap, write helpers, and terminal-history shaping.
- `traceability.py` and `traceability_support.py`: Traceability index orchestration and helper-backed merge logic.
- `github_tasks.py` and `github_task_sync_support.py`: GitHub task mirror orchestration plus task-selection, rendering, and write-sync helpers.

## Shrink Rules
- Keep reusable sync harness behavior in `watchtower_core.sync`.
- Keep repo-shared governed-index rebuilds such as command, route, and repository-path sync under `watchtower_core.sync`.
- Keep reusable rebuild-target execution and rendered-view building in `watchtower_core.rebuild`.
- Keep `watchtower_plan.sync` focused on current pack-specific source selection, document joins, and write targets that still depend on the WatchTowerPlan layout.
- Do not mirror reusable-core sync modules here just to create plan-flavored duplicates.

## Related Surfaces
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/integrations/github/README.md`
- `core/docs/standards/engineering/python_code_design_standard.md`
- `core/docs/commands/core_python/watchtower_core_sync.md`
