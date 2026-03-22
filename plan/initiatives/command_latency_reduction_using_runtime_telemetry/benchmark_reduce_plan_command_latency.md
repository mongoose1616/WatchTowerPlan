# Plan Command Latency Reduction

## Summary
- Captured on `2026-03-22T19:25:00Z` after the `reduce_plan_command_latency` slice.
- The read-path work now reuses the cached plan pack loader and avoids eagerly constructing write-only workspace collaborators during query-heavy command paths.
- The write-path work now avoids rerunning overlapping coordination targets after task and GitHub task sync flows have already rebuilt the plan workspace surfaces.
- Project-scoped initiative location syncing intentionally stayed on the full coordination rebuild path after regression checks showed that the reduced follow-up slice left project initiative and coordination indexes stale.

## Command Delta Against Baseline
| Command | Baseline Median (ms) | Current Median (ms) | Improvement (ms) | Improvement (%) |
| --- | ---: | ---: | ---: | ---: |
| `plan query coordination --format json` | `1379.610` | `612.292` | `767.318` | `55.62` |
| `plan sync coordination --write --format json` | `1329.894` | `1210.746` | `119.148` | `8.96` |
| `plan task create --write --format json` | `3037.702` | `2668.563` | `369.139` | `12.15` |

## Implementation Notes
- [service.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/workspace/service.py) now keeps its cached pack loader on the read path and lazily initializes the render/build helpers that are only needed for rebuild flows.
- [coordination.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/query/coordination.py) no longer instantiates the initiative-history query service unless the coordination query explicitly delegates to non-active history.
- [coordination.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/sync/coordination.py), [lifecycle.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/tasks/lifecycle.py), and [github_task_sync_support.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/sync/github_task_sync_support.py) now use a reduced coordination follow-up slice after plan workspace sync so the task write path avoids redundant `initiative-index`, `coordination-index`, and `task-index` rebuilds.
- [locations.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/initiatives/locations.py) deliberately continues to use the full coordination rebuild because project-scoped bootstrap and readiness flows still need the broader coordination service behavior for correctness.

## Remaining Hotspot Shape
- `plan task create --write --format json` is still the slowest plan-owned command in the benchmark set, even after the first write-path reduction.
- `pack validate --pack plan --format json` remains the next reusable-core hotspot from the original baseline and should stay the next execution target for this initiative.

## Notes
- The isolated `plan task create --write --format json` benchmark still ran in a temporary repo copy so the active `plan` workspace stayed clean.
- The machine-readable companion for this note is `benchmark_reduce_plan_command_latency.json`.
