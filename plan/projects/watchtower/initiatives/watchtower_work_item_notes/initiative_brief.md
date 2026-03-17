# WatchTower Work Item Notes

## Summary
Adds local-first note capture on work items so operators can preserve thread context and resume a bounded slice without external scratch notes.

## Identity
- `initiative_id`: `initiative.watchtower_work_item_notes`
- `trace_id`: `trace.watchtower_work_item_notes`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`

## Initial Task Set
- `task.watchtower_work_item_notes.add_watchtower_work_item_note_flow`: Add a CLI path that appends one timestamped note to an existing local work-item record.
- `task.watchtower_work_item_notes.validate_watchtower_work_item_note_flow`: Cover note capture with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Bounded Slice
- Add `watchtower work note --slug <slug> --message <text>` so operators can capture progress or context directly on a local work item.
- Store notes on the existing work-item JSON record so no second scratch artifact is needed.
- Keep note retrieval implicit through `watchtower work show`; this slice does not add a separate history viewer.
- Do not add threaded comments, attachments, multi-user sync, or full journal management in this slice.
