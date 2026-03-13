# `watchtower-core query workflows`

## Summary
This command searches the governed workflow index so engineers and agents can find workflow modules by behavior, task-specific extra files to load, or related repository path.

## Use When
- You know the behavior or task-specific file you need, but not yet the exact workflow module name.
- You want to confirm which workflow module tells an agent to open a specific standard, template, reference doc, or canonical file next.
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
uv run watchtower-core query workflows [--query <text>] [--workflow-id <workflow_id>] [--phase-type <phase>] [--task-family <family>] [--trigger-tag <tag>] [--related-path <path>] [--reference-path <doc_path>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed workflow fields such as workflow ID, title, summary, extra load paths, and reference docs.
- `--workflow-id <workflow_id>`: Exact workflow identifier such as `workflow.code_validation`.
- `--phase-type <phase>`: Exact workflow phase filter such as `execution`, `validation`, or `reconciliation`.
- `--task-family <family>`: Exact workflow task-family filter such as `engineering_validation` or `traceability`.
- `--trigger-tag <tag>`: Exact trigger-tag filter such as `validation`, `github`, or `scope`.
- `--related-path <path>`: Exact repository-path filter such as `docs/templates/prd_template.md`.
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
uv run watchtower-core query workflows --query "current cli behavior"
```

```sh
cd core/python
uv run watchtower-core query workflows --query "successor tasks"
```

```sh
cd core/python
uv run watchtower-core query workflows --phase-type reconciliation
```

```sh
cd core/python
uv run watchtower-core query workflows --related-path docs/templates/prd_template.md
```

```sh
cd core/python
uv run watchtower-core query workflows --reference-path docs/references/github_collaboration_reference.md --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching workflow IDs, retrieval metadata, summaries, and any indexed task-specific files to load.
- In `json` mode, the command prints one JSON object with the command name, status, result count, result records, and workflow lookup fields such as `phase_type`, `task_family`, `trigger_tags`, `reference_doc_paths`, `internal_reference_paths`, and `external_reference_urls`.
- Trigger terms come from workflow titles, purpose summaries, retrieval metadata, and task-specific additional-load files, so adjacent route lookups such as `current cli behavior` and `successor tasks` can resolve without exact module names.
- Use workflow lookup to distinguish adjacent boundaries before opening the raw module docs: behavior docs versus implementation drift, schema-family coherence, traced planning drift, task-record lifecycle work, and task-phase handoff work.
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
- `core/python/src/watchtower_core/repo_ops/query/workflows.py`
- `core/control_plane/indexes/workflows/workflow_index.v1.json`

## Updated At
- `2026-03-13T21:17:49Z`
