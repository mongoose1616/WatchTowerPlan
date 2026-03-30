# `watchtower-core query benchmarks`

## Summary
This command searches the retained benchmark-record family for one record ID or suite ID so you can inspect durable performance evidence without opening raw JSON directly.

## Use When
- You need the latest retained benchmark baseline for one suite.
- You want to confirm whether a benchmark record was written to the canonical retained record family.
- You need a structured lookup surface before comparing new benchmark output against a prior retained record.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query benchmarks` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/query_records_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query benchmarks [--record-id <record_id>] [--suite-id <suite_id>] [--limit <count>] [--format <human|json>]
```

## Arguments and Options
- `--record-id <record_id>`: Exact benchmark record ID filter.
- `--suite-id <suite_id>`: Exact benchmark suite ID filter.
- `--limit <count>`: Maximum number of benchmark records to return.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query benchmarks
```

```sh
cd core/python
uv run watchtower-core query benchmarks --suite-id suite.benchmark.core_cli_representative_v1 --format json
```

## Behavior and Outputs
- The command reads retained benchmark records directly from `core/control_plane/records/benchmarks/`.
- Portable customer exports can legitimately return no benchmark records because retained benchmark history is excluded from staged handoff bundles.
- In `human` mode, the command prints matching benchmark record IDs with suite, recorded-at time, and command count.
- In `json` mode, the command prints one JSON object with matching benchmark records and their key metadata.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core benchmark run` | Generates the retained benchmark record that this command later reads. |
| `watchtower-core query authority` | Resolves the canonical benchmarking standard and retained benchmark surfaces. |
| `watchtower-core validate artifact` | Validates one retained benchmark record by path. |

## Source Surface
- `core/python/src/watchtower_host/cli/query_records_family.py`
- `core/python/src/watchtower_host/cli/query_records_handlers.py`
- `core/python/src/watchtower_core/query/benchmarks.py`
- `core/control_plane/records/benchmarks/`

## Updated At
- `2026-03-29T12:30:00Z`
