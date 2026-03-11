# `watchtower-core closeout initiative`

## Summary
This command records terminal closeout state for one traced initiative and, in write mode, refreshes the initiative, planning-catalog, and coordination views plus the mirrored family trackers that reflect that state.

## Use When
- A traced initiative is complete, superseded, cancelled, or abandoned.
- You need the traceability index, initiative view, planning-catalog, coordination surfaces, and family trackers to agree on the current initiative outcome.
- You want to dry-run the closeout record before mutating canonical planning surfaces.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core closeout initiative` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core closeout initiative --trace-id <trace_id> --initiative-status <completed|superseded|cancelled|abandoned> --closure-reason <reason> [--superseded-by-trace-id <trace_id>] [--closed-at <timestamp>] [--allow-open-tasks] [--write] [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier such as `trace.core_python_foundation`.
- `--initiative-status <status>`: Terminal initiative status to record.
- `--closure-reason <reason>`: Short human-readable reason for the closeout decision.
- `--superseded-by-trace-id <trace_id>`: Replacement trace identifier. Required when initiative status is `superseded`.
- `--closed-at <timestamp>`: Explicit RFC 3339 UTC closeout timestamp. Defaults to the current UTC time.
- `--allow-open-tasks`: Allow terminal closeout even if linked tasks are still open.
- `--write`: Persist the updated closeout state and regenerated trackers to their canonical paths.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status completed --closure-reason "Delivered and validated"
```

```sh
cd core/python
uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status superseded --superseded-by-trace-id trace.replacement --closure-reason "Replaced by the new initiative" --write
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate canonical planning surfaces.
- In write mode, the command updates the traceability index first, advances effective `updated_at` to the closeout timestamp, and then regenerates the initiative index, planning catalog, coordination index, initiative tracker, coordination tracker, and PRD, decision, and design trackers that mirror initiative status.
- The command blocks closeout by default when linked tasks are still open, unless `--allow-open-tasks` is used explicitly.
- In `human` mode, the command prints the chosen initiative status, timestamp, and write outcome.
- In `json` mode, the command prints one JSON object with the trace ID, closeout metadata, open-task exception list, and output paths for the traceability, initiative, planning-catalog, coordination, and family tracking surfaces when it wrote them.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core closeout` | Parent command group for closeout operations. |
| `watchtower-core query planning` | Reads the planning-catalog view this command now refreshes in write mode. |
| `watchtower-core query initiatives` | Reads the initiative view this command refreshes in write mode. |
| `watchtower-core query coordination` | Reads the coordination view this command refreshes in write mode. |
| `watchtower-core query trace` | Reads the traceability entry this command updates. |
| `watchtower-core sync initiative-index` | Rebuilds the machine-readable initiative index that this command also refreshes in write mode. |
| `watchtower-core sync planning-catalog` | Rebuilds the planning catalog that this command now refreshes in write mode. |
| `watchtower-core sync coordination` | Rebuilds the coordination slice this command now refreshes in write mode. |
| `watchtower-core sync initiative-tracking` | Rebuilds the human-readable initiative tracker that this command also refreshes in write mode. |
| `watchtower-core sync prd-tracking` | Rebuilds one tracker that this command updates in write mode. |
| `watchtower-core sync decision-tracking` | Rebuilds one tracker that this command updates in write mode. |
| `watchtower-core sync design-tracking` | Rebuilds one tracker that this command updates in write mode. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/closeout/initiative.py`

## Updated At
- `2026-03-11T16:10:47Z`
