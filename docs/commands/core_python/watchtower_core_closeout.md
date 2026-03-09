# `watchtower-core closeout`

## Summary
This command group applies initiative-level closeout state to traced planning surfaces.

## Use When
- You want help for one of the closeout operations without opening the implementation code first.
- You need to mark one traced initiative as completed, superseded, cancelled, or abandoned.
- You want a governed closeout path that updates both machine-readable and human-readable planning mirrors.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core closeout` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core closeout <closeout_command> [args]
```

## Arguments and Options
- `<closeout_command>`: Choose the closeout operation you want to run, currently `initiative`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core closeout --help
```

```sh
cd core/python
uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status completed --closure-reason "Delivered and validated"
```

## Behavior and Outputs
- With no leaf command, the current implementation prints closeout-specific help and exits successfully.
- The current leaf command is `initiative`, which applies terminal initiative state to the traceability index and regenerates the mirrored planning trackers in write mode.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core closeout initiative` | Applies terminal closeout state for one traced initiative. |
| `watchtower-core query trace` | Reads the traceability entry that the closeout command updates. |
| `watchtower-core sync prd-tracking` | Rebuilds one of the human trackers the closeout command also updates in write mode. |
| `watchtower-core sync decision-tracking` | Rebuilds one of the human trackers the closeout command also updates in write mode. |
| `watchtower-core sync design-tracking` | Rebuilds one of the human trackers the closeout command also updates in write mode. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/closeout/`

## Updated At
- `2026-03-09T16:20:00Z`
