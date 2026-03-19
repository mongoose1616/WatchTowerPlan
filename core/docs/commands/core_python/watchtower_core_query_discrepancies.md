# `watchtower-core query discrepancies`

## Summary
This command searches the live discrepancy index for mismatch, drift, and stale-surface records captured in the plan workspace.

## Use When
- You need to inspect blocking discrepancies without opening one initiative package directly.
- You want machine-readable discrepancy results for an agent, workflow, or script.
- You need to filter discrepancy state by trace, category, severity, or current status.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query discrepancies` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query discrepancies [--query <text>] [--initiative-id <initiative_id>] [--project-id <project_id>] [--trace-id <trace_id>] [--category <category>] [--severity <severity>] [--status <status>] [--blocking-only] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over discrepancy fields such as IDs, title, summary, category, and source paths.
- `--initiative-id <initiative_id>`: Exact initiative identifier such as `initiative.plan_live_query_authority_cutover`.
- `--project-id <project_id>`: Exact project identifier such as `project.watchtower`.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.plan_core_documentation_template_authority_foundation`.
- `--category <category>`: Exact discrepancy category such as `stale_aggregate_index` or `scope_mismatch`.
- `--severity <severity>`: Exact severity filter such as `low`, `high`, or `critical`.
- `--status <status>`: Exact discrepancy status such as `open` or `resolved`.
- `--blocking-only`: Return only discrepancies that block readiness or execution.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query discrepancies --blocking-only
```

```sh
cd core/python
uv run watchtower-core query discrepancies --trace-id trace.plan_core_documentation_template_authority_foundation --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints discrepancy IDs, severity, gate effect, current status, and source paths.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and discrepancy-entry records.
- The command reads `plan/.wt/indexes/discrepancy_index.json`.
- If no entries match the requested filters, the command exits successfully and reports that no discrepancy entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query readiness` | Surfaces the execution gate state affected by blocking discrepancies. |
| `watchtower-core query coordination` | Pack-level start-here path before narrowing to mismatch details. |
| `watchtower-core query authority` | Resolves when discrepancy lookup is the canonical surface. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `core/python/src/watchtower_core/plan_runtime/query/discrepancies.py`
- `plan/.wt/indexes/discrepancy_index.json`

## Updated At
- `2026-03-17T19:13:00Z`
