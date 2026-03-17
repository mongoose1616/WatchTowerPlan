# WatchTower Workspace Init Bootstrap Implementation Slice

## Summary
Adds a local-first workspace manifest and init flow so later WatchTower operator work starts from a real on-disk state root.

## Initial Work Breakdown
- `task.watchtower_workspace_init_bootstrap.add_watchtower_workspace_init_flow`
  - Add a small workspace helper for `.watchtower/workspace.json`.
  - Add `watchtower init` to create the state root and manifest.
  - Keep the manifest local-first and JSON-based.
- `task.watchtower_workspace_init_bootstrap.validate_watchtower_workspace_init_flow`
  - Update `watchtower doctor` to read the manifest when present.
  - Add CLI tests for init creation and doctor reporting.
  - Refresh the WatchTower repo README and workspace README for the new command path.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
