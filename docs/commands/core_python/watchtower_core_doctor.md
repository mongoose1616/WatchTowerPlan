# `watchtower-core doctor`

## Summary
This command runs the current lightweight workspace smoke check for the core Python package and confirms that the scaffolded CLI surface is available.

## Use When
- You want a quick sanity check that the core Python CLI is wired correctly.
- You are onboarding to the workspace and want to confirm the installed command runs.
- You need the simplest successful command invocation for the current `watchtower-core` CLI.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core doctor` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core doctor
```

## Arguments and Options
- `-h`, `--help`: Show the command help text.
- No command-specific arguments or options exist yet beyond help.

## Examples
```sh
cd core/python
uv run watchtower-core doctor
```

## Behavior and Outputs
- The current implementation prints `watchtower_core workspace scaffold is available.` and exits with status code `0`.
- The command does not mutate repository state.
- The command currently acts as a minimal operator-visible smoke check and placeholder for future workspace health checks.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core` | Root command that dispatches to this subcommand. |
| `core/python/README.md` | Workspace onboarding guide that uses this command as the final smoke-check step. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/README.md`

## Last Synced
- `2026-03-09`
