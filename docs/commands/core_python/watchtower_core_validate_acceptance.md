# `watchtower-core validate acceptance`

## Summary
This command validates one trace across PRD acceptance IDs, acceptance contracts, validation evidence, validator references, and traceability.

## Use When
- You need semantic acceptance reconciliation rather than only schema validation.
- You want to detect missing acceptance joins, unknown validator references, or uncovered acceptance IDs.
- You want a fast pass or fail signal before closeout or review.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate acceptance` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate acceptance --trace-id <trace_id> [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier such as `trace.core_python_foundation`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation --format json
```

## Behavior and Outputs
- The command resolves the trace, matching PRD, acceptance contract, validation evidence, validator references, and traceability entry.
- It checks for PRD-versus-contract drift, contract-versus-traceability drift, unknown validator references, missing traceability evidence joins, and uncovered acceptance IDs.
- In `human` mode, the command prints `PASS` or `FAIL`, the semantic validator ID, and any findings.
- In `json` mode, the command prints one JSON object with the pass or fail result and structured issues.
- The command exits with status code `0` when reconciliation passes and `1` when semantic drift is detected.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate artifact` | Validates the underlying JSON artifacts structurally before or after semantic reconciliation. |
| `watchtower-core query acceptance` | Shows the current acceptance contract inputs to the reconciliation step. |
| `watchtower-core query evidence` | Shows the durable evidence artifacts that the reconciliation step inspects. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/validation/acceptance.py`
- `core/control_plane/contracts/acceptance/`
- `core/control_plane/ledgers/validation_evidence/`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

## Updated At
- `2026-03-09T16:33:16Z`
