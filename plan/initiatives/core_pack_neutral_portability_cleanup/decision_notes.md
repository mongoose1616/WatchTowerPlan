# Core Pack Neutral Portability Cleanup Decision Notes

## Summary
This initiative removes portability debt from shared core without rewriting current-repository facts that are still true for `WatchTowerPlan`.

## Locked Decisions
- Shared-core tests must remain pack-neutral and must not depend on the live `plan/` workspace just because it exists in this repository.
- Tests that prove direct `watchtower_plan` behavior or current-repository `plan` command and doc contracts belong under `plan/python/tests/`.
- Shared-core docs should use pack-neutral wording such as `<pack-root>/python/tests/` when a direct `plan` example is not materially required.
- Current-repository foundations and other durable surfaces that intentionally describe `plan` as the active internal pack are not deplanified in this slice.
- Synthetic fixture defaults in shared-core helpers should be neutral example values, not donor-pack identifiers.
