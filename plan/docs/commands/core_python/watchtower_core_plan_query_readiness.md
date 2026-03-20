# `watchtower-core plan query readiness`

## Summary
This command searches the live readiness index for initiative execution-gate state, including capture completeness, approval status, and blocking reasons.

## Use When
- You need to know whether an initiative package is ready to start or resume execution.
- You want machine-readable readiness results for an agent, workflow, or script.
- You need to inspect capture, validation, review, or approval state without opening one initiative root directly.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan query readiness` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/query.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan query readiness [--query <text>] [--initiative-id <initiative_id>] [--project-id <project_id>] [--trace-id <trace_id>] [--lifecycle-stage <stage>] [--review-status <status>] [--ready-for-execution <true|false>] [--blocked-only] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over readiness fields such as trace ID, title, and blocking reasons.
- `--initiative-id <initiative_id>`: Exact initiative identifier such as `initiative.plan_live_query_authority_cutover`.
- `--project-id <project_id>`: Exact project identifier such as `project.watchtower`.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.plan_live_query_authority_cutover`.
- `--lifecycle-stage <stage>`: Exact lifecycle-stage filter such as `ready_for_execution`, `in_progress`, or `completed`.
- `--review-status <status>`: Exact review-status filter such as `approved` or `pending`.
- `--ready-for-execution <true|false>`: Filter by whether the initiative is currently marked ready for execution.
- `--blocked-only`: Return only readiness entries with one or more blocking reasons.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan query readiness --ready-for-execution true
```

```sh
cd core/python
uv run watchtower-core plan query readiness --trace-id trace.plan_live_query_authority_cutover --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints lifecycle stage, review state, readiness state, and any blocking reasons for matching initiatives.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and readiness-entry records.
- The command reads `plan/.wt/indexes/readiness_index.json`.
- If no entries match the requested filters, the command exits successfully and reports that no readiness entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan query coordination` | Machine start-here path for current live planning state before narrowing to readiness details. |
| `watchtower-core plan query discrepancies` | Shows blocking mismatches that can also affect readiness. |
| `watchtower-core plan query initiatives` | Shows the broader initiative-family state behind one readiness entry. |
| `watchtower-core plan query authority` | Resolves when readiness is the canonical lookup surface. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/query.py`
- `plan/python/src/watchtower_plan/cli/query_lookup_handlers.py`
- `plan/python/src/watchtower_plan/query/readiness.py`
- `plan/.wt/indexes/readiness_index.json`

## Updated At
- `2026-03-17T19:13:00Z`
