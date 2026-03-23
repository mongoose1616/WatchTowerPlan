# `watchtower-core pack`

## Summary
This command group inspects, scaffolds, bootstraps, and validates hosted domain-pack integration contracts.

## Use When
- You want to see which hosted packs the current repository exposes.
- You need the runtime manifest and registry details for one pack before changing host or pack wiring.
- You want a starter hosted-pack root plus the exact registry and workspace snippets needed to finish host wiring deliberately.
- You want one guarded command to register a scaffolded or pack-authored root into shared host composition.
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
- `<pack_command>`: Choose `list`, `describe`, `scaffold`, `bootstrap`, or `validate`.
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
uv run watchtower-core pack validate --format json
```

```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug oversight --pack-root packs/oversight --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path packs/oversight/.wt/manifests/pack_settings.json --write --format json
```

## Behavior and Outputs
- With no leaf command, the group prints pack-specific help and exits successfully.
- `list` reports the effective hosted-pack runtime view. In steady state that matches the shared registry; during copied-core bring-up it may also include runtime-only packs discovered from valid local manifests.
- `describe` combines the effective runtime entry plus the pack-owned runtime manifest for one hosted pack.
- `scaffold` renders the pack-owned starter files for one new hosted pack without mutating shared host surfaces.
- `bootstrap` applies the shared hosted-pack registry and `core/python` workspace wiring for one pack, then validates the resulting steady-state contract.
- `validate` runs the pack-contract validator directly for one hosted pack, including pack-owned command-doc, owned-root, and shared workspace registration checks. Runtime-only discovered packs validate as structured failures until bootstrap persists the shared wiring they are missing.
- Use `validate all` when you want pack-interface validation included in the broader repository pass.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack list` | Lists the effective hosted packs available to runtime composition. |
| `watchtower-core pack describe` | Shows one hosted pack's effective runtime entry, runtime manifest, and integration-module status. |
| `watchtower-core pack scaffold` | Creates a starter hosted-pack root and emits the pack settings path to bootstrap next. |
| `watchtower-core pack bootstrap` | Registers one hosted pack into shared host composition and shared workspace metadata. |
| `watchtower-core pack validate` | Runs the pack-contract validator directly for one hosted pack. |
| `watchtower-core validate all` | Includes pack-contract validation inside the broader repository validation pass. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_family.py`
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/control_plane/registries/pack_registry.json`

## Updated At
- `2026-03-22T23:45:00Z`
