# `watchtower-core plan`

## Summary
This command group bootstraps live initiative packages and advances initiative readiness through confirmation and approval while refreshing derived plan surfaces in write mode.

## Use When
- You want to bootstrap one live initiative package under `plan/**`.
- You need to confirm reviewed initiative inputs or approve one live initiative package before execution can start.

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
- `<plan_command>`: Choose `bootstrap`, `confirm-inputs`, or `approve`.
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

## Behavior and Outputs
- With no leaf command, the current implementation prints plan-specific help and exits successfully.
- `bootstrap` creates one live initiative package, its initiative-local machine state, and a bootstrap task, with optional `decision_notes.md`, and leaves the package in pre-execution review until approval.
- `confirm-inputs` records maintainer confirmation of the current initiative-authored inputs before execution approval.
- `approve` moves one validated live initiative package into `ready_for_execution`, which is required before task mutations may start real execution.
- In write mode, the command refreshes the deterministic derived planning surfaces after the selected plan operation writes its canonical outputs.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan bootstrap` | Bootstraps one live initiative package plus one bootstrap task. |
| `watchtower-core plan confirm-inputs` | Records reviewed initiative-authored inputs into machine state before approval. |
| `watchtower-core plan approve` | Approves one live initiative package into `ready_for_execution`. |
| `watchtower-core task` | Manages the bootstrap task or follow-up work after the planning chain exists. |
| `watchtower-core sync all` | Rebuilds the same deterministic planning surfaces refreshed in write mode. |
| `watchtower-core query initiatives` | Reads the live initiative-family surface affected by plan writes. |
| `watchtower-core query readiness` | Reads the readiness-gate surface affected by plan writes. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/namespace.py`
- `plan/python/src/watchtower_plan/cli/handlers.py`
- `plan/python/src/watchtower_plan/initiative_packages.py`

## Updated At
- `2026-03-18T20:35:00Z`
