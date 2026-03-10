# `watchtower-core task`

## Summary
This command group creates, updates, and transitions governed local task records while keeping task documents authoritative and refreshing the coordination slice in write mode.

## Use When
- You want help for the governed local task lifecycle without hand-editing front matter.
- You need to create one new task, apply structured field updates, or perform a bounded handoff-style transition.
- You want dry-run preview before mutating the canonical task corpus and its derived coordination mirrors.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core task` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/task_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core task <task_command> [args]
```

## Arguments and Options
- `<task_command>`: Choose `create`, `update`, or `transition`.
- `-h`, `--help`: Show the command help text.
- Task mutations are dry-run by default. Pass `--write` to the selected leaf command to persist the task change and refresh the coordination slice.

## Examples
```sh
cd core/python
uv run watchtower-core task --help
```

```sh
cd core/python
uv run watchtower-core task create --task-id task.example.001 --title "Draft the example" --summary "Creates the example task." --task-kind documentation --priority medium --owner repository_maintainer --scope "Write the example" --done-when "The example exists"
```

```sh
cd core/python
uv run watchtower-core task update --task-id task.example.001 --task-status in_progress --owner implementation_engineer --format json
```

```sh
cd core/python
uv run watchtower-core task transition --task-id task.example.001 --task-status done --write
```

## Behavior and Outputs
- With no leaf command, the current implementation prints task-specific help and exits successfully.
- The command group keeps task Markdown files under `docs/planning/tasks/` as the authoritative source of truth.
- `create` materializes a new governed task document from compact structured inputs.
- `update` applies bounded front-matter or body-section changes without manual editing.
- `transition` is a narrower handoff-oriented wrapper for status, owner, and blocker changes.
- In write mode, all leaf commands refresh the deterministic coordination slice so task, traceability, initiative, and coordination views stay aligned.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core task create` | Creates one governed local task document. |
| `watchtower-core task update` | Applies structured field or body updates to one task. |
| `watchtower-core task transition` | Applies a handoff-style status or ownership transition. |
| `watchtower-core query tasks` | Reads the task index refreshed by task write operations. |
| `watchtower-core sync coordination` | Rebuilds the same coordination slice that task write operations refresh. |
| `watchtower-core closeout initiative` | Use after task transitions leave a traced initiative with only terminal task state. |

## Source Surface
- `core/python/src/watchtower_core/cli/task_family.py`
- `core/python/src/watchtower_core/cli/task_handlers.py`
- `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`

## Updated At
- `2026-03-10T22:54:30Z`
