# `watchtower-core plan closeout`

## Summary
This command group closes live initiative packages under `plan/**` and closes retained trace records after live work is already promoted or otherwise retired.

## Use When
- You want help for one of the live plan closeout operations without opening the implementation code first.
- You need to mark one live initiative package under `plan/**` as completed, superseded, or cancelled.
- You need to mark one retained trace record as terminal after the live initiative package is already closed or otherwise retired.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan closeout` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/closeout.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan closeout <closeout_command> [args]
```

## Arguments and Options
- `<closeout_command>`: Choose `initiative` or `retained-initiative`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan closeout --help
```

```sh
cd core/python
uv run watchtower-core plan closeout initiative --initiative-slug plan_terminal_initiative_closeout_runtime --initiative-status completed --closure-reason "Delivered the live closeout runtime" --write
```

```sh
cd core/python
uv run watchtower-core plan closeout retained-initiative --trace-id trace.example --initiative-status completed --closure-reason "Closed the retained trace record" --write
```

## Behavior and Outputs
- With no leaf command, the current implementation prints plan-closeout-specific help and exits successfully.
- `initiative` closes one live initiative package under `plan/**`, finalizes initiative-local evidence and closeout artifacts, and refreshes the live plan coordination and rendered surfaces in write mode.
- `retained-initiative` closes one retained trace record after live `plan/**` work is already promoted or otherwise retired, then refreshes the traceability, initiative, and coordination mirrors that still expose retained history.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan closeout initiative` | Applies terminal closeout state for one live initiative package under `plan/**`. |
| `watchtower-core plan closeout retained-initiative` | Applies terminal closeout state for one retained trace record after live `plan/**` work is already promoted or otherwise retired. |
| `watchtower-core validate acceptance` | Performs the trace-level acceptance reconciliation that retained closeout may still enforce. |
| `watchtower-core plan query coordination` | Reads the live pack-level coordination view that plan closeout refreshes in write mode. |
| `watchtower-core plan query trace` | Reads the retained traceability entry updated by retained closeout. |
| `watchtower-core plan sync all` | Rebuilds the broader derived surface set that plan closeout also updates in write mode. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/closeout.py`
- `plan/python/src/watchtower_plan/closeout/`
- `plan/python/src/watchtower_plan/initiatives/service.py`

## Updated At
- `2026-03-24T23:45:00Z`
