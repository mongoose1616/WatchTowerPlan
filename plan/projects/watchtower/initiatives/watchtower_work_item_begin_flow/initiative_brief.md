# WatchTower Work Item Begin Flow

## Summary
Adds a local-first begin command so operators can mark one WatchTower work item as actively in progress before completion.

## Identity
- `initiative_id`: `initiative.watchtower_work_item_begin_flow`
- `trace_id`: `trace.watchtower_work_item_begin_flow`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`

## Initial Task Set
- `task.watchtower_work_item_begin_flow.add_watchtower_work_item_begin_flow`: Add a CLI path that marks one local work item in progress and persists active-work metadata.
- `task.watchtower_work_item_begin_flow.validate_watchtower_work_item_begin_flow`: Cover the begin flow with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Bounded Slice
- Add `watchtower work begin --slug <slug>` so operators can move one local work item from `planned` to `in_progress`.
- Persist the active-work transition on the existing `.watchtower/work_items/<slug>.json` record and stamp a `started_at` timestamp the first time a record begins.
- Keep the command idempotent for already active items instead of introducing a separate resume ledger.
- Do not add pause, reprioritization, remote locks, or multi-user queue semantics in this slice.
