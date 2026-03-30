# `watchtower-core benchmark`

## Summary
This command group runs governed reusable-core performance benchmarks. Use it when you need deliberate retained benchmark evidence rather than default-on runtime telemetry.

## Use When
- You need to run one governed benchmark suite through fresh subprocesses.
- You want retained benchmark evidence with telemetry-on versus telemetry-off comparison.
- You need a fail-closed benchmark path before writing a retained benchmark record.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core benchmark` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/benchmark_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core benchmark <benchmark_command> [args]
```

## Arguments and Options
- `<benchmark_command>`: Choose a leaf command such as `run`.
- `-h`, `--help`: Show the benchmark-group help text.
- Pass suite selection, output, and retained-record flags to the selected benchmark command.

## Examples
```sh
cd core/python
uv run watchtower-core benchmark --help
```

```sh
cd core/python
uv run watchtower-core benchmark run --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- Benchmark commands are deliberate and fail closed rather than default-on and fail-open.
- Use this command group for repeatable retained benchmark evidence, not for routine operational observation.
- Runtime telemetry remains active as the operational observation baseline outside this command group.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core benchmark run` | Runs one governed benchmark suite and optionally writes retained benchmark evidence. |
| `watchtower-core query benchmarks` | Reads retained benchmark evidence without opening raw JSON directly. |
| `watchtower-core query authority` | Resolves the canonical benchmarking standard and retained benchmark surfaces. |
| `watchtower-core` | Root command that dispatches to this group. |

## Source Surface
- `core/python/src/watchtower_host/cli/benchmark_family.py`
- `core/python/src/watchtower_host/cli/benchmark_handlers.py`

## Updated At
- `2026-03-29T12:30:00Z`
