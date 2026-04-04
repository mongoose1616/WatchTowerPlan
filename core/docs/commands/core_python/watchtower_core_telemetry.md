# `watchtower-core telemetry`

## Summary
This command group manages local runtime telemetry machine state. Use it when you need a dry-run-first cleanup path for retained telemetry files rather than manual filesystem deletion.

## Use When
- Runtime telemetry files have accumulated under one pack machine root and you need a governed cleanup path.
- You want to preview which telemetry runs would be removed before deleting anything.
- You need to target the active pack telemetry root, another pack via `--pack-settings-path`, or one explicit telemetry root override.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core telemetry` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/telemetry_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core telemetry <telemetry_command> [args]
```

## Arguments and Options
- `<telemetry_command>`: Choose a leaf command such as `delete`.
- `-h`, `--help`: Show the telemetry-group help text.
- Pass selection, targeting, and `--write` flags to the selected telemetry command.

## Examples
```sh
cd core/python
uv run watchtower-core telemetry --help
```

```sh
cd core/python
uv run watchtower-core telemetry delete --older-than-days 7 --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- Telemetry cleanup defaults to dry-run output; use `--write` to apply deletion.
- Cleanup is constrained to one resolved telemetry root and prunes only matched JSONL files plus empty dated directories beneath that root.
- The active invocation's own telemetry file is excluded from deletion automatically.
- Use this command group for telemetry machine-state hygiene, not for deliberate retained benchmark evidence or governed artifact deletion.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core telemetry delete` | Deletes or previews retained runtime telemetry files under one telemetry root. |
| `watchtower-core benchmark` | Deliberate retained performance measurement rather than operational telemetry cleanup. |
| `watchtower-core` | Root command that dispatches to this group. |

## Source Surface
- `core/python/src/watchtower_host/cli/telemetry_family.py`
- `core/python/src/watchtower_host/cli/telemetry_handlers.py`
- `core/python/src/watchtower_core/telemetry/cleanup.py`

## Updated At
- `2026-03-31T07:15:00Z`
