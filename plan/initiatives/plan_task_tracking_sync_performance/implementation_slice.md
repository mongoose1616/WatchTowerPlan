# Plan Task Tracking Sync Performance Implementation Slice

## Summary
Reduce the coordination rebuild cost caused by repeated live task-state loading during plan write commands.

## Initial Work Breakdown
- `task.plan_task_tracking_sync_performance.bootstrap_plan_task_tracking_sync_performance`: Bootstrap Plan Task Tracking Sync Performance live initiative package.

## Planned Execution
- Measure the current hot path for `CoordinationSyncService.run()` and `TaskTrackingSyncService.build_document()` against the live repository.
- Refactor `plan/python/src/watchtower_plan/tasks/state.py` so one task-iteration pass does not call initiative-state discovery for every task document.
- Add or update regression coverage for task-state loading to preserve the current task metadata contract while asserting the new direct-build path.
- Re-measure targeted sync timings and rerun the relevant validation bundle before closeout.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
