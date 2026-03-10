# `docs/planning/tasks`

## Description
`This directory holds local-first task records for active and closed work. Use it for engineer-sized execution items that need ownership, status, blockers, and links back to the planning corpus.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/tasks/README.md` | Describes the purpose of the task tracking directory and its main task surfaces. |
| `docs/planning/tasks/task_tracking.md` | Generated human-readable summary board for current local tasks. |
| `docs/planning/tasks/open/` | Holds non-terminal local task records. |
| `docs/planning/tasks/closed/` | Holds terminal local task records. |

## Notes
- Start with `docs/planning/initiatives/initiative_tracking.md` when you need to know whether an initiative is actively assigned and what should happen next beyond one task file.
- Treat one task file as one bounded work item.
- Treat task files as the local source of truth.
- Rebuild `task_tracking.md` and `core/control_plane/indexes/tasks/task_index.v1.json` after task changes.
