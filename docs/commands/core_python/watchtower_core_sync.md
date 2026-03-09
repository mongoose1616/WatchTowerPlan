# `watchtower-core sync`

## Summary
This command is the namespace entrypoint for rebuilding or materializing derived governed artifacts.

## Use When
- You want to refresh a derived control-plane artifact deterministically from repository source surfaces.
- You want to inspect the current sync-capable artifact family before running a write.
- You need a stable namespace for future sync operations in the core Python workspace.

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
uv run watchtower-core sync <subcommand>
```

## Arguments and Options
- `<subcommand>`: Dispatch to `repository-paths`.
- `-h`, `--help`: Show the command help text.
- No namespace-level options exist yet beyond help and subcommand selection.

## Examples
```sh
cd core/python
uv run watchtower-core sync repository-paths
```

```sh
cd core/python
uv run watchtower-core sync repository-paths --format json
```

## Behavior and Outputs
- With a valid leaf subcommand, this command dispatches to the requested sync handler.
- The current leaf sync command supports `human` and `json` output modes.
- With no leaf subcommand, the current implementation falls back to the root CLI help output.
- Sync commands may write artifacts when explicitly asked; review the leaf command docs before using `--write`.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core` | Root command that dispatches to this namespace. |
| `watchtower-core sync repository-paths` | Rebuilds the repository path index from README inventories. |
| `watchtower-core query paths` | Reads the repository path index that this namespace can rebuild. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/sync/`

## Updated At
- `2026-03-09T05:43:10Z`
