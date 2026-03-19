# `docs/planning/tasks`

## Description
`This directory holds the human-readable live task tracker plus the retained historical docs-backed task corpus. New live tasks do not originate here.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/tasks/README.md` | Describes the purpose of the task-tracking directory and its retained historical boundaries. |
| `docs/planning/tasks/task_tracking.md` | Generated human-readable task board derived from live initiative-local task state. |
| `docs/planning/tasks/open/` | Retained historical pre-cutover non-terminal task Markdown. |
| `docs/planning/tasks/closed/` | Retained historical terminal-task archive tree and entrypoint README. |

## Notes
- Start with `plan/plan_overview.md` when you need the live planning state and next action.
- Use `uv run watchtower-core query tasks --format json` when you need the canonical machine-readable live task lookup.
- Treat `task_tracking.md` as the human companion to the live task index under `plan/.wt/indexes/task_index.json`.
- Do not create new live tasks under `docs/planning/tasks/**`.
- Treat `open/` and `closed/` as retained historical material only.
- Use `watchtower-core query tasks --task-status completed --format json` for live completed-task lookup and `--task-status cancelled` for live cancelled-task lookup.
