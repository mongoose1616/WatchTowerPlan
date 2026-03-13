# `watchtower-core task create`

## Summary
This command creates one governed local task document from compact structured inputs and refreshes the coordination slice in write mode.

## Use When
- You need a new bounded local task record without hand-editing front matter.
- You want the task tracker, task index, traceability, initiative, and coordination surfaces to stay aligned when the new task is written.
- You want dry-run preview before creating the canonical task document.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core task create` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/task_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core task create --task-id <task_id> --title <title> --summary <summary> --task-kind <kind> --priority <priority> --owner <owner> --scope <item> --done-when <item> [--trace-id <trace_id>] [--task-status <status>] [--applies-to <path_or_concept>] [--related-id <id>] [--depends-on <task_id>] [--blocked-by <task_id>] [--file-stem <stem>] [--updated-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--task-id <task_id>`: Stable task identifier.
- `--title <title>`: Human-readable task title.
- `--summary <summary>`: One-line task summary used in trackers and indexes.
- `--task-kind <feature|bug|chore|documentation|governance|research>`: Governed task kind.
- `--priority <critical|high|medium|low>`: Governed task priority.
- `--owner <owner>`: Current task owner.
- `--scope <item>`: Scope item. Repeat for multiple values.
- `--done-when <item>`: Completion condition. Repeat for multiple values.
- `--trace-id <trace_id>`: Optional linked trace identifier.
- `--task-status <status>`: Initial task status. Defaults to `backlog`.
- `--applies-to <path_or_concept>`: Optional applied surface or concept. Repeat for multiple values.
- `--related-id <id>`: Optional related planning or governance ID. Repeat for multiple values.
- `--depends-on <task_id>`: Optional dependency task ID. Repeat for multiple values.
- `--blocked-by <task_id>`: Optional blocker task ID. Repeat for multiple values.
- `--file-stem <stem>`: Optional filename stem. Defaults to a slug derived from the title.
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now.
- `--write`: Persist the task document and refresh the coordination slice.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core task create --task-id task.example.001 --title "Draft the example" --summary "Creates the example task." --task-kind documentation --priority medium --owner repository_maintainer --scope "Write the example" --done-when "The example exists"
```

```sh
cd core/python
uv run watchtower-core task create --task-id task.traceable.example.001 --trace-id trace.example --title "Implement the slice" --summary "Implements the bounded slice." --task-kind feature --priority high --owner implementation_engineer --applies-to core/python/src/ --related-id design.features.example --scope "Ship the slice" --done-when "Tests pass" --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not create or modify files.
- The command rejects duplicate task IDs, path collisions, invalid task-state vocabulary, and unresolved blocker or dependency task IDs.
- If any `--related-id` value is a `trace.*` identifier, `--trace-id` becomes required and must match that traced linkage.
- In write mode, the command writes one Markdown task record under `docs/planning/tasks/open/` or `docs/planning/tasks/closed/` based on the requested task status and refreshes the deterministic coordination slice.
- In `human` mode, the command prints the target task path, resulting task status, owner, and whether write mode refreshed coordination.
- In `json` mode, the command prints one JSON object with the task metadata, path outcome, write state, and a `closeout_recommended` hint when the resulting traced task set is fully terminal.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core task` | Parent command group for task lifecycle operations. |
| `watchtower-core task update` | Applies later structured updates to the created task. |
| `watchtower-core task transition` | Applies a narrower handoff-style update to the created task. |
| `watchtower-core query tasks` | Reads the task index refreshed in write mode. |
| `watchtower-core sync coordination` | Rebuilds the same coordination slice that write mode refreshes. |

## Source Surface
- `core/python/src/watchtower_core/cli/task_family.py`
- `core/python/src/watchtower_core/cli/task_handlers.py`
- `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`

## Updated At
- `2026-03-13T04:05:00Z`
