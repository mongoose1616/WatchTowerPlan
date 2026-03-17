# WatchTower Work Item Lifecycle

## Summary
Adds local-first work-item inspection and completion flows so operators can see current work and close it cleanly inside an initialized WatchTower workspace.

## Identity
- `initiative_id`: `initiative.watchtower_work_item_lifecycle`
- `trace_id`: `trace.watchtower_work_item_lifecycle`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`

## Initial Task Set
- `task.watchtower_work_item_lifecycle.add_watchtower_work_item_inspection_flows`: Add CLI paths that list local work items and show one work-item record from the initialized workspace state root.
- `task.watchtower_work_item_lifecycle.add_watchtower_work_item_completion_flow`: Add a CLI path that marks one local work item completed and records its closeout metadata.
- `task.watchtower_work_item_lifecycle.validate_watchtower_work_item_lifecycle_flow`: Cover work-item inspection and completion with CLI tests, exercise the commands against the initialized WatchTower repo, and refresh repo guidance.

## Bounded Slice
- Add `watchtower work list` so operators can inspect the current local work queue without reading JSON by hand.
- Add `watchtower work show --slug <slug>` so one work-item record can be inspected directly from the CLI.
- Add `watchtower work complete --slug <slug>` with optional closeout summary text so a bounded item can leave the `planned` state cleanly.
- Keep work-item state local-first under `.watchtower/work_items/` and keep records human-inspectable JSON.
- Do not add editing, deletion, multi-user sync, remote storage, or a broader workflow engine in this slice.
