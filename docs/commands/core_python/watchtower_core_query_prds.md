# `watchtower-core query prds`

## Summary
This command searches the governed PRD index so engineers and agents can find PRDs by trace, requirement ID, acceptance ID, or free-text planning context.

## Use When
- You need to find the PRD for a trace or initiative without opening the raw PRD index JSON directly.
- You want to search by requirement ID or acceptance ID instead of scanning PRDs manually.
- You want machine-readable PRD lookup results for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query prds` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_records_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query prds [--query <text>] [--trace-id <trace_id>] [--tag <tag>] [--requirement-id <requirement_id>] [--acceptance-id <acceptance_id>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed PRD fields such as IDs, title, summary, tags, and linked surfaces.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--tag <tag>`: Exact tag filter.
- `--requirement-id <requirement_id>`: Exact requirement-ID filter such as `req.core_python_foundation.003`.
- `--acceptance-id <acceptance_id>`: Exact acceptance-ID filter such as `ac.core_python_foundation.002`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query prds --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query prds --requirement-id req.core_python_foundation.003 --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching PRD IDs, titles, summaries, and whether the PRD explicitly used internal or external references.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, and reference-use indicators captured in the PRD index.
- If no entries match the requested filters, the command exits successfully and reports that no PRD entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync prd-index` | Rebuilds the PRD index that this command reads. |
| `watchtower-core query trace` | Resolves a joined trace record when you already know the trace ID and want linked planning surfaces. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_records_family.py`
- `core/python/src/watchtower_core/cli/query_records_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/prds.py`
- `core/control_plane/indexes/prds/prd_index.v1.json`

## Updated At
- `2026-03-13T21:57:29Z`
