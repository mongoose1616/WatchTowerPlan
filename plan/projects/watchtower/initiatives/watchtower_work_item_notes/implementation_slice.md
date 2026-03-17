# WatchTower Work Item Notes Implementation Slice

## Summary
Adds local-first note capture on work items so operators can preserve thread context and resume a bounded slice without external scratch notes.

## Initial Work Breakdown
- `task.watchtower_work_item_notes.add_watchtower_work_item_note_flow`
  - Extend the local work-item helpers to append one structured note to an existing record.
  - Add `watchtower work note --slug <slug> --message <text>`.
- `task.watchtower_work_item_notes.validate_watchtower_work_item_note_flow`
  - Add CLI tests for missing-workspace, missing-item, and successful note capture paths.
  - Exercise the command against the initialized `/home/j/WatchTower` workspace.
  - Refresh the WatchTower repo README and Python workspace README for the new command.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
