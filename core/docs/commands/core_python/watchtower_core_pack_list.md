# `watchtower-core pack list`

## Summary
This command lists the hosted packs available through the effective runtime view.

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
- Reads the effective hosted-pack runtime view from shared registry data plus any valid runtime-only manifest discoveries available in the current repository.
- Reports each hosted pack's slug, pack ID, command namespace, distribution, package name, and settings paths.
- Marks the default repository pack from authored registry metadata when present; otherwise it derives the default from the active pack settings path when one usable pack is available during copied-core bring-up.
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
- `core/python/src/watchtower_core/pack_integration/runtime_registry.py`

## Updated At
- `2026-03-22T23:45:00Z`
