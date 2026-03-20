# `watchtower-core plan`

## Summary
This command group owns the plan-pack runtime surface: bootstrap, live query, task lifecycle, closeout, and readiness transitions for `plan/**`.

## Use When
- You want to bootstrap one live initiative package under `plan/**`.
- You need to confirm reviewed initiative inputs or approve one live initiative package before execution can start.
- You need the plan-owned command namespace for live query, task, or closeout operations.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/namespace.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan <plan_command> [args]
```

## Arguments and Options
- `<plan_command>`: Choose `bootstrap`, `confirm-inputs`, `approve`, `query`, `sync`, `task`, or `closeout`.
- `-h`, `--help`: Show the command help text.
- Plan operations are dry-run by default. Pass `--write` to the selected leaf command to persist the generated state and refresh derived planning surfaces.

## Examples
```sh
cd core/python
uv run watchtower-core plan --help
```

```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id trace.example --title "Example Initiative" --summary "Bootstraps the example initiative." --include-decision --write
```

```sh
cd core/python
uv run watchtower-core plan approve --initiative-slug example_initiative --write
```

```sh
cd core/python
uv run watchtower-core plan query coordination --format json
```

## Behavior and Outputs
- With no leaf command, the current implementation prints plan-specific help and exits successfully.
- `bootstrap` creates one live initiative package, its initiative-local machine state, and a bootstrap task, with optional `decision_notes.md`, and leaves the package in pre-execution review until approval.
- `confirm-inputs` records maintainer confirmation of the current initiative-authored inputs before execution approval.
- `approve` moves one validated live initiative package into `ready_for_execution`, which is required before task mutations may start real execution.
- `query` provides read-only lookup over live plan state, plan-owned indexes, and retained planning records.
- `sync` rebuilds the plan-owned derived indexes, trackers, and orchestration slices under the pack namespace.
- `task` owns initiative-local live task creation, update, and transition flows.
- `closeout` owns live initiative terminal closeout and eligible purge flows under the plan namespace.
- In write mode, the command refreshes the deterministic derived planning surfaces after the selected plan operation writes its canonical outputs.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan bootstrap` | Bootstraps one live initiative package plus one bootstrap task. |
| `watchtower-core plan confirm-inputs` | Records reviewed initiative-authored inputs into machine state before approval. |
| `watchtower-core plan approve` | Approves one live initiative package into `ready_for_execution`. |
| `watchtower-core plan query` | Reads live plan state, plan-owned indexes, and retained planning records. |
| `watchtower-core plan task` | Manages the bootstrap task or follow-up work after the planning chain exists. |
| `watchtower-core plan sync` | Rebuilds the plan-owned derived indexes and trackers refreshed by plan write operations. |
| `watchtower-core plan closeout` | Applies live initiative closeout and eligible purge flows under the pack-owned namespace. |
| `watchtower-core plan sync all` | Rebuilds the same deterministic planning surfaces refreshed in write mode. |
| `watchtower-core plan query initiatives` | Reads the live initiative-family surface affected by plan writes. |
| `watchtower-core plan query readiness` | Reads the readiness-gate surface affected by plan writes. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/namespace.py`
- `plan/python/src/watchtower_plan/cli/handlers.py`
- `plan/python/src/watchtower_plan/cli/query.py`
- `plan/python/src/watchtower_plan/cli/sync.py`
- `plan/python/src/watchtower_plan/cli/tasks.py`
- `plan/python/src/watchtower_plan/cli/closeout.py`
- `plan/python/src/watchtower_plan/initiative_packages.py`

## Updated At
- `2026-03-20T21:20:00Z`
