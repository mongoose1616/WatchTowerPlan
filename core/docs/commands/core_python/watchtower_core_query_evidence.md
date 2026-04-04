# `watchtower-core query evidence`

## Summary
This command searches the governed validation-evidence record family for one trace, acceptance ID, validator ID, or overall result.

## Use When
- You need to inspect durable validation proof for a traced initiative.
- You want to see whether a specific acceptance ID is covered by committed evidence.
- You want a structured lookup surface before semantic acceptance reconciliation or closeout.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query evidence` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/query_records_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query evidence [--trace-id <trace_id>] [--result <passed|failed|warning|not_applicable>] [--acceptance-id <acceptance_id>] [--validator-id <validator_id>] [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Exact trace filter such as `trace.governed_acceptance_example`.
- `--result <result>`: Exact overall-result filter such as `passed` or `failed`.
- `--acceptance-id <acceptance_id>`: Exact acceptance-ID filter such as `ac.governed_acceptance_example.001`.
- `--validator-id <validator_id>`: Exact validator-ID filter such as `validator.control_plane.traceability_index`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query evidence --trace-id trace.governed_acceptance_example
```

```sh
cd core/python
uv run watchtower-core query evidence --acceptance-id ac.governed_acceptance_example.001 --format json
```

## Behavior and Outputs
- The command reads governed validation-evidence records directly from `core/control_plane/records/validation_evidence/`.
- Portable customer exports can legitimately return no shared evidence records because retained validation evidence is excluded from staged handoff bundles.
- In `human` mode, the command prints matching evidence artifacts with their trace, recorded-at timestamp, and check count.
- In `json` mode, the command prints one JSON object with matching evidence artifacts and the acceptance IDs they cover.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query acceptance` | Lets you inspect the acceptance contract that the evidence should cover. |
| `watchtower-core validate acceptance` | Performs semantic reconciliation across initiative acceptance, contracts, evidence, and traceability. |

## Source Surface
- `core/python/src/watchtower_host/cli/query_records_family.py`
- `core/python/src/watchtower_host/cli/query_records_handlers.py`
- `core/python/src/watchtower_core/query/evidence.py`
- `core/control_plane/records/validation_evidence/`

## Updated At
- `2026-04-04T02:45:00Z`
