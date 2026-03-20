# `watchtower-core plan task`

## Summary
This command group creates, updates, and transitions initiative-local live task records under `plan/**/.wt/tasks/**` while refreshing derived plan-workspace surfaces in write mode.

## Use When
- You want help for the live task lifecycle without hand-editing initiative-local task state.
- You need to create one new task, apply structured field updates, or perform a bounded handoff-style transition.
- You want dry-run preview before mutating live task state and its derived plan-workspace mirrors.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan task` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/tasks.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan task <task_command> [args]
```

## Arguments and Options
- `<task_command>`: Choose `create`, `update`, or `transition`.
- `-h`, `--help`: Show the command help text.
- Task mutations are dry-run by default. Pass `--write` to the selected leaf command to persist the task change and refresh the derived plan surfaces.

## Examples
```sh
cd core/python
uv run watchtower-core plan task --help
```

```sh
cd core/python
uv run watchtower-core plan task create --task-id task.example.001 --title "Draft the example" --summary "Creates the example task." --task-kind documentation --priority medium --owner repository_maintainer --scope "Write the example" --done-when "The example exists"
```

```sh
cd core/python
uv run watchtower-core plan task update --task-id task.example.001 --task-status in_progress --owner implementation_engineer --format json
```

```sh
cd core/python
uv run watchtower-core plan task transition --task-id task.example.001 --task-status completed --write
```

## Behavior and Outputs
- With no leaf command, the current implementation prints task-specific help and exits successfully.
- The command group keeps initiative-local `task.json` records under `plan/**/.wt/tasks/**` as the authoritative live task surface.
- `create` materializes one new live task record under the matching initiative root.
- `update` applies bounded field changes without manual JSON editing.
- `transition` is a narrower handoff-oriented wrapper for status, owner, and blocker changes.
- If a task links to any `trace.*` value through `related_ids`, the task must also publish the matching `trace_id`.
- Task statuses that start or imply real execution (`in_progress`, `in_review`, `completed`) require the initiative package to have already been approved into `ready_for_execution`.
- Live task updates do not move between docs-backed open and closed directories. Terminal state is represented directly in the initiative-local task record.
- The first execution-starting task transition moves an approved initiative package from `ready_for_execution` into `in_progress` and records an `execution_started` initiative event.
- In write mode, all leaf commands refresh the live task, initiative, readiness, artifact, and coordination surfaces plus their companion rendered views.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan task create` | Creates one initiative-local live task record. |
| `watchtower-core plan task update` | Applies structured field updates to one live task record. |
| `watchtower-core plan task transition` | Applies a handoff-style status or ownership transition. |
| `watchtower-core plan approve` | Required before task transitions can begin real execution on a live initiative package. |
| `watchtower-core plan query tasks` | Reads the task index refreshed by task write operations. |
| `watchtower-core sync coordination` | Rebuilds the same coordination slice that task write operations refresh. |
| `watchtower-core plan closeout initiative` | Use after task transitions leave a live `plan/**` initiative package with only terminal task state. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/tasks.py`
- `plan/python/src/watchtower_plan/task_lifecycle.py`

## Updated At
- `2026-03-18T20:35:00Z`
