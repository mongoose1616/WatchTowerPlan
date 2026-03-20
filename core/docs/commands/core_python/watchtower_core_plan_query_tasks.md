# `watchtower-core plan query tasks`

## Summary
This command searches the live plan task index so engineers and agents can find initiative-local task records by task ID, task status, owner, trace, blockers, dependencies, priority, task kind, or free-text execution context.

## Use When
- You need to find active or closed local tasks without opening the raw task index JSON directly.
- You want to filter work by owner, task status, or trace.
- You want machine-readable task lookup results for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan query tasks` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/query.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan query tasks [--query <text>] [--task-id <task_id>] [--trace-id <trace_id>] [--task-status <task_status>] [--priority <priority>] [--owner <owner>] [--task-kind <task_kind>] [--blocked-only] [--blocked-by <task_id>] [--depends-on <task_id>] [--include-dependency-details] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed task fields such as IDs, title, summary, owner, related IDs, and applies-to paths.
- `--task-id <task_id>`: Exact task identifier filter. Repeat for multiple task IDs.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.plan_live_query_authority_cutover`.
- `--task-status <task_status>`: Exact task-status filter such as `planned`, `ready`, `in_progress`, `in_review`, `blocked`, `completed`, or `cancelled`.
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
uv run watchtower-core plan query tasks --task-status planned
```

```sh
cd core/python
uv run watchtower-core plan query tasks --blocked-only --include-dependency-details
```

```sh
cd core/python
uv run watchtower-core plan query tasks --trace-id trace.plan_live_query_authority_cutover --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching task IDs, task statuses, priorities, titles, summaries, and optional dependency detail when requested.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and result records.
- The command reads `plan/.wt/indexes/task_index.json` and exposes initiative ID, project ID when present, and dependency links from live initiative-local task state.
- `watchtower-core sync github-tasks` uses the same live task query semantics for dry-run and write-mode selection, then loads the matched initiative-local task records before applying GitHub updates.
- If no entries match the requested filters, the command exits successfully and reports that no task entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan query` | Parent command group for all plan-owned index-backed lookup commands. |
| `watchtower-core sync all` | Rebuilds the live task index and its rendered companions. |
| `watchtower-core plan query trace` | Resolves a joined trace record when you already know the trace ID and want linked task IDs. |
| `watchtower-core sync github-tasks` | Uses the same live task filters, then previews or applies GitHub sync for the matched initiative-local task records. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/query.py`
- `plan/python/src/watchtower_plan/cli/query_lookup_handlers.py`
- `plan/python/src/watchtower_plan/query/tasks.py`
- `plan/.wt/indexes/task_index.json`

## Updated At
- `2026-03-18T00:00:00Z`
