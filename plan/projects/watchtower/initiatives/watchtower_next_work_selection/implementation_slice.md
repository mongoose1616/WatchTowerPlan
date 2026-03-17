# WatchTower Next Work Selection Implementation Slice

## Summary
Adds a local-first next-work command so operators can ask WatchTower what unfinished work should be picked up next from the current workspace state.

## Initial Work Breakdown
- `task.watchtower_next_work_selection.add_watchtower_next_work_flow`
  - Extend the work-item helper layer with one deterministic next-work selector.
  - Add `watchtower work next [--format json|human]`.
- `task.watchtower_next_work_selection.validate_watchtower_next_work_flow`
  - Add CLI tests for missing-workspace, empty-queue, and successful selection paths.
  - Exercise the command against the initialized `/home/j/WatchTower` workspace.
  - Refresh the WatchTower repo README and Python workspace README for the new command.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
