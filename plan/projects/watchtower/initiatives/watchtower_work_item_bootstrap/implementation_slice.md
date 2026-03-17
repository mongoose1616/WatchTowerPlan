# WatchTower Work Item Bootstrap Implementation Slice

## Summary
Adds a local-first work-item record flow so operators can start bounded work inside an initialized WatchTower workspace.

## Initial Work Breakdown
- `task.watchtower_work_item_bootstrap.add_watchtower_work_item_start_flow`
  - Add a small work-item helper under `core/python/src/watchtower/`.
  - Add `watchtower work start --slug <slug> --title <title>`.
  - Write one work-item record under `.watchtower/work_items/`.
- `task.watchtower_work_item_bootstrap.validate_watchtower_work_item_start_flow`
  - Add CLI tests for the missing-workspace failure path and the successful work-item creation path.
  - Exercise the command against the initialized `/home/j/WatchTower` workspace.
  - Refresh the repo README and workspace README for the new command.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
