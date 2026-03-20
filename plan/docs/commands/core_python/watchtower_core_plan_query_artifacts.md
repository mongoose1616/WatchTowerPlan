# `watchtower-core plan query artifacts`

## Summary
This command searches the live plan artifact index for cross-family machine artifacts, aggregate indexes, and their canonical context metadata.

## Use When
- You need one read-only lookup surface across initiative-local artifacts, project-local machine artifacts, pack work-item notes, and pack-level aggregate indexes.
- You want canonical artifact paths, context IDs, or rendered companions without crawling `plan/**` manually.
- You need machine-readable artifact inventory results for scripts, workflows, or agent use.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan query artifacts` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/query.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan query artifacts [--query <text>] [--artifact-id <artifact_id>] [--artifact-family <family>] [--context-id <context_id>] [--source-context <context>] [--source-channel <channel>] [--status <status>] [--authoritative <true|false>] [--derived <true|false>] [--hidden <true|false>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over artifact fields such as IDs, family, path, title, summary, and context IDs.
- `--artifact-id <artifact_id>`: Exact artifact identifier such as `initiative.plan_artifact_index_runtime_foundation` or `index.artifacts`.
- `--artifact-family <family>`: Exact artifact-family filter such as `initiative_state`, `task_state`, `pack_work_item_note`, or `artifact_index`.
- `--context-id <context_id>`: Exact context filter such as `trace.plan_artifact_index_runtime_foundation`, `project.watchtower`, or `pack.plan`.
- `--source-context <context>`: Exact source-context filter such as `initiative.plan_artifact_index_runtime_foundation`, `project.watchtower`, or `bootstrap.plan.stage1_bootstrap`.
- `--source-channel <channel>`: Exact source-channel filter such as `initiative_package`, `project_container`, `event_stream`, `pack_work_item`, or `aggregate_index`.
- `--status <status>`: Exact artifact-status filter such as `ready_for_execution`, `planned`, `active`, or `completed`.
- `--authoritative <true|false>`: Filter by whether the artifact is authoritative.
- `--derived <true|false>`: Filter by whether the artifact is derived.
- `--hidden <true|false>`: Filter by whether the artifact lives on a hidden machine surface.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan query artifacts --artifact-family initiative_state
```

```sh
cd core/python
uv run watchtower-core plan query artifacts --context-id trace.plan_artifact_index_runtime_foundation --format json
```

```sh
cd core/python
uv run watchtower-core plan query artifacts --artifact-id index.artifacts
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints artifact ID, family, status, path, context IDs, provenance summary, and authority flags for matching entries.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and artifact-entry records.
- The command reads `plan/.wt/indexes/artifact_index.json`.
- The artifact index is the cross-family lookup authority for live plan machine artifacts and aggregate indexes; it is not a replacement for deep trace-linked planning context.
- If no entries match the requested filters, the command exits successfully and reports that no artifact entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan query coordination` | Start-here planning lookup before narrowing into specific artifacts. |
| `watchtower-core plan query initiatives` | Initiative-family browse view when the question is about initiative summaries rather than artifact inventory. |
| `watchtower-core plan query projects` | Project-container browse surface when you need project summaries rather than artifact-level results. |
| `watchtower-core plan query authority` | Resolves when the artifact index is the canonical lookup surface for a planning question. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/query.py`
- `plan/python/src/watchtower_plan/cli/query_lookup_handlers.py`
- `plan/python/src/watchtower_plan/query/artifacts.py`
- `plan/python/src/watchtower_plan/artifact_index.py`
- `plan/.wt/indexes/artifact_index.json`

## Updated At
- `2026-03-17T20:03:23Z`
