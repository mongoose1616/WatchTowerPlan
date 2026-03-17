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
- Start with `plan/plan_overview.md` when you need the live planning state and next action before opening docs-backed task surfaces.
- Use `docs/planning/coordination_tracking.md` and `docs/planning/initiatives/initiative_tracking.md` when you need the traced-planning backlog context behind a task.
- Treat one task file as one bounded work item.
- Treat task files as the local source of truth.
- Treat `task_tracking.md` as an open-work tracker with compact terminal context. Use `docs/planning/tasks/closed/archive/` for retained closed-task documents while a trace remains in the planning corpus, `uv run watchtower-core query tasks --task-status done --format json` for completed-task lookup, and `uv run watchtower-core query tasks --task-status cancelled --format json` for cancelled-task lookup.
- Do not rely on archived task files as the enduring source of current policy once equivalent standards, plans, or other canonical artifacts exist.
- Rebuild `task_tracking.md` and `core/control_plane/indexes/tasks/task_index.json` after task changes.
