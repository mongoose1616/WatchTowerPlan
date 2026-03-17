# WatchTower Workspace Init Bootstrap

## Summary
Adds a local-first workspace manifest and init flow so later WatchTower operator work starts from a real on-disk state root.

## Identity
- `initiative_id`: `initiative.watchtower_workspace_init_bootstrap`
- `trace_id`: `trace.watchtower_workspace_init_bootstrap`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`

## Initial Task Set
- `task.watchtower_workspace_init_bootstrap.add_watchtower_workspace_init_flow`: Add a CLI init path that writes a local workspace manifest and establishes the managed state root.
- `task.watchtower_workspace_init_bootstrap.validate_watchtower_workspace_init_flow`: Exercise the generated workspace manifest through CLI tests and update doctor to surface the initialized workspace state.

## Bounded Slice
- Add a repo-local `.watchtower/` state root under `/home/j/WatchTower`.
- Add `watchtower init` as the first mutating CLI command.
- Write one machine-readable workspace manifest at `.watchtower/workspace.json`.
- Update `watchtower doctor` so it reports whether the repo is only bootstrapped or has an initialized workspace manifest.
- Keep the slice local-first and inspectable: no frontend stack, database, hosted dependency, or long-lived background service.
