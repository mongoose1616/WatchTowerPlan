# `watchtower-core closeout`

## Summary
This command group applies terminal initiative state to traced planning surfaces and also
provides the governed purge path for eligible closed trace packages.

## Use When
- You want help for one of the closeout operations without opening the implementation code first.
- You need to mark one traced initiative as completed, superseded, cancelled, or abandoned.
- You need to mark one live initiative package under `plan/**` as completed, superseded, or cancelled.
- You want a governed closeout or purge path that updates both machine-readable and human-readable planning mirrors.

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
- `<closeout_command>`: Choose the closeout operation you want to run, currently `initiative`, `plan-initiative`, or `purge-trace`.
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

```sh
cd core/python
./.venv/bin/watchtower-core closeout plan-initiative --initiative-slug plan_terminal_initiative_closeout_runtime --initiative-status completed --closure-reason "Delivered the live closeout runtime" --write
```

```sh
cd core/python
uv run watchtower-core closeout purge-trace --trace-id trace.example --retained-authority-path docs/standards/governance/planning_retention_and_purge_standard.md
```

## Behavior and Outputs
- With no leaf command, the current implementation prints closeout-specific help and exits successfully.
- `initiative` validates acceptance reconciliation by default, applies terminal initiative state to the traceability index, and regenerates the mirrored initiative, coordination, and family tracking surfaces in write mode.
- `plan-initiative` closes one live initiative package under `plan/**`, finalizes initiative-local evidence and closeout artifacts, and refreshes the live plan coordination and rendered surfaces in write mode.
- `purge-trace` validates terminal-state, open-task, acceptance, duplicate-ledger, and surviving-reference preconditions before it removes one closed trace package and writes the minimal purge ledger entry.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core closeout initiative` | Applies terminal closeout state for one traced initiative. |
| `watchtower-core closeout plan-initiative` | Applies terminal closeout state for one live initiative package under `plan/**`. |
| `watchtower-core closeout purge-trace` | Purges one eligible closed trace package after retention checks pass. |
| `watchtower-core validate acceptance` | Performs the trace-level acceptance reconciliation that closeout now enforces by default. |
| `watchtower-core query initiatives` | Reads the initiative view that the closeout command also refreshes in write mode. |
| `watchtower-core query trace` | Reads the traceability entry that the closeout command updates. |
| `watchtower-core query coordination` | Reads the live pack-level coordination view that `plan-initiative` refreshes in write mode. |
| `watchtower-core sync initiative-index` | Rebuilds one of the initiative coordination surfaces the closeout command also updates in write mode. |
| `watchtower-core sync initiative-tracking` | Rebuilds the human-readable initiative tracker the closeout command also updates in write mode. |
| `watchtower-core sync prd-tracking` | Rebuilds one of the human trackers the closeout command also updates in write mode. |
| `watchtower-core sync decision-tracking` | Rebuilds one of the human trackers the closeout command also updates in write mode. |
| `watchtower-core sync design-tracking` | Rebuilds one of the human trackers the closeout command also updates in write mode. |

## Source Surface
- `core/python/src/watchtower_core/cli/closeout_family.py`
- `core/python/src/watchtower_core/closeout/`

## Updated At
- `2026-03-17T10:30:00Z`
