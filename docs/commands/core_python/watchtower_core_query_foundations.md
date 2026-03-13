# `watchtower-core query foundations`

## Summary
This command searches the governed foundation index so engineers and agents can find repository intent documents by topic, authority, related surface, or downstream citation or application use.

## Use When
- You need to know which foundation document governs a repo surface such as `core/python/` or `workflows/modules/`.
- You want to check whether a foundation document is only cited or is explicitly applied by a standard, workflow, or planning doc.
- You want machine-readable foundation lookup results for scripts, workflows, or agent calls.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query foundations` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_knowledge_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query foundations [--query <text>] [--foundation-id <foundation_id>] [--audience <audience>] [--authority <authority>] [--tag <tag>] [--related-path <path>] [--reference-path <doc_path>] [--cited-by-path <doc_path>] [--applied-by-path <doc_path>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed foundation fields such as ID, title, summary, aliases, and related paths.
- `--foundation-id <foundation_id>`: Exact foundation identifier such as `foundation.engineering_design_principles`.
- `--audience <audience>`: Exact audience filter such as `shared`.
- `--authority <authority>`: Exact authority filter such as `authoritative` or `supporting`.
- `--tag <tag>`: Exact tag filter.
- `--related-path <path>`: Exact repository-path filter such as `core/python/` or `workflows/modules/`.
- `--reference-path <doc_path>`: Exact governed reference-doc filter such as `docs/references/github_collaboration_reference.md`.
- `--cited-by-path <doc_path>`: Exact doc-path filter for documents that cite the foundation doc.
- `--applied-by-path <doc_path>`: Exact doc-path filter for documents that apply the foundation doc in an applied-reference section.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query foundations --query philosophy
```

```sh
cd core/python
uv run watchtower-core query foundations --related-path core/python/
```

```sh
cd core/python
uv run watchtower-core query foundations --reference-path docs/references/uv_reference.md --format json
```

```sh
cd core/python
uv run watchtower-core query foundations --applied-by-path docs/standards/engineering/engineering_best_practices_standard.md --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching foundation IDs, authorities, titles, summaries, and current citation or application counts.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, and reference-capture fields such as `audience`, `reference_doc_paths`, `internal_reference_paths`, `external_reference_urls`, `cited_by_paths`, and `applied_by_paths`.
- If no entries match the requested filters, the command exits successfully and reports that no foundation entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync foundation-index` | Rebuilds the foundation index that this command reads. |
| `watchtower-core query references` | Searches the reference index when you know the source authority topic but not the governing foundation doc. |
| `watchtower-core query standards` | Searches the standard index when you want the downstream governed rules that apply one foundation doc. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_knowledge_family.py`
- `core/python/src/watchtower_core/cli/query_knowledge_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/foundations.py`
- `core/control_plane/indexes/foundations/foundation_index.v1.json`

## Updated At
- `2026-03-13T21:57:29Z`
