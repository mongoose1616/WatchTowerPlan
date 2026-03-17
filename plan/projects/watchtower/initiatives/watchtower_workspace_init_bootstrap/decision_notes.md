# WatchTower Workspace Init Bootstrap Decision Notes

## Summary
Capture the minimal decisions that keep the workspace-init slice bounded.

## Decisions
- Use `.watchtower/` as the local managed-state root instead of putting mutable state directly at repo root.
- Use one JSON manifest at `.watchtower/workspace.json` so both humans and CLI code can inspect the same bootstrap state.
- Keep `watchtower init` local-only and dependency-light; do not introduce a backend service, database, or hosted control plane in this slice.
