# Plan Task Tracking Sync Performance

## Summary
Reduce the coordination rebuild cost caused by repeated live task-state loading during plan write commands.

## Identity
- `initiative_id`: `initiative.plan_task_tracking_sync_performance`
- `trace_id`: `trace.plan_task_tracking_sync_performance`
- `scope_type`: `pack_wide`

## Problem Statement
- `watchtower-core plan approve --write` and related plan write commands currently spend most of their runtime in the coordination rebuild rather than in the requested state mutation.
- The dominant hotspot is `plan/python/src/watchtower_plan/sync/task_tracking.py`, which calls `iter_task_documents()` and triggers repeated initiative-state discovery and validation work for each task document.
- On the current repository state, `task-tracking` takes roughly 30 seconds by itself, which makes common write commands operationally too slow.

## Desired Outcome
- Keep the same governed task-tracking output and plan coordination behavior.
- Eliminate redundant initiative/task reload work so plan write commands complete in a materially faster, operator-usable time window.
- Preserve fail-closed validation and compatibility with the existing task lifecycle and sync services.

## Initial Task Set
- `task.plan_task_tracking_sync_performance.bootstrap_plan_task_tracking_sync_performance`: Bootstrap Plan Task Tracking Sync Performance live initiative package.
