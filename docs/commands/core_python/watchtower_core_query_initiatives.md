# `watchtower-core query initiatives`

## Summary
This command searches the governed initiative index for broader initiative-family lookup, including filtered history and non-default initiative-status views.

## Use When
- You want active initiative-family lookup beyond the default coordination start-here path.
- You need to filter initiatives by phase, owner, status, or blockers.
- You want machine-readable initiative-family data for a workflow, script, or agent and need more than the default `coordination` view.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query initiatives` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_coordination_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query initiatives [--query <text>] [--trace-id <trace_id>] [--initiative-status <status>] [--current-phase <phase>] [--owner <owner>] [--blocked-only] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over indexed initiative fields such as trace ID, title, summary, owner, next action, and linked artifact IDs.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--initiative-status <status>`: Exact initiative-status filter such as `active`, `completed`, or `superseded`. When omitted for filterless browse, the command defaults to `active`.
- `--current-phase <phase>`: Exact current-phase filter such as `prd`, `execution`, `validation`, or `closed`.
- `--owner <owner>`: Exact active-owner filter such as `repository_maintainer`.
- `--blocked-only`: Return only initiatives with one or more currently blocked active tasks.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Notes
- Use `watchtower-core query coordination` when you want the machine start-here path for current planning state.
- Use `watchtower-core query planning` when you need the canonical deep planning record for one trace rather than a compact initiative projection.
- Use `watchtower-core query authority` when you need to confirm that initiative lookup is the right surface for the question you are asking.
- Filterless browse now defaults to active initiatives; this command remains the broader initiative query surface for explicit historical or status-specific lookup.

## Examples
```sh
cd core/python
uv run watchtower-core query initiatives --current-phase execution
```

```sh
cd core/python
uv run watchtower-core query initiatives --blocked-only --format json
```

```sh
cd core/python
uv run watchtower-core query initiatives --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query initiatives --initiative-status completed --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching trace IDs, current phases, initiative statuses, active owners, open-task counts, and next-step guidance.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and result records, including `artifact_status`, `initiative_status`, and compact active-task summaries when present.
- With no explicit `--trace-id`, `--query`, `--current-phase`, `--owner`, `--blocked-only`, or `--initiative-status`, the command defaults to `initiative_status=active` so filterless browse stays aligned with the planning start-here model.
- When that active-default path is applied, the JSON payload includes `default_initiative_status: "active"` to keep the injected browse filter explicit for machine consumers.
- Use `--initiative-status completed|cancelled|superseded` for terminal-history browse instead of relying on filterless output.
- If no entries match the requested filters, the command exits successfully and reports that no initiative entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query` | Parent command group for all index-backed lookup commands. |
| `watchtower-core query coordination` | Preferred machine start-here path for current planning state. |
| `watchtower-core query authority` | Resolves when initiative lookup is canonical versus when coordination, traceability, or planning should answer instead. |
| `watchtower-core query planning` | Canonical deep-planning read path when the initiative summary is too compact. |
| `watchtower-core sync initiative-index` | Rebuilds the initiative index that this command reads. |
| `watchtower-core sync initiative-tracking` | Rebuilds the human-readable tracker derived from the same initiative view. |
| `watchtower-core query trace` | Resolves the underlying traceability record for one known trace ID. |
| `watchtower-core query tasks` | Inspects the active or blocked tasks that contribute to initiative phase and ownership. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_projection_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/initiatives.py`
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`

## Updated At
- `2026-03-13T23:21:33Z`
