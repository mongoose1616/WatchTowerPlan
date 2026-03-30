# `watchtower-core benchmark run`

## Summary
This command runs one governed benchmark suite through fresh serialized subprocesses, validates the generated benchmark record, and can write both an explicit output file and the canonical retained benchmark record.

## Use When
- You need a repeatable shared-core performance baseline.
- You want telemetry-on versus telemetry-off timing plus top nested operations from telemetry JSONL.
- You need to compare a current run against a prior retained benchmark record.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core benchmark run` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/benchmark_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core benchmark run [--suite-id <suite_id>] [--runs <count>] [--warmup-runs <count>] [--baseline-record <path>] [--output <path>] [--write-record] [--record-id <record_id>] [--format <human|json>]
```

## Arguments and Options
- `--suite-id <suite_id>`: Benchmark suite identifier declared in the benchmark-suite registry. Defaults to `suite.benchmark.core_cli_representative_v1`.
- `--runs <count>`: Optional measured-run override applied to each suite command.
- `--warmup-runs <count>`: Optional warmup-run override applied to each suite command.
- `--baseline-record <path>`: Optional prior benchmark record used for current-versus-baseline comparison.
- `--output <path>`: Optional explicit file path for the generated benchmark record JSON.
- `--write-record`: Write the generated benchmark record to the canonical retained benchmark-record family.
- `--record-id <record_id>`: Optional explicit benchmark record identifier.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core benchmark run --format json
```

```sh
cd core/python
uv run watchtower-core benchmark run --output /tmp/core_cli_benchmark.json --format json
```

```sh
cd core/python
uv run watchtower-core benchmark run --write-record --record-id benchmark.core_cli_representative_v1.20260329_baseline --format json
```

## Behavior and Outputs
- The command loads the requested suite from `core/control_plane/registries/benchmark_suite_registry.json`.
- Each suite command runs in a fresh serialized subprocess from the suite's declared working directory.
- Telemetry-on runs require exactly one telemetry JSONL file per measured subprocess; missing telemetry fails the benchmark run.
- Warmup runs are excluded from the retained measured timing samples.
- The command validates the generated benchmark record against the benchmark-record schema before writing output.
- If `--baseline-record` is provided, the command requires matching suite ID and command IDs before computing comparison deltas.
- The retained environment context records a portable Python executable label rather than a machine-local absolute interpreter path.
- In `human` mode, the command prints the suite summary and per-command median timings.
- In `json` mode, the command prints one JSON object containing the full generated benchmark record plus any output paths.
- The command exits with status code `0` when the benchmark run succeeds and `1` when suite loading, subprocess execution, telemetry capture, comparison compatibility, or schema validation fails.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core benchmark` | Parent command group for governed benchmark commands. |
| `watchtower-core query benchmarks` | Reads retained benchmark evidence after the run is committed. |
| `watchtower-core validate artifact` | Validates retained benchmark records by path through the benchmark-record validator. |

## Source Surface
- `core/python/src/watchtower_host/cli/benchmark_handlers.py`
- `core/python/src/watchtower_core/benchmarking/runner.py`
- `core/control_plane/registries/benchmark_suite_registry.json`
- `core/control_plane/records/benchmarks/`

## Updated At
- `2026-03-30T18:30:00Z`
