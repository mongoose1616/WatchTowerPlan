# `watchtower-core git`

## Summary
This command group evaluates local branch and worktree hygiene against the repository's current git-workflow policy.

## Use When
- You want a read-first report on stale local branches or temporary worktrees.
- You need a conservative cleanup path instead of deleting branches or worktrees manually.
- You want one CLI surface that applies the current old-state evaluation rules from the git workflow standard.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core git` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/git_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core git <git_command> [args]
```

## Arguments and Options
- `<git_command>`: Choose `hygiene`.
- `-h`, `--help`: Show the git-command help text.
- No group-level flags exist; pass evaluation and apply options to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core git --help
```

```sh
cd core/python
uv run watchtower-core git hygiene --format json
```

```sh
cd core/python
uv run watchtower-core git hygiene --base-ref origin/main --apply --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- The group delegates branch and worktree evaluation to the reusable-core git hygiene runtime rather than shelling out ad hoc cleanup logic in docs or workflows.
- Cleanup is read-only unless the selected leaf command explicitly opts into `--apply`.
- Use the `hygiene` leaf when you need the repository-standard old-state evaluation plus conservative local cleanup behavior.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core git hygiene` | Evaluates local branches and worktrees and can apply conservative cleanup. |
| `watchtower-core route preview` | Shows which workflow route the repository would apply for a branch-hygiene request. |
| `watchtower-core` | Root command that dispatches to this command group. |

## Source Surface
- `core/python/src/watchtower_host/cli/git_family.py`
- `core/python/src/watchtower_host/cli/git_handlers.py`
- `core/python/src/watchtower_core/utils/git_hygiene.py`

## Updated At
- `2026-04-04T22:50:00Z`
