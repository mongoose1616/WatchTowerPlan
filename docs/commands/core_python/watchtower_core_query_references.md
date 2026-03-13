# `watchtower-core query references`

## Summary
This command searches the governed reference index so engineers and agents can find curated reference documents by topic, reference ID, repository-status maturity, local repository touchpoint, canonical upstream URL, or free-text lookup terms.

## Use When
- You want to find the right reference document without browsing `docs/references/` manually.
- You need to separate active-support references from supporting-authority or candidate-future guidance without scanning the whole corpus.
- You need to know whether a reference maps to a local repo surface such as `core/python/` or one of the standards directories.
- You want machine-readable lookup results for workflows, scripts, or agent calls.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query references` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_knowledge_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query references [--query <text>] [--reference-id <reference_id>] [--repository-status <candidate_future_guidance|supporting_authority|active_support>] [--tag <tag>] [--related-path <path>] [--upstream-url <url>] [--cited-by-path <doc_path>] [--applied-by-path <doc_path>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed reference fields such as reference ID, title, summary, upstream URLs, related paths, aliases, and tags.
- `--reference-id <reference_id>`: Exact reference identifier filter such as `ref.uv`.
- `--repository-status <status>`: Exact repository-status filter such as `supporting_authority`, `active_support`, or `candidate_future_guidance`.
- `--tag <tag>`: Exact tag filter such as `uv` or `reference`.
- `--related-path <path>`: Repository-path filter such as `core/python/` or `docs/standards/engineering/`. Directory paths ending in `/` match descendant touchpoints such as `core/python/pyproject.toml`.
- `--upstream-url <url>`: Exact canonical-upstream URL filter.
- `--cited-by-path <doc_path>`: Exact governed-doc filter for documents that cite the reference.
- `--applied-by-path <doc_path>`: Exact governed-doc filter for documents that apply the reference in an applied-reference section.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query references --query uv
```

```sh
cd core/python
uv run watchtower-core query references --repository-status candidate_future_guidance --format json
```

```sh
cd core/python
uv run watchtower-core query references --related-path core/python/ --format json
```

```sh
cd core/python
uv run watchtower-core query references --upstream-url https://docs.astral.sh/uv/
```

```sh
cd core/python
uv run watchtower-core query references --applied-by-path docs/standards/governance/github_collaboration_standard.md --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching reference IDs, lifecycle status, repository-status maturity, titles, summaries, whether the indexed document explicitly uses internal or external references, and whether the reference is currently cited or applied elsewhere.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, the derived `repository_status` field, and reverse-citation fields such as `cited_by_paths` and `applied_by_paths`.
- If no entries match the requested filters, the command exits successfully and reports that no reference entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync reference-index` | Rebuilds the reference index that this command reads. |
| `watchtower-core query paths` | Searches the repository path index when you know the path or surface instead of the reference topic. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_knowledge_family.py`
- `core/python/src/watchtower_core/cli/query_knowledge_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/references.py`
- `core/control_plane/indexes/references/reference_index.v1.json`

## Updated At
- `2026-03-13T21:57:29Z`
