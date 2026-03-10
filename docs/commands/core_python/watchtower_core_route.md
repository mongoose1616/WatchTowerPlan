# `watchtower-core route`

## Summary
This command group previews the workflow-module route that the current authored routing surfaces would activate for a request or explicit task type.

## Use When
- You want a deterministic advisory route preview without manually reading `AGENTS.md` and `workflows/ROUTING_TABLE.md` line by line.
- You need machine-readable route lookup for higher-level workflows or agent calls.
- You want to confirm which workflow modules a routed task type currently activates.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core route` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/route_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core route <route_command> [args]
```

## Arguments and Options
- `<route_command>`: Choose `preview`.
- `-h`, `--help`: Show the command help text.
- No group-level route-selection flags exist; pass selection arguments to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core route --help
```

```sh
cd core/python
uv run watchtower-core route preview --request "review code and commit the change"
```

```sh
cd core/python
uv run watchtower-core route preview --task-type "Repository Review" --format json
```

## Behavior and Outputs
- With no leaf command, the current implementation prints route-specific help and exits successfully.
- The command group is read-only and does not mutate repository state.
- The current route family is advisory and deterministic: it reads governed route and workflow lookup data without overriding the authored routing surfaces.
- Use `preview` when you want either scored request-text matches or one explicit routed task type.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core route preview` | Returns the actual route preview for a request or task type. |
| `watchtower-core query workflows` | Searches the companion workflow index used to describe the selected workflow modules. |
| `watchtower-core sync route-index` | Rebuilds the route index that this command group reads. |
| `watchtower-core` | Root command that dispatches to this command group. |

## Source Surface
- `core/python/src/watchtower_core/cli/route_family.py`
- `core/python/src/watchtower_core/cli/route_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/routes.py`

## Updated At
- `2026-03-10T22:45:00Z`
