# WatchTower Work Item Lifecycle Implementation Slice

## Summary
Adds local-first work-item inspection and completion flows so operators can see current work and close it cleanly inside an initialized WatchTower workspace.

## Initial Work Breakdown
- `task.watchtower_work_item_lifecycle.add_watchtower_work_item_inspection_flows`
  - Extend the local work-item helpers to load one record and list all current records from `.watchtower/work_items/`.
  - Add `watchtower work list` and `watchtower work show --slug <slug>`.
- `task.watchtower_work_item_lifecycle.add_watchtower_work_item_completion_flow`
  - Add a helper that marks one work-item record completed and persists closeout metadata.
  - Add `watchtower work complete --slug <slug> [--summary <text>]`.
- `task.watchtower_work_item_lifecycle.validate_watchtower_work_item_lifecycle_flow`
  - Add CLI tests for list, show, missing-item failure, and complete flows.
  - Exercise the commands against the initialized `/home/j/WatchTower` workspace.
  - Refresh the WatchTower repo README and Python workspace README for the added command set.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
