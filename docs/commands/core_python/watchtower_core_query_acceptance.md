# `watchtower-core query acceptance`

## Summary
This command searches the governed acceptance-contract artifacts for a trace, PRD, or acceptance ID.

## Use When
- You need the machine-readable acceptance boundary for a traced initiative.
- You want to confirm which acceptance IDs are published in the current acceptance contract.
- You want a structured lookup surface before running semantic acceptance validation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query acceptance` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query acceptance [--trace-id <trace_id>] [--source-prd-id <prd_id>] [--acceptance-id <acceptance_id>] [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Exact trace filter such as `trace.core_python_foundation`.
- `--source-prd-id <prd_id>`: Exact source PRD filter such as `prd.core_python_foundation`.
- `--acceptance-id <acceptance_id>`: Exact acceptance-ID filter such as `ac.core_python_foundation.002`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query acceptance --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core query acceptance --acceptance-id ac.core_python_foundation.002 --format json
```

## Behavior and Outputs
- The command reads governed acceptance contracts directly from `core/control_plane/contracts/acceptance/`.
- In `human` mode, the command prints matching contracts with their trace, source PRD, and published acceptance IDs.
- In `json` mode, the command prints one JSON object with the matching contracts and their required validator IDs.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query evidence` | Lets you inspect durable evidence that should cover the same acceptance IDs. |
| `watchtower-core validate acceptance` | Performs semantic reconciliation across the same trace surfaces. |
| `watchtower-core query trace` | Shows the joined traceability record that should mirror the same acceptance contract IDs. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/acceptance.py`
- `core/control_plane/contracts/acceptance/`

## Updated At
- `2026-03-09T16:33:16Z`
