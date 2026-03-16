# `docs/planning/tasks/closed`

## Description
`This directory holds the dated archive tree for terminal task records such as completed or cancelled work.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/tasks/closed/README.md` | Describes the purpose of the closed-task archive root. |
| `docs/planning/tasks/closed/archive/` | Holds dated terminal task records under `YYYY/MM/DD/` directories. |

## Notes
- Keep the root compact. Terminal task files should live under `docs/planning/tasks/closed/archive/<yyyy>/<mm>/<dd>/`.
- Use [task_tracking.md](/docs/planning/tasks/task_tracking.md) for a compact recent-closeout view, `watchtower-core query tasks --task-status done --format json` for completed-task lookup, and `watchtower-core query tasks --task-status cancelled --format json` for cancelled-task lookup.
