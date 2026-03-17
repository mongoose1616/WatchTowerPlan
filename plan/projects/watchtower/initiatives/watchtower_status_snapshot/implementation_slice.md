# WatchTower Status Snapshot Implementation Slice

## Summary
Adds one local-first status command so operators can see workspace readiness and current work-item counts from a single WatchTower entrypoint.

## Initial Work Breakdown
- `task.watchtower_status_snapshot.add_watchtower_status_snapshot_flow`
  - Add a status payload helper that reads the current workspace manifest and local work-item records.
  - Add `watchtower status [--format json|human]`.
- `task.watchtower_status_snapshot.validate_watchtower_status_snapshot_flow`
  - Add CLI tests for missing-workspace and initialized-workspace status paths.
  - Exercise the command against the initialized `/home/j/WatchTower` repo.
  - Refresh the WatchTower repo README and Python workspace README for the new entrypoint.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
