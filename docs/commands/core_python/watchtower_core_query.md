# `watchtower-core query`

## Summary
This command is the namespace entrypoint for governed index lookups in the core Python workspace.

## Use When
- You want to search the repository path index.
- You want to search the command index.
- You want to resolve one traced initiative without reading multiple planning artifacts directly.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query <subcommand>
```

## Arguments and Options
- `<subcommand>`: Dispatch to `paths`, `commands`, or `trace`.
- `-h`, `--help`: Show the command help text.
- No namespace-level options exist yet beyond help and subcommand selection.

## Examples
```sh
cd core/python
uv run watchtower-core query paths --query planning
```

```sh
cd core/python
uv run watchtower-core query trace --trace-id trace.core_python_foundation --format json
```

## Behavior and Outputs
- With a valid leaf subcommand, this command dispatches to the requested query handler.
- The leaf query commands support `human` and `json` output modes.
- With no leaf subcommand, the current implementation falls back to the root CLI help output.
- This command does not mutate repository state.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core` | Root command that dispatches to this namespace. |
| `watchtower-core query paths` | Searches repository path entries. |
| `watchtower-core query commands` | Searches command-index entries. |
| `watchtower-core query trace` | Resolves one traceability record. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/query/`

## Updated At
- `2026-03-09T05:43:10Z`
