# `watchtower-core`

## Summary
This command is the root CLI entrypoint for the core Python workspace and dispatches to the available `watchtower-core` subcommands.

## Use When
- You want to discover the current core helper and harness commands.
- You need a stable CLI entrypoint for workspace checks or future core operations.
- You want the built-in help output for the current command surface.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core` |
| Kind | `root_command` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core <command>
```

## Arguments and Options
- `<command>`: Dispatch to an available subcommand such as `doctor`.
- `-h`, `--help`: Show the command help text.
- No root-command-specific options exist yet beyond help and subcommand selection.

## Examples
```sh
cd core/python
uv run watchtower-core --help
```

```sh
cd core/python
uv run watchtower-core doctor
```

## Behavior and Outputs
- With no subcommand, the current implementation prints the CLI help text and exits successfully.
- With a valid subcommand, the root command dispatches to that subcommand handler.
- Unknown subcommands are rejected by the underlying CLI parser.
- The current command surface is intentionally small and acts as the operator entrypoint for the growing core workspace.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core doctor` | Lightweight workspace smoke check exposed through the root CLI. |
| `docs/commands/core_python/README.md` | Local command-family inventory for the core Python workspace. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/README.md`

## Last Synced
- `2026-03-09`
