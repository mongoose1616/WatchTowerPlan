# `watchtower-core query tasks`

## Summary
This command searches the governed task index so engineers and agents can find local task records by task ID, task status, owner, trace, blockers, dependencies, priority, task kind, or free-text execution context.

## Use When
- You need to find active or closed local tasks without opening the raw task index JSON directly.
- You want to filter work by owner, task status, or trace.
- You want machine-readable task lookup results for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query tasks` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_coordination_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query tasks [--query <text>] [--task-id <task_id>] [--trace-id <trace_id>] [--task-status <task_status>] [--priority <priority>] [--owner <owner>] [--task-kind <task_kind>] [--blocked-only] [--blocked-by <task_id>] [--depends-on <task_id>] [--include-dependency-details] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed task fields such as IDs, title, summary, owner, related IDs, and applies-to paths.
- `--task-id <task_id>`: Exact task identifier filter. Repeat for multiple task IDs.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.local_task_tracking`.
- `--task-status <task_status>`: Exact task-status filter such as `backlog`, `in_progress`, or `done`.
- `--priority <priority>`: Exact priority filter such as `critical`, `high`, `medium`, or `low`.
- `--owner <owner>`: Exact owner filter such as `repository_maintainer`.
- `--task-kind <task_kind>`: Exact task-kind filter such as `feature`, `bug`, or `chore`.
- `--blocked-only`: Return only tasks that list one or more blocking task IDs.
- `--blocked-by <task_id>`: Return only tasks blocked by the given task ID.
- `--depends-on <task_id>`: Return only tasks that depend on the given task ID.
- `--include-dependency-details`: Include forward and reverse dependency detail in the result payload or human output.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query tasks --task-status backlog
```

```sh
cd core/python
uv run watchtower-core query tasks --blocked-only --include-dependency-details
```

```sh
cd core/python
uv run watchtower-core query tasks --trace-id trace.local_task_tracking --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching task IDs, task statuses, priorities, titles, summaries, and optional dependency detail when requested.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and result records.
- If no entries match the requested filters, the command exits successfully and reports that no task entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync task-index` | Rebuilds the task index that this command reads. |
| `watchtower-core sync task-tracking` | Rebuilds the human-readable task tracker derived from the same task records. |
| `watchtower-core query trace` | Resolves a joined trace record when you already know the trace ID and want linked task IDs. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/tasks.py`
- `core/control_plane/indexes/tasks/task_index.v1.json`

## Updated At
- `2026-03-13T23:21:33Z`
