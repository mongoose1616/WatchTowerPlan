# `watchtower-core pack bootstrap`

## Summary
This command registers one hosted pack into the shared hosted-pack registry and shared `core/python` workspace metadata.

## Use When
- You have already scaffolded or authored a pack root and want the host to load it through the normal pack contract.
- You want one guarded command to update `pack_registry.json`, `core/python/pyproject.toml`, and optional workspace sync behavior together.
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
uv run watchtower-core pack bootstrap --pack-settings-path packs/oversight/.wt/manifests/pack_settings.json --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path packs/oversight/.wt/manifests/pack_settings.json --write --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path packs/oversight/.wt/manifests/pack_settings.json --write --no-sync-workspace --format json
```

## Behavior and Outputs
- Loads the declared pack settings and runtime manifest before changing shared host surfaces.
- Fails closed when the pack settings path is not repository-relative and portable.
- Fails closed when the integration module cannot import from the pack-owned `python/src` root.
- Computes and applies the shared `pack_registry.json` entry plus the shared `core/python/pyproject.toml` dev-dependency and `tool.uv.sources` registration for the pack.
- Preserves an existing pack's `default_repo_pack` and notes when the bootstrap targets a pack already in the registry.
- When `--write` is omitted, reports the pending shared changes without mutating the repository.
- When `--write` is used, validates the hosted pack immediately after applying the shared wiring and restores the shared files if validation fails.
- Runs `uv sync` by default after writing shared workspace metadata. Use `--no-sync-workspace` only when a staged change or test fixture needs to defer that step deliberately.

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
- `2026-03-21T23:59:00Z`
