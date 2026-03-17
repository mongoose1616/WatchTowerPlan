# WatchTower Work Item Bootstrap

## Summary
Adds a local-first work-item record flow so operators can start bounded work inside an initialized WatchTower workspace.

## Identity
- `initiative_id`: `initiative.watchtower_work_item_bootstrap`
- `trace_id`: `trace.watchtower_work_item_bootstrap`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`

## Initial Task Set
- `task.watchtower_work_item_bootstrap.add_watchtower_work_item_start_flow`: Add a CLI path that creates one local work-item record under the initialized workspace state root.
- `task.watchtower_work_item_bootstrap.validate_watchtower_work_item_start_flow`: Cover workspace-required work-item creation with CLI tests and exercise the flow against the initialized WatchTower repo.

## Bounded Slice
- Add one CLI entrypoint, `watchtower work start`.
- Require an initialized `.watchtower/workspace.json` before any work-item record can be created.
- Write one machine-readable work-item record per started item under `.watchtower/work_items/`.
- Keep the first work-item record minimal: id, slug, title, status, created_at, and updated_at.
- Do not add work-item editing, listing, or workflow automation in this slice.
