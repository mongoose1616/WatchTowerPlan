# `watchtower-core pack describe`

## Summary
This command describes one hosted pack's registry entry and runtime manifest.

## Use When
- You need the owned roots, integration module, or declared capabilities for one hosted pack.
- You are reviewing host-to-pack integration wiring before making boundary changes.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack describe` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack describe [--pack <pack_slug>] [--format <human|json>]
```

## Arguments and Options
- `--pack <pack_slug>`: Hosted pack slug. Defaults to the default repository pack.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack describe
```

```sh
cd core/python
uv run watchtower-core pack describe --format json
```

## Behavior and Outputs
- Reads the shared hosted-pack registry entry and the pack-owned runtime manifest for the selected pack.
- Reports declared capabilities, required validation suites, owned roots, the integration module path, and the typed query or sync runtimes published by the pack integration descriptor.
- Separates integration-module import status from runtime-hook validity so malformed query or sync contracts stay visible to operators instead of looking like a plain import failure.
- Attempts to import the declared integration module and reports whether that import succeeds.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection and validation. |
| `watchtower-core pack list` | Lists the hosted packs available to describe. |
| `watchtower-core pack validate` | Validates the same hosted pack contract directly. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/control_plane/registries/pack_registry.json`

## Updated At
- `2026-03-20T23:58:00Z`
