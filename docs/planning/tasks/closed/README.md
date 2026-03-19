# `docs/planning/tasks/closed`

## Description
`This directory holds the retained historical archive tree for docs-backed terminal task Markdown. It is not the live source of task truth.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/tasks/closed/README.md` | Describes the purpose of the retained historical closed-task archive root. |
| `docs/planning/tasks/closed/archive/` | Holds dated historical terminal task records under `YYYY/MM/DD/` directories. |

## Notes
- Keep the root read-only except for retention or purge hygiene.
- Do not create new live tasks here.
- Use [task_tracking.md](/docs/planning/tasks/task_tracking.md) for the generated human task board, `watchtower-core query tasks --task-status completed --format json` for live completed-task lookup, and `watchtower-core query tasks --task-status cancelled --format json` for live cancelled-task lookup.
