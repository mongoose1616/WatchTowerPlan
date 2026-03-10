# `watchtower-core query coordination`

## Summary
This command is the explicit machine start-here path for active traced initiative coordination, including phase, owners, actionable tasks, blockers, and next-step guidance.

## Use When
- You want the active initiative view without reopening PRDs, designs, tasks, and traceability separately.
- You need machine-readable coordination output for an agent, workflow, or script.
- You want compact active-task summaries and the next surface to open first.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query coordination` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query coordination [--query <text>] [--trace-id <trace_id>] [--initiative-status <status>] [--current-phase <phase>] [--owner <owner>] [--blocked-only] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over initiative coordination fields such as trace ID, title, next action, and active-task summaries.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--initiative-status <status>`: Exact initiative-status filter such as `active`, `completed`, or `superseded`. Defaults to `active` when omitted.
- `--current-phase <phase>`: Exact current-phase filter such as `prd`, `execution`, `validation`, or `closed`.
- `--owner <owner>`: Exact active-owner filter such as `repository_maintainer`.
- `--blocked-only`: Return only initiatives with one or more currently blocked active tasks.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Notes
- This command defaults to active initiatives because it is the coordination start-here path.
- Use `watchtower-core query initiatives` when you want broader initiative-family lookup or closed-history browsing without the active-only default.

## Examples
```sh
cd core/python
uv run watchtower-core query coordination
```

```sh
cd core/python
uv run watchtower-core query coordination --blocked-only --format json
```

```sh
cd core/python
uv run watchtower-core query coordination --initiative-status completed --trace-id trace.core_python_foundation
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- With no explicit `--initiative-status`, the command defaults to `active`.
- In `human` mode, the command prints matching initiatives, active-owner projection, open-task counts, compact task summaries, and the next surface to open first.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, and the active-only default when it was applied.
- If no entries match the requested filters, the command exits successfully and suggests using `query initiatives` or an explicit `--initiative-status` for closed history.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core query initiatives` | Broader initiative-family lookup surface, including closed-history inspection. |
| `watchtower-core sync initiative-index` | Rebuilds the initiative index that this command reads. |
| `watchtower-core sync initiative-tracking` | Rebuilds the human-readable tracker derived from the same initiative view. |
| `watchtower-core query tasks` | Inspects the full task records behind the compact active-task summaries. |
| `watchtower-core query trace` | Resolves the underlying traceability record for one known trace ID. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/repo_ops/query/initiatives.py`
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`

## Updated At
- `2026-03-10T18:10:36Z`
