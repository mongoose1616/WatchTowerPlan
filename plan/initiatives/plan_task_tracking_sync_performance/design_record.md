# Plan Task Tracking Sync Performance Design Record

## Summary
Reduce the coordination rebuild cost caused by repeated live task-state loading during plan write commands.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_task_tracking_sync_performance/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Focused Design
- Optimize task-state loading in `plan/python/src/watchtower_plan/tasks/state.py` first, because the measured hotspot is repeated per-task initiative lookup and validation churn rather than markdown rendering.
- Build `PlanTaskStateDocument` instances directly from the already-known initiative state when iterating task directories, instead of re-resolving initiative ownership for every task path.
- Reuse a single pack-derived loader and stable initiative-root mapping within one iteration pass.
- Keep public task-state APIs stable unless a private helper split is required to support the faster path.

## Non-Goals
- Do not redesign the full plan sync architecture in this slice.
- Do not relax schema validation or remove derived-surface rebuilds from write commands.
- Do not change the human-visible task tracking format except where a bug fix requires it.
