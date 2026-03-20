# `watchtower-core plan task update`

## Summary
This command applies structured field updates to one initiative-local live task record and refreshes derived plan-workspace surfaces in write mode.

## Use When
- You need to change task metadata, scope, completion criteria, blockers, or dependencies without hand-editing task JSON.
- You want to update one live task in place rather than moving docs-backed task files around.
- You want dry-run preview before mutating the canonical live task record.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan task update` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/tasks.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan task update --task-id <task_id> [--title <title>] [--summary <summary>] [--task-kind <kind>] [--priority <priority>] [--owner <owner>] [--task-status <status>] [--scope <item>] [--done-when <item>] [--applies-to <path_or_concept> | --clear-applies-to] [--related-id <id> | --clear-related-ids] [--depends-on <task_id> | --clear-depends-on] [--blocked-by <task_id> | --clear-blocked-by] [--updated-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--task-id <task_id>`: Stable task identifier to update.
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
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now when changes occur.
- `--write`: Persist the updated live task record and refresh the derived plan surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan task update --task-id task.example.001 --task-status in_progress --owner implementation_engineer
```

```sh
cd core/python
uv run watchtower-core plan task update --task-id task.example.001 --blocked-by task.other.001 --depends-on task.other.001 --write
```

```sh
cd core/python
uv run watchtower-core plan task update --task-id task.example.001 --clear-blocked-by --clear-depends-on --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate files.
- Replacement list flags overwrite the current value set. Use the matching clear flag when you want to remove a list field.
- The command rejects path collisions, invalid task-state vocabulary, conflicting replacement and clear flags, and unresolved blocker or dependency task IDs.
- If `related_ids` include any `trace.*` value, the resulting task must keep the matching `trace_id`.
- Execution-starting statuses such as `in_progress`, `in_review`, and `completed` require the initiative package to have already been approved into `ready_for_execution`.
- Live task updates stay under the same initiative-local `task.json` path; terminality is represented by `task_status`, not by moving files between open and closed docs directories.
- In write mode, the command refreshes the live task, initiative, readiness, artifact, and coordination surfaces plus companion rendered views.
- In `json` mode, the command prints one JSON object with the resulting task metadata, path outcome, write state, and `closeout_recommended` hint.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan task` | Parent command group for task lifecycle operations. |
| `watchtower-core plan task create` | Creates the original task record. |
| `watchtower-core plan task transition` | Applies a narrower handoff-style update when full field updates are not needed. |
| `watchtower-core plan approve` | Required before status updates can start real execution on a live initiative package. |
| `watchtower-core plan query tasks` | Reads the task index refreshed in write mode. |
| `watchtower-core plan sync coordination` | Rebuilds the same coordination slice that write mode refreshes. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/tasks.py`
- `plan/python/src/watchtower_plan/task_lifecycle.py`

## Updated At
- `2026-03-18T20:35:00Z`
