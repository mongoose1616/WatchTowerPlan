# `watchtower-core task transition`

## Summary
This command applies a bounded handoff-style status, owner, or blocker transition to one initiative-local live task record and refreshes derived plan-workspace surfaces in write mode.

## Use When
- You are handing a task from one phase or owner to the next.
- You want a narrower mutation surface than `task update` for status, owner, or blocker transitions.
- You want dry-run preview before mutating the canonical live task record.

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
uv run watchtower-core task transition --task-id <task_id> --task-status <status> [--next-owner <owner>] [--depends-on <task_id> | --clear-depends-on] [--blocked-by <task_id> | --clear-blocked-by] [--updated-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--task-id <task_id>`: Stable task identifier to transition.
- `--task-status <status>`: Next task execution status.
- `--next-owner <owner>`: Optional next responsible owner.
- `--depends-on <task_id>`: Replacement dependency task ID. Repeat for multiple values.
- `--clear-depends-on`: Remove the current dependency list.
- `--blocked-by <task_id>`: Replacement blocker task ID. Repeat for multiple values.
- `--clear-blocked-by`: Remove the current blocker list.
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.
- `--write`: Persist the transitioned live task record and refresh the derived plan surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core task transition --task-id task.example.001 --task-status in_review --next-owner validation_engineer
```

```sh
cd core/python
uv run watchtower-core task transition --task-id task.example.001 --task-status completed --clear-blocked-by --clear-depends-on --write
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate files.
- The command is a narrower handoff wrapper over the same governed task lifecycle service that powers `task update`.
- Execution-starting statuses such as `in_progress`, `in_review`, and `completed` require the initiative package to have already been approved into `ready_for_execution`.
- The task stays at the same initiative-local `task.json` path; terminality is represented by `task_status`, not path movement.
- The first execution-starting transition records an `execution_started` initiative event and advances the live initiative package into `in_progress`.
- In write mode, the command refreshes the live task, initiative, readiness, artifact, and coordination surfaces plus companion rendered views.
- In `human` mode, the command prints the resulting task path, status, owner, and write outcome.
- In `json` mode, the command prints one JSON object with the resulting task metadata, path outcome, write state, and `closeout_recommended` hint.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core task` | Parent command group for task lifecycle operations. |
| `watchtower-core task update` | Use when the transition also requires broader field or body edits. |
| `watchtower-core plan approve` | Required before handoff transitions can start real execution. |
| `watchtower-core query tasks` | Reads the task index refreshed in write mode. |
| `watchtower-core sync coordination` | Rebuilds the same coordination slice that write mode refreshes. |
| `watchtower-core closeout plan-initiative` | Use when the transition leaves a live `plan/**` initiative package with only terminal task state. |

## Source Surface
- `core/python/src/watchtower_core/cli/task_family.py`
- `core/python/src/watchtower_core/cli/task_handlers.py`
- `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`

## Updated At
- `2026-03-18T20:35:00Z`
