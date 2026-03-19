# `watchtower-core doctor`

## Summary
This command runs the current workspace health snapshot for the core Python package and confirms that the local CLI entrypoint plus the main governed lookup surfaces load successfully.

## Use When
- You want a quick sanity check that the core Python CLI is wired correctly.
- You are onboarding to the workspace and want to confirm the installed command plus the core governed surfaces load.
- You need the simplest successful command invocation for the current `watchtower-core` CLI.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core doctor` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/doctor_family.py` |

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
- In `human` mode, the command prints a workspace-health summary including the repo root, loaded governed-surface counts, and the recommended validation baseline.
- In `json` mode, the command prints a single JSON object describing the command, workspace, repo root, result status, governed-surface counts, and the recommended validation baseline, then exits with status code `0`.
- The command does not mutate repository state.
- The command remains lightweight, but it is now a real health snapshot rather than only a scaffold placeholder.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core` | Root command that dispatches to this subcommand. |
| `core/python/README.md` | Workspace onboarding guide that uses this command as the final baseline health-check step. |

## Source Surface
- `core/python/src/watchtower_core/cli/doctor_family.py`
- `core/python/README.md`

## Updated At
- `2026-03-14T05:37:06Z`
