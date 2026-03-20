# `watchtower-core plan closeout`

## Summary
This command group closes live initiative packages under `plan/**` and purges eligible closed trace packages after the plan-owned retention guards pass.

## Use When
- You want help for one of the live plan closeout operations without opening the implementation code first.
- You need to mark one live initiative package under `plan/**` as completed, superseded, or cancelled.
- You need to purge one eligible closed trace package through the governed plan-owned purge path.

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
- `<closeout_command>`: Choose `initiative` or `purge-trace`.
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
uv run watchtower-core plan closeout purge-trace --trace-id trace.example --retained-authority-path plan/docs/standards/governance/planning_retention_and_purge_standard.md
```

## Behavior and Outputs
- With no leaf command, the current implementation prints plan-closeout-specific help and exits successfully.
- `initiative` closes one live initiative package under `plan/**`, finalizes initiative-local evidence and closeout artifacts, and refreshes the live plan coordination and rendered surfaces in write mode.
- `purge-trace` validates terminal-state, open-task, acceptance, duplicate-ledger, and surviving-reference preconditions before it removes one closed trace package and writes the minimal purge ledger entry.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan closeout initiative` | Applies terminal closeout state for one live initiative package under `plan/**`. |
| `watchtower-core plan closeout purge-trace` | Purges one eligible closed trace package after retention checks pass. |
| `watchtower-core closeout initiative` | Applies terminal closeout state for one retained trace record after live `plan/**` work has already been promoted or purged. |
| `watchtower-core validate acceptance` | Performs the trace-level acceptance reconciliation that purge enforces by default. |
| `watchtower-core plan query coordination` | Reads the live pack-level coordination view that plan closeout refreshes in write mode. |
| `watchtower-core plan query trace` | Reads the retained traceability entry updated before or after purge. |
| `watchtower-core sync all` | Rebuilds the broader derived surface set that plan closeout also updates in write mode. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/closeout.py`
- `plan/python/src/watchtower_plan/closeout/`
- `plan/python/src/watchtower_plan/initiative_packages.py`

## Updated At
- `2026-03-20T17:10:00Z`
