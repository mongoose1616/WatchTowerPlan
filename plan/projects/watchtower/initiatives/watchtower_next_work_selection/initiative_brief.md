# WatchTower Next Work Selection

## Summary
Adds a local-first next-work command so operators can ask WatchTower what unfinished work should be picked up next from the current workspace state.

## Identity
- `initiative_id`: `initiative.watchtower_next_work_selection`
- `trace_id`: `trace.watchtower_next_work_selection`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`

## Initial Task Set
- `task.watchtower_next_work_selection.add_watchtower_next_work_flow`: Add a CLI path that selects one unfinished local work item and returns a compact resume snapshot.
- `task.watchtower_next_work_selection.validate_watchtower_next_work_flow`: Cover next-work selection with CLI tests, exercise it against the initialized WatchTower repo, and refresh repo guidance.

## Bounded Slice
- Add `watchtower work next` so operators can ask the local workspace what unfinished work should be picked up next.
- Select from existing non-completed work-item records only; do not invent planning state outside `.watchtower/work_items/`.
- Return a compact resume snapshot with the selected work item, its latest note if one exists, and the on-disk path.
- Do not add prioritization policy, scheduling, or multi-user queue semantics in this slice.
