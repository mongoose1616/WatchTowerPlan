# `docs/planning/tasks`

## Description
`This directory holds local-first task records for active and closed work. Use it for engineer-sized execution items that need ownership, status, blockers, and links back to the planning corpus.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/tasks/README.md` | Describes the purpose of the task tracking directory and its main task surfaces. |
| `docs/planning/tasks/task_tracking.md` | Generated human-readable summary board for current local tasks. |
| `docs/planning/tasks/open/` | Holds non-terminal local task records. |
| `docs/planning/tasks/closed/` | Holds the dated terminal-task archive tree and its entrypoint README. |

## Notes
- Start with `docs/planning/coordination_tracking.md` when you need the current planning state and next action before opening task-specific surfaces.
- Use `docs/planning/initiatives/initiative_tracking.md` when you need the deeper initiative-family context behind a task.
- Treat one task file as one bounded work item.
- Treat task files as the local source of truth.
- Treat `task_tracking.md` as an open-work tracker with compact terminal context. Use `docs/planning/tasks/closed/archive/` for canonical closed task documents, `uv run watchtower-core query tasks --task-status done --format json` for completed-task lookup, and `uv run watchtower-core query tasks --task-status cancelled --format json` for cancelled-task lookup.
- Rebuild `task_tracking.md` and `core/control_plane/indexes/tasks/task_index.v1.json` after task changes.
