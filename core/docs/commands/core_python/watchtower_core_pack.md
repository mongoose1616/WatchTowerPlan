# `watchtower-core pack`

## Summary
This command group inspects, scaffolds, and validates hosted domain-pack integration contracts.

## Use When
- You want to see which hosted packs the current repository exposes.
- You need the runtime manifest and registry details for one pack before changing host or pack wiring.
- You want a starter hosted-pack root plus the exact registry and workspace snippets needed to finish host wiring deliberately.
- You want a dedicated pack-interface validation command instead of relying only on `validate all`.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack <pack_command> [args]
```

## Arguments and Options
- `<pack_command>`: Choose `list`, `describe`, `scaffold`, or `validate`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack --help
```

```sh
cd core/python
uv run watchtower-core pack list --format json
```

```sh
cd core/python
uv run watchtower-core pack validate --pack plan --format json
```

```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug oversight --pack-root packs/oversight --format json
```

```sh
cd core/python
uv run watchtower-core pack validate --pack oversight --format json
```

## Behavior and Outputs
- With no leaf command, the group prints pack-specific help and exits successfully.
- `list` reads the shared hosted-pack registry and reports the declared packs.
- `describe` combines the shared registry entry plus the pack-owned runtime manifest for one hosted pack.
- `scaffold` renders the pack-owned starter files plus the registry and `core/python` workspace snippets needed to finish host wiring deliberately.
- `validate` runs the pack-contract validator directly for one hosted pack, including pack-owned command-doc and owned-root checks.
- Use `validate all` when you want pack-interface validation included in the broader repository pass.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack list` | Lists the hosted packs declared in the shared registry. |
| `watchtower-core pack describe` | Shows one hosted pack's registry entry, runtime manifest, and integration-module status. |
| `watchtower-core pack scaffold` | Creates a starter hosted-pack root and emits the registry plus workspace snippets needed for host wiring. |
| `watchtower-core pack validate` | Runs the pack-contract validator directly for one hosted pack. |
| `watchtower-core validate all` | Includes pack-contract validation inside the broader repository validation pass. |
| `watchtower-core plan` | Current hosted default pack namespace. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_family.py`
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/control_plane/registries/pack_registry.json`

## Updated At
- `2026-03-22T03:35:00Z`
