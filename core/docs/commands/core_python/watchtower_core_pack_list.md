# `watchtower-core pack list`

## Summary
This command lists the hosted packs declared in the shared pack registry.

## Use When
- You need to see the hosted packs available in the current repository.
- You want the declared pack slug, namespace, distribution, or settings paths for automation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack list` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack list [--format <human|json>]
```

## Arguments and Options
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack list
```

```sh
cd core/python
uv run watchtower-core pack list --format json
```

## Behavior and Outputs
- Reads the hosted-pack registry from `core/control_plane/registries/pack_registry.json`.
- Reports each hosted pack's slug, pack ID, command namespace, distribution, package name, and settings paths.
- In `json` mode, returns one result array for scripting and workflow use.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection and validation. |
| `watchtower-core pack describe` | Shows the runtime-manifest details for one hosted pack. |
| `watchtower-core pack validate` | Validates one hosted pack contract directly. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/control_plane/registries/pack_registry.json`

## Updated At
- `2026-03-20T19:20:00Z`
