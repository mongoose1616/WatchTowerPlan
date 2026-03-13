# `watchtower-core query planning`

## Summary
This command searches the canonical planning catalog for one deep machine-readable planning record that joins trace-linked planning documents, tasks, acceptance contracts, validation evidence, and per-trace coordination state.

## Use When
- You already know the trace you want from `watchtower-core query coordination` and need the canonical deep planning record for it.
- You want filterless active-only browse over current traced planning work before deciding which active trace to open in full.
- You want explicit planning status semantics such as `artifact_status`, `initiative_status`, `record_status`, `decision_status`, and `task_status` instead of one ambiguous `status` field.
- You need one machine-readable record for PRD, decision, design, task, acceptance, evidence, and next-step lookup.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query planning` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_coordination_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query planning [--query <text>] [--trace-id <trace_id>] [--initiative-status <status>] [--current-phase <phase>] [--owner <owner>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over planning-catalog fields such as trace ID, titles, explicit status fields, next action, linked IDs, and related paths.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--initiative-status <status>`: Exact initiative-status filter such as `active`, `completed`, or `superseded`. When omitted for filterless browse, the command defaults to `active`.
- `--current-phase <phase>`: Exact current-phase filter such as `execution` or `closeout`.
- `--owner <owner>`: Exact owner filter against the current active owners for the trace.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query planning --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query planning --initiative-status active --format json
```

```sh
cd core/python
uv run watchtower-core query planning --current-phase execution --owner repository_maintainer
```

```sh
cd core/python
uv run watchtower-core query planning --initiative-status completed --trace-id trace.core_python_foundation --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching trace IDs, current phases, initiative statuses, owners, next-step guidance, and section counts for the joined planning record.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and full planning-catalog entries.
- With no explicit `--trace-id`, `--query`, `--current-phase`, `--owner`, or `--initiative-status`, the command defaults to `initiative_status=active` so filterless browse stays aligned with the active-first planning navigation model.
- The JSON payload uses explicit status fields inside the joined sections, including `artifact_status`, `initiative_status`, `record_status`, `decision_status`, and `task_status`.
- When that active-default path is applied, the JSON payload also includes `default_initiative_status: "active"` so machine consumers can tell the filter was injected by the entrypoint rather than supplied explicitly.
- This command is the canonical deep-planning read path, while coordination remains the start-here path and initiative or trace queries remain narrower projections.
- Explicit terminal-history browsing remains available through `--initiative-status completed|cancelled|superseded` or a known `--trace-id`.
- If no entries match the requested filters, the command exits successfully and reports that no planning-catalog entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query coordination` | Preferred machine start-here path before descending into one deep planning record. |
| `watchtower-core query authority` | Resolves when the planning catalog is canonical versus when a narrower planning or governance surface should answer instead. |
| `watchtower-core query initiatives` | Broader initiative-family lookup surface that stays compact instead of returning the full deep planning join. |
| `watchtower-core query trace` | Resolves the traceability join when you need the source trace-linked IDs without the full planning catalog sections. |
| `watchtower-core sync planning-catalog` | Rebuilds the planning catalog that this command reads. |
| `watchtower-core query acceptance` | Searches acceptance contracts directly when you need the contract family rather than the joined planning record. |
| `watchtower-core query evidence` | Searches validation evidence directly when you need the evidence family rather than the joined planning record. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/planning.py`
- `core/control_plane/indexes/planning/planning_catalog.v1.json`

## Updated At
- `2026-03-13T20:36:00Z`
