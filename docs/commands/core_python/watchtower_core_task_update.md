# `watchtower-core task update`

## Summary
This command applies structured field or body updates to one governed local task record and refreshes the coordination slice in write mode.

## Use When
- You need to change task metadata, scope, completion criteria, blockers, dependencies, or path placement without hand-editing front matter.
- You want to move a task between `open/` and `closed/` based on terminal or non-terminal status.
- You want dry-run preview before mutating the canonical task document.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core task update` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/task_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core task update --task-id <task_id> [--trace-id <trace_id> | --clear-trace-id] [--title <title>] [--summary <summary>] [--task-kind <kind>] [--priority <priority>] [--owner <owner>] [--task-status <status>] [--scope <item>] [--done-when <item>] [--applies-to <path_or_concept> | --clear-applies-to] [--related-id <id> | --clear-related-ids] [--depends-on <task_id> | --clear-depends-on] [--blocked-by <task_id> | --clear-blocked-by] [--file-stem <stem>] [--updated-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--task-id <task_id>`: Stable task identifier to update.
- `--trace-id <trace_id>`: Replacement trace identifier.
- `--clear-trace-id`: Remove the current trace identifier.
- `--title <title>`: Replacement task title.
- `--summary <summary>`: Replacement task summary.
- `--task-kind <feature|bug|chore|documentation|governance|research>`: Replacement governed task kind.
- `--priority <critical|high|medium|low>`: Replacement governed task priority.
- `--owner <owner>`: Replacement task owner.
- `--task-status <status>`: Replacement task execution status.
- `--scope <item>`: Replacement scope item. Repeat for multiple values.
- `--done-when <item>`: Replacement completion condition. Repeat for multiple values.
- `--applies-to <path_or_concept>`: Replacement applies-to value. Repeat for multiple values.
- `--clear-applies-to`: Remove the current applies-to list.
- `--related-id <id>`: Replacement related ID. Repeat for multiple values.
- `--clear-related-ids`: Remove the current related ID list.
- `--depends-on <task_id>`: Replacement dependency task ID. Repeat for multiple values.
- `--clear-depends-on`: Remove the current dependency list.
- `--blocked-by <task_id>`: Replacement blocker task ID. Repeat for multiple values.
- `--clear-blocked-by`: Remove the current blocker list.
- `--file-stem <stem>`: Optional replacement filename stem. The task ID remains authoritative.
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.
- `--write`: Persist the updated task document and refresh the coordination slice.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core task update --task-id task.example.001 --task-status in_progress --owner implementation_engineer
```

```sh
cd core/python
uv run watchtower-core task update --task-id task.example.001 --blocked-by task.other.001 --depends-on task.other.001 --write
```

```sh
cd core/python
uv run watchtower-core task update --task-id task.example.001 --clear-blocked-by --clear-depends-on --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate files.
- Replacement list flags overwrite the current value set. Use the matching clear flag when you want to remove a list field or `trace_id`.
- The command rejects path collisions, invalid task-state vocabulary, conflicting replacement and clear flags, and unresolved blocker or dependency task IDs.
- If the resulting task status changes terminality, write mode moves the task document between `docs/planning/tasks/open/` and `docs/planning/tasks/closed/`.
- In `json` mode, the command prints one JSON object with the resulting task metadata, path outcome, write state, and `closeout_recommended` hint.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core task` | Parent command group for task lifecycle operations. |
| `watchtower-core task create` | Creates the original task record. |
| `watchtower-core task transition` | Applies a narrower handoff-style update when full field updates are not needed. |
| `watchtower-core query tasks` | Reads the task index refreshed in write mode. |
| `watchtower-core sync coordination` | Rebuilds the same coordination slice that write mode refreshes. |

## Source Surface
- `core/python/src/watchtower_core/cli/task_family.py`
- `core/python/src/watchtower_core/cli/task_handlers.py`
- `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`

## Updated At
- `2026-03-10T22:54:30Z`
