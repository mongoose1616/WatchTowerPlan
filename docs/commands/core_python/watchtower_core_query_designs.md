# `watchtower-core query designs`

## Summary
This command searches the governed design-document index so engineers and agents can find feature designs and implementation plans by trace, family, tag, or free-text planning context.

## Use When
- You need to find a feature design or implementation plan without opening the raw design-document index JSON directly.
- You want to filter design documents by family or trace instead of scanning planning docs manually.
- You want machine-readable design lookup results for a workflow, script, or agent.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query designs` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query designs [--query <text>] [--trace-id <trace_id>] [--family <family>] [--tag <tag>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed design fields such as IDs, title, summary, tags, and linked paths.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--family <family>`: Exact design-family filter such as `feature_design` or `implementation_plan`.
- `--tag <tag>`: Exact tag filter.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query designs --family feature_design
```

```sh
cd core/python
uv run watchtower-core query designs --trace-id trace.core_python_foundation --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching design-document IDs, titles, summaries, and whether the design explicitly used internal or external references.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, and reference-use indicators captured in the design-document index.
- If no entries match the requested filters, the command exits successfully and reports that no design-document entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync design-document-index` | Rebuilds the design-document index that this command reads. |
| `watchtower-core query trace` | Resolves a joined trace record when you already know the trace ID and want linked planning surfaces. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/repo_ops/query/designs.py`
- `core/control_plane/indexes/design_documents/design_document_index.v1.json`

## Updated At
- `2026-03-12T22:05:00Z`
