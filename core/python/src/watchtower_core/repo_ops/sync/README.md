# `watchtower_core.repo_ops.sync`

## Summary
Residual repository sync services for plan-pack derived indexes, rendered trackers, route and workflow metadata materialization, and GitHub task mirrors.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit sync services and family modules such as `all`, `command_index`, `standard_index`, and `github_tasks`.
- `Non-Goals`: Stable public export surface through `watchtower_core.sync`.
- `Non-Goals`: Growing generic harness, dependency-ordering, or reusable rebuild behavior that now belongs under `watchtower_core.sync` or `watchtower_core.rebuild`.

## Key Surfaces
- `all.py`: Aggregate sync orchestration.
- `*_index.py` and `*_tracking.py`: Family-specific rebuild logic for governed indexes and trackers.
- `tracking_common.py`: Shared rendered-tracker bootstrap, write helpers, and terminal-history shaping.
- `traceability.py` and `traceability_support.py`: Traceability index orchestration and helper-backed merge logic.
- `github_tasks.py` and `github_task_sync_support.py`: GitHub task mirror orchestration plus task-selection, rendering, and write-sync helpers.

## Shrink Rules
- Keep reusable sync harness behavior in `watchtower_core.sync`.
- Keep reusable rebuild-target execution and rendered-view building in `watchtower_core.rebuild`.
- Keep `repo_ops.sync` focused on current pack-specific source selection, document joins, and write targets that still depend on the WatchTowerPlan layout.

## Related Surfaces
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/integrations/github/README.md`
- `docs/commands/core_python/watchtower_core_sync.md`
