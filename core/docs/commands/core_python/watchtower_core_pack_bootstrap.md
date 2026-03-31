# `watchtower-core pack bootstrap`

## Summary
This command reconciles one hosted pack into the shared hosted-pack registry, shared `core/python` workspace metadata, the shared governed discovery surfaces, and any declared pack-local `sync all` slice when the workspace is ready.

## Use When
- You have already scaffolded or authored a pack root and want the host to load it through the normal pack contract.
- You want one guarded command to update `pack_registry.json`, `core/python/pyproject.toml`, shared command discovery, shared repository-path discovery, and optional workspace sync behavior together.
- You want copied-core bring-up to reconcile the broader shared and pack-local derived state, not just the registry and workspace metadata.
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
uv run watchtower-core pack bootstrap --pack-settings-path <path> [--write] [--no-sync-workspace] [--sync-extra <extra>]... [--replace-hosted-packs] [--format <human|json>]
```

## Arguments and Options
- `--pack-settings-path <path>`: Required repository-relative path to the pack settings manifest for the pack being bootstrapped.
- `--write`: Persist the shared registry and workspace updates. Without this flag, the command is a dry run.
- `--no-sync-workspace`: Skip `uv sync` after writing the shared workspace metadata.
- `--sync-extra <extra>`: Optional `uv sync --extra <extra>` group to include during workspace sync. Repeat for multiple extras such as `dev`.
- `--replace-hosted-packs`: Scrub the current shared hosted-pack registrations and shared `core/python` pack wiring before reloading the target pack as the new default repository pack.
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

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --write --sync-extra dev --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --replace-hosted-packs --write --format json
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
- `--replace-hosted-packs` is the copied-core scrub-and-reload mode: it removes the current shared hosted-pack registry entries, rewrites `core/python/pyproject.toml` to retain only the target pack's shared workspace registration, and then rebuilds the shared discovery indexes for the recipient pack.
- The command only reconciles shared hosted-pack wiring. It does not build a curated staged export or scrub donor retained records, test trees, internal assessment docs, or other customer-release exclusions described in [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md).
- The command also does not reinterpret donor-specific shared-core tests or docs as recipient contract. If pack-neutral shared-core validation fails after copied-core apply, fix the donor shared core and restage the extract rather than expecting bootstrap to hide donor drift.
- Rebuilds the shared discovery indexes whenever the shared hosted-pack registry changes:
  - `core/control_plane/indexes/commands/command_index.json`
  - `core/control_plane/indexes/repository_paths/repository_path_index.json`
  - `core/control_plane/indexes/references/reference_index.json`
  - `core/control_plane/indexes/standards/standard_index.json`
  - `core/control_plane/indexes/workflows/workflow_index.json`
  - `core/control_plane/indexes/routes/route_index.json`
- When the selected pack declares the `all` sync target and the workspace is already usable, bootstrap also runs `watchtower-core <pack-namespace> sync all --write --format json` so pack-local derived indexes and trackers are materialized in the same pass.
- When `--no-sync-workspace` defers a required shared workspace sync, bootstrap defers the pack-local `sync all` pass too and reports it explicitly in `next_steps` instead of leaving the repository in a quiet half-bootstrapped state.
- When a new pack will publish workflow IDs outside the shared core workflow metadata registry, scaffold or author the pack-owned `workflow_metadata_registry` before bootstrap so later workflow-index and route-preview runs have the required metadata.
- Bootstrap does not rewrite pack-owned foundations docs automatically. When the selected pack publishes a pack-owned foundations view such as `<pack>/docs/foundations/**`, copy `core/docs/foundations/**` into that pack-owned root during bootstrap bring-up and adapt the pack-local wording before treating the pack as fully bootstrapped.
- Copy-forward support applies to source-owned `core/` surfaces only. Do not copy `core/python/.venv`, editable-install metadata from an existing environment, build caches, or pack `.wt/runtime/**` outputs into the consuming repository.
- When `--write` is omitted, reports the pending shared changes without mutating the repository.
- When `--write` is used and the shared workspace is synced, validates the hosted pack immediately after applying the shared wiring and restores the shared files if validation fails.
- When `--write` is used with `--no-sync-workspace`, applies the shared wiring but reports validation as deferred until the shared workspace is synced honestly.
- Runs `uv sync` by default after writing shared workspace metadata. Add `--sync-extra dev` or other repeatable extras when the recipient workspace should come up with optional dependency groups during the same bootstrap pass.
- Use `--no-sync-workspace` only when a staged change or test fixture intentionally needs to defer that step and run explicit validation afterward.
- The default write path requires `uv` to be installed and available on `PATH`. If the current machine does not have `uv` yet, install it first by following [uv_reference.md](/core/docs/references/uv_reference.md) or the onboarding steps in [core/python/README.md](/core/python/README.md).

## Copied-Core Rehost
Use this start-up flow when a recipient repository copied `core/` exactly from a donor repository and now needs to replace the donor's hosted-pack wiring with its own pack.

1. In the donor repository, prefer `watchtower-core pack extract-core --output-root <path> --overwrite --format json` instead of a raw `core/` copy when you control the source repository.
2. In the recipient repository, run `watchtower-core pack apply-core --source-root <path> --write --format json` to replace the local `core/` tree from the staged extract while preserving local `.venv` and cache residue.
3. Confirm `uv` is installed and available on `PATH`. If not, install it first by following [uv_reference.md](/core/docs/references/uv_reference.md) or the onboarding steps in [core/python/README.md](/core/python/README.md), then verify with `uv --version`.
4. Author or scaffold the recipient pack root and confirm its `pack_settings.json` plus `pack_runtime_manifest.json` are valid.
5. Run `watchtower-core pack bootstrap --pack-settings-path <recipient>/.wt/manifests/pack_settings.json --replace-hosted-packs --write --sync-extra dev --format json`.
6. On the normal path, bootstrap now materializes the recipient pack's declared `sync all` slice automatically after shared workspace reconciliation. No extra manual pack-local sync step should be needed.
7. If copied-core validation still fails because a shared-core test or doc names donor-pack validators, workflows, rendered surfaces, or tracking files directly, stop and fix the donor shared core before continuing. `pack bootstrap` only reconciles recipient hosted-pack wiring; it does not convert donor-specific shared-core assertions into recipient-owned ones.
8. If the recipient pack publishes a pack-owned foundations view such as `<pack>/docs/foundations/**`, copy `core/docs/foundations/**` into that pack-owned root and adapt the pack-local wording before final validation.
9. If a staged change or fixture intentionally needs to defer the honest workspace sync, add `--no-sync-workspace`, then run `uv sync --extra dev`, `watchtower-core <recipient-namespace> sync all --write --format json`, and `watchtower-core pack validate --pack-settings-path <recipient>/.wt/manifests/pack_settings.json --format json` as soon as the shared workspace can be synced honestly.
10. Run `watchtower-core pack list --format json` and `watchtower-core validate all --format json` to confirm the recipient pack now owns the shared host wiring.
11. Run `watchtower-core pack export --output-root <path> --include-pack <slug> --overwrite --format json` before treating the copied repository as a customer-safe deliverable, or `watchtower-core pack export --output-root <path> --include-pack <slug> --pack-only --overwrite --format json` when you need an additive pack bundle without shared core.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection, scaffold, bootstrap, and validation flows. |
| `watchtower-core pack extract-core` | Preferred donor-side engineering extract when repo-to-repo shared-core refresh is the goal. |
| `watchtower-core pack apply-core` | Preferred recipient-side helper for replacing `core/` from a staged engineering extract without deleting local dev residue. |
| `watchtower-core pack export` | Builds the curated staged export that bootstrap alone does not provide. |
| `watchtower-core pack scaffold` | Generates the pack-owned starter surfaces that bootstrap then registers. |
| `watchtower-core pack validate` | Validates the same hosted pack contract directly. |
| `watchtower-core validate all` | Includes pack-contract validation in the broader repository validation pass after bootstrap. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/python/src/watchtower_core/pack_integration/bootstrap.py`
- `core/python/src/watchtower_core/pack_integration/workspace_registration.py`
- `core/python/src/watchtower_core/validation/pack_contract.py`

## Updated At
- `2026-03-29T03:35:00Z`
