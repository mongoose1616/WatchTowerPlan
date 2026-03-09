# `watchtower-core sync`

## Summary
This command group rebuilds derived governed artifacts from authored repository sources.

## Use When
- You need help for one of the sync operations without opening the implementation code first.
- You want to rebuild a derived artifact after changing the authored source surfaces it depends on.
- You want to confirm whether a sync command defaults to dry-run or writes to disk.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync <sync_command> [args]
```

## Arguments and Options
- `<sync_command>`: Choose the derived artifact you want to rebuild, currently `command-index` or `repository-paths`.
- `-h`, `--help`: Show the command help text.
- No group-level write flags exist; pass mutation or output flags to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core sync --help
```

```sh
cd core/python
uv run watchtower-core sync command-index
```

```sh
cd core/python
uv run watchtower-core sync command-index --write
```

```sh
cd core/python
uv run watchtower-core sync repository-paths
```

```sh
cd core/python
uv run watchtower-core sync repository-paths --write
```

## Behavior and Outputs
- With no leaf command, the current implementation prints sync-specific help and exits successfully.
- The command group explains the available sync surfaces without requiring engineers to inspect the implementation directly.
- The current leaf commands are `command-index` for command-doc lookup rebuilds and `repository-paths` for README inventory rebuilds.
- Individual leaf commands may be dry-run by default and should document their mutation flags explicitly.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync command-index` | Rebuilds the command index from authored command docs. |
| `watchtower-core sync repository-paths` | Rebuilds the repository path index from README inventories. |
| `watchtower-core query commands` | Reads the command index that one of the current sync commands rebuilds. |
| `watchtower-core query paths` | Reads the repository path index that the current sync command rebuilds. |
| `watchtower-core` | Root command that dispatches to this command group. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/sync/`

## Updated At
- `2026-03-09T06:42:17Z`
