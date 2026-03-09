# `watchtower-core query decisions`

## Summary
This command searches the governed decision index so engineers and agents can find durable decision records by trace, decision status, linked PRD, or free-text planning context.

## Use When
- You need to find accepted or proposed decisions without opening the raw decision index JSON directly.
- You want to find the decisions linked to a PRD or trace without scanning decision records manually.
- You want machine-readable decision lookup results for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query decisions` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query decisions [--query <text>] [--trace-id <trace_id>] [--decision-status <status>] [--tag <tag>] [--linked-prd-id <prd_id>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed decision fields such as IDs, title, summary, tags, and linked surfaces.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--decision-status <status>`: Exact decision-status filter such as `accepted` or `proposed`.
- `--tag <tag>`: Exact tag filter.
- `--linked-prd-id <prd_id>`: Exact linked-PRD filter such as `prd.core_python_foundation`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query decisions --decision-status accepted
```

```sh
cd core/python
uv run watchtower-core query decisions --linked-prd-id prd.core_python_foundation --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching decision IDs, titles, and summaries.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and result records.
- If no entries match the requested filters, the command exits successfully and reports that no decision entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync decision-index` | Rebuilds the decision index that this command reads. |
| `watchtower-core query trace` | Resolves a joined trace record when you already know the trace ID and want linked planning surfaces. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/decisions.py`
- `core/control_plane/indexes/decisions/decision_index.v1.json`

## Updated At
- `2026-03-09T07:21:07Z`
