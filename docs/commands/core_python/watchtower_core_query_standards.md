# `watchtower-core query standards`

## Summary
This command searches the governed standard index so engineers and agents can find standards and best-practice docs by category, related repo surface, reference doc, or free-text governance context.

## Use When
- You need to find the governing standard for a repo surface without browsing `docs/standards/` manually.
- You want to know which standards currently rely on a given local reference doc under `docs/references/`.
- You want machine-readable standard lookup results for workflows, scripts, or agent calls.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query standards` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query standards [--query <text>] [--standard-id <standard_id>] [--category <category>] [--owner <owner>] [--tag <tag>] [--applies-to <target>] [--related-path <path>] [--reference-path <doc_path>] [--operationalization-mode <mode>] [--operationalization-path <path>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed standard fields such as ID, title, summary, category, references, and related paths.
- `--standard-id <standard_id>`: Exact standard identifier such as `std.engineering.best_practices`.
- `--category <category>`: Exact standards-category filter such as `governance` or `engineering`.
- `--owner <owner>`: Exact owner filter such as `repository_maintainer`.
- `--tag <tag>`: Exact tag filter.
- `--applies-to <target>`: Exact authored `applies_to` filter such as `core/python/` or `docs/standards/`.
- `--related-path <path>`: Exact repository-path filter such as `.github/` or `core/python/`.
- `--reference-path <doc_path>`: Exact governed reference-doc filter such as `docs/references/github_collaboration_reference.md`.
- `--operationalization-mode <mode>`: Exact operationalization-mode filter such as `validation`, `query`, or `workflow`.
- `--operationalization-path <path>`: Repository-path filter for one operationalizing surface such as `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`. Exact file paths match directly, and indexed directory paths also match concrete descendants under that directory.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query standards --category governance
```

```sh
cd core/python
uv run watchtower-core query standards --operationalization-mode validation
```

```sh
cd core/python
uv run watchtower-core query standards --reference-path docs/references/github_collaboration_reference.md --format json
```

```sh
cd core/python
uv run watchtower-core query standards --related-path .github/
```

```sh
cd core/python
uv run watchtower-core query standards --operationalization-path docs/planning/prds/reference_and_workflow_standards_alignment.md --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- `--operationalization-path` matches both exact indexed files and concrete descendant files when a standard operationalizes a directory path such as `docs/planning/prds/`.
- In `human` mode, the command prints matching standard IDs, categories, owners, titles, summaries, and compact operationalization metadata.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, and indexed retrieval fields such as `owner`, `applies_to`, `reference_doc_paths`, `operationalization_modes`, and `operationalization_paths`.
- If no entries match the requested filters, the command exits successfully and reports that no standard entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core sync standard-index` | Rebuilds the standard index that this command reads. |
| `watchtower-core query references` | Searches the reference index when you know the local reference doc but not the governed standard. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/repo_ops/query/standards.py`
- `core/control_plane/indexes/standards/standard_index.v1.json`

## Updated At
- `2026-03-12T00:18:45Z`
