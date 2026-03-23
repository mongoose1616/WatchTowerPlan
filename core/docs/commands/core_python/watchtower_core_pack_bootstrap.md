# `watchtower-core pack bootstrap`

## Summary
This command reconciles one hosted pack into the shared hosted-pack registry, shared `core/python` workspace metadata, and the shared governed discovery surfaces.

## Use When
- You have already scaffolded or authored a pack root and want the host to load it through the normal pack contract.
- You want one guarded command to update `pack_registry.json`, `core/python/pyproject.toml`, shared command discovery, shared repository-path discovery, and optional workspace sync behavior together.
- You want copied-core bring-up to reconcile the broader shared discovery state, not just the registry and workspace metadata.
- You want bootstrap-time validation before treating a new hosted pack as loadable.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack bootstrap` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path <path> [--write] [--no-sync-workspace] [--format <human|json>]
```

## Arguments and Options
- `--pack-settings-path <path>`: Required repository-relative path to the pack settings manifest for the pack being bootstrapped.
- `--write`: Persist the shared registry and workspace updates. Without this flag, the command is a dry run.
- `--no-sync-workspace`: Skip `uv sync` after writing the shared workspace metadata.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --write --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --write --no-sync-workspace --format json
```

## Behavior and Outputs
- Loads the declared pack settings and runtime manifest before changing shared host surfaces.
- Expects any pack-owned `workflow_metadata_registry` declared by `pack_settings.json` to exist already; bootstrap does not invent pack-local workflow metadata for the pack.
- Fails closed when the pack settings path is not repository-relative and portable.
- Fails closed when the declared integration module cannot be resolved beneath the pack-owned `python/src` root.
- Computes and applies the shared `pack_registry.json` entry plus the shared `core/python/pyproject.toml` dev-dependency and `tool.uv.sources` registration for the pack.
- Promotes a runtime-only discovered copied-core pack into the normal steady-state shared registry and shared workspace contract.
- Works for both first-party root packs and nested `packs/<slug>` packs as long as the manifest path is repository-relative and the pack contract is valid.
- Preserves an existing pack's `default_repo_pack` and notes when the bootstrap targets a pack already in the registry.
- Removes unusable donor registry entries when copied-core bootstrap is reconciling the current repository's active hosted pack into place.
- Rebuilds the shared discovery indexes whenever the shared hosted-pack registry changes:
  - `core/control_plane/indexes/commands/command_index.json`
  - `core/control_plane/indexes/repository_paths/repository_path_index.json`
  - `core/control_plane/indexes/references/reference_index.json`
  - `core/control_plane/indexes/standards/standard_index.json`
  - `core/control_plane/indexes/workflows/workflow_index.json`
  - `core/control_plane/indexes/routes/route_index.json`
- When a new pack will publish workflow IDs outside the shared core workflow metadata registry, scaffold or author the pack-owned `workflow_metadata_registry` before bootstrap so later workflow-index and route-preview runs have the required metadata.
- Copy-forward support applies to source-owned `core/` surfaces only. Do not copy `core/python/.venv`, editable-install metadata from an existing environment, build caches, or pack `.wt/runtime/**` outputs into the consuming repository.
- When `--write` is omitted, reports the pending shared changes without mutating the repository.
- When `--write` is used and the shared workspace is synced, validates the hosted pack immediately after applying the shared wiring and restores the shared files if validation fails.
- When `--write` is used with `--no-sync-workspace`, applies the shared wiring but reports validation as deferred until the shared workspace is synced honestly.
- Runs `uv sync` by default after writing shared workspace metadata. Use `--no-sync-workspace` only when a staged change or test fixture intentionally needs to defer that step and run explicit validation afterward.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection, scaffold, bootstrap, and validation flows. |
| `watchtower-core pack scaffold` | Generates the pack-owned starter surfaces that bootstrap then registers. |
| `watchtower-core pack validate` | Validates the same hosted pack contract directly. |
| `watchtower-core validate all` | Includes pack-contract validation in the broader repository validation pass after bootstrap. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/python/src/watchtower_core/pack_integration/bootstrap.py`
- `core/python/src/watchtower_core/pack_integration/workspace_registration.py`
- `core/python/src/watchtower_core/validation/pack_contract.py`

## Updated At
- `2026-03-23T22:05:00Z`
