# `watchtower-core closeout`

## Summary
This command group closes retained traced initiatives after live `plan/**` work has already
been promoted or purged.

## Use When
- You want help for one of the closeout operations without opening the implementation code first.
- You need to mark one retained traced initiative record as completed, superseded, cancelled, or abandoned.
- You want the retained closeout path that updates both machine-readable and human-readable historical mirrors.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core closeout` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/closeout_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core closeout <closeout_command> [args]
```

## Arguments and Options
- `<closeout_command>`: Choose the retained closeout operation you want to run, currently `initiative`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core closeout --help
```

```sh
cd core/python
uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status completed --closure-reason "Closed the retained trace record"
```

## Behavior and Outputs
- With no leaf command, the current implementation prints closeout-specific help and exits successfully.
- `initiative` validates acceptance reconciliation by default, applies terminal initiative state to the retained trace record, rejects live `plan/**` trace IDs, and regenerates the mirrored initiative, coordination, and traceability surfaces in write mode.
- Live initiative-package closeout now lives under `watchtower-core plan closeout initiative`.
- Trace purge now lives under `watchtower-core plan closeout purge-trace`.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core closeout initiative` | Applies terminal closeout state for one retained trace record after live `plan/**` work has already been promoted or purged. |
| `watchtower-core plan closeout` | Entry point for live initiative closeout and purge operations under the plan namespace. |
| `watchtower-core plan closeout initiative` | Applies terminal closeout state for one live initiative package under `plan/**`. |
| `watchtower-core plan closeout purge-trace` | Purges one eligible closed trace package after retention checks pass. |
| `watchtower-core validate acceptance` | Performs the trace-level acceptance reconciliation that closeout now enforces by default. |
| `watchtower-core query initiatives` | Reads the initiative view that the closeout command also refreshes in write mode. |
| `watchtower-core query trace` | Reads the traceability entry that the closeout command updates. |
| `watchtower-core query coordination` | Reads the live pack-level coordination view that plan closeout refreshes in write mode. |
| `watchtower-core sync initiative-index` | Rebuilds one of the initiative coordination surfaces that retained or plan closeout also updates in write mode. |
| `watchtower-core sync initiative-tracking` | Rebuilds the human-readable initiative tracker that retained or plan closeout also updates in write mode. |

## Source Surface
- `core/python/src/watchtower_core/cli/closeout_family.py`
- `core/python/src/watchtower_core/cli/closeout_handlers.py`

## Updated At
- `2026-03-18T23:58:00Z`
