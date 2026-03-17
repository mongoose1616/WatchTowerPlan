# WatchTower Work Item Begin Flow Implementation Slice

## Summary
Adds a local-first begin command so operators can mark one WatchTower work item as actively in progress before completion.

## Initial Work Breakdown
- `task.watchtower_work_item_begin_flow.add_watchtower_work_item_begin_flow`
  - Extend the local work-item helpers with one begin transition that updates the current JSON record in place.
  - Add `watchtower work begin --slug <slug> [--format json|human]`.
  - Persist `status: in_progress`, `started_at`, and the latest `updated_at` on the selected work item.
- `task.watchtower_work_item_begin_flow.validate_watchtower_work_item_begin_flow`
  - Cover missing-workspace, missing-work-item, active-work, and already-active paths with CLI tests.
  - Exercise the command against the initialized WatchTower repo and refresh repo guidance.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
