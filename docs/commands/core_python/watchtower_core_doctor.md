# `watchtower-core doctor`

## Summary
This command runs the current lightweight workspace smoke check for the core Python package and confirms that the local CLI entrypoint is available.

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
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls. Defaults to `human`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core doctor
```

```sh
cd core/python
uv run watchtower-core doctor --format json
```

## Behavior and Outputs
- In `human` mode, the command prints `watchtower_core workspace scaffold is available.` and exits with status code `0`.
- In `json` mode, the command prints a single JSON object describing the command, workspace, result status, and message, then exits with status code `0`.
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

## Updated At
- `2026-03-10T02:30:31Z`
