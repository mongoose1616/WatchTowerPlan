# `watchtower-core task transition`

## Summary
This command applies a bounded handoff-style status, owner, or blocker transition to one governed local task record and refreshes the coordination slice in write mode.

## Use When
- You are handing a task from one phase or owner to the next.
- You want a narrower mutation surface than `task update` for status, owner, or blocker transitions.
- You want dry-run preview before mutating the canonical task document.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core task transition` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/task_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core task transition --task-id <task_id> --task-status <status> [--next-owner <owner>] [--depends-on <task_id> | --clear-depends-on] [--blocked-by <task_id> | --clear-blocked-by] [--file-stem <stem>] [--updated-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--task-id <task_id>`: Stable task identifier to transition.
- `--task-status <status>`: Next task execution status.
- `--next-owner <owner>`: Optional next responsible owner.
- `--depends-on <task_id>`: Replacement dependency task ID. Repeat for multiple values.
- `--clear-depends-on`: Remove the current dependency list.
- `--blocked-by <task_id>`: Replacement blocker task ID. Repeat for multiple values.
- `--clear-blocked-by`: Remove the current blocker list.
- `--file-stem <stem>`: Optional replacement filename stem when the transition also moves the file.
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.
- `--write`: Persist the transitioned task document and refresh the coordination slice.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core task transition --task-id task.example.001 --task-status in_review --next-owner validation_engineer
```

```sh
cd core/python
uv run watchtower-core task transition --task-id task.example.001 --task-status done --clear-blocked-by --clear-depends-on --write
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate files.
- The command is a narrower handoff wrapper over the same governed task lifecycle service that powers `task update`.
- Write mode moves the task document between `open/` and `closed/` automatically when the new task status changes terminality.
- In `human` mode, the command prints the resulting task path, status, owner, and write outcome.
- In `json` mode, the command prints one JSON object with the resulting task metadata, path outcome, write state, and `closeout_recommended` hint.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core task` | Parent command group for task lifecycle operations. |
| `watchtower-core task update` | Use when the transition also requires broader field or body edits. |
| `watchtower-core query tasks` | Reads the task index refreshed in write mode. |
| `watchtower-core sync coordination` | Rebuilds the same coordination slice that write mode refreshes. |
| `watchtower-core closeout initiative` | Use when the transition leaves a traced initiative with only terminal task state. |

## Source Surface
- `core/python/src/watchtower_core/cli/task_family.py`
- `core/python/src/watchtower_core/cli/task_handlers.py`
- `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`

## Updated At
- `2026-03-10T22:54:30Z`
