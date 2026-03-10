# `watchtower-core query workflows`

## Summary
This command searches the governed workflow index so engineers and agents can find workflow modules by behavior, governing source, or related repository path.

## Use When
- You know the behavior or governing source you need, but not yet the exact workflow module name.
- You want to confirm which workflow module cites a specific standard, reference doc, or canonical file.
- You want machine-readable workflow lookup results for scripts, workflows, or agent calls.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query workflows` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query workflows [--query <text>] [--workflow-id <workflow_id>] [--related-path <path>] [--reference-path <doc_path>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed workflow fields such as workflow ID, title, summary, related paths, and references.
- `--workflow-id <workflow_id>`: Exact workflow identifier such as `workflow.code_validation`.
- `--related-path <path>`: Exact repository-path filter such as `docs/standards/documentation/workflow_md_standard.md`.
- `--reference-path <doc_path>`: Exact governed reference-doc filter such as `docs/references/github_collaboration_reference.md`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query workflows --query validation
```

```sh
cd core/python
uv run watchtower-core query workflows --related-path docs/standards/documentation/workflow_md_standard.md
```

```sh
cd core/python
uv run watchtower-core query workflows --reference-path docs/references/github_collaboration_reference.md --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching workflow IDs, titles, summaries, and current internal or external reference use.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, and reference-capture fields such as `reference_doc_paths`, `internal_reference_paths`, and `external_reference_urls`.
- If no entries match the requested filters, the command exits successfully and reports that no workflow entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync workflow-index` | Rebuilds the workflow index that this command reads. |
| `watchtower-core query standards` | Searches the standard index when you know the governing standard but not the workflow module. |
| `watchtower-core query references` | Searches the reference index when you know the source authority topic but not the workflow module. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/workflows.py`
- `core/control_plane/indexes/workflows/workflow_index.v1.json`

## Updated At
- `2026-03-09T23:59:23Z`
