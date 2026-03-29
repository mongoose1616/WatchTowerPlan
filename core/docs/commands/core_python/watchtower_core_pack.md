# `watchtower-core pack`

## Summary
This command group inspects, extracts, applies, exports, scaffolds, bootstraps, and validates hosted domain-pack integration contracts.

## Use When
- You want to see which hosted packs the current repository exposes.
- You need the runtime manifest and registry details for one pack before changing host or pack wiring.
- You need a curated staged export for customer bootstrap or customer release handoff.
- You need a donor-neutral `core/` extract for engineering repo-to-repo refresh.
- You need a recipient-side helper to replace `core/` from a staged engineering extract without carrying a raw copy command around.
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
- `<pack_command>`: Choose `list`, `describe`, `extract-core`, `apply-core`, `export`, `scaffold`, `bootstrap`, or `validate`.
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
uv run watchtower-core pack export --output-root /tmp/customer_export --include-pack plan --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core pack extract-core --output-root /tmp/shared_core --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core pack apply-core --source-root /tmp/shared_core --write --format json
```

```sh
cd core/python
uv run watchtower-core pack export --output-root /tmp/customer_plan_pack --include-pack plan --pack-only --overwrite --format json
```

```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug oversight --pack-root oversight --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --write --format json
```

```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --replace-hosted-packs --write --format json
```

## Behavior and Outputs
- With no leaf command, the group prints pack-specific help and exits successfully.
- `list` reports the effective hosted-pack runtime view. In steady state that matches the shared registry; during copied-core bring-up it may also include runtime-only packs discovered from valid local manifests.
- `describe` combines the effective runtime entry plus the pack-owned runtime manifest for one hosted pack.
- `extract-core` stages a donor-neutral shared-core bundle for engineering reuse and validates it against the engineering-core portability contract.
- `apply-core` validates one staged engineering extract and applies its `core/` tree into the current repository while preserving recipient-local `.venv` and cache residue.
- `export` stages either a portability-clean repository bundle or a portability-clean pack-only bundle, depending on whether `--pack-only` is used.
- `release check` remains the preferred one-shot local gate when you want dirty-worktree protection and broad validation wrapped around export instead of calling `export` directly.
- `scaffold` renders the pack-owned starter files for one new hosted pack without mutating shared host surfaces.
- `bootstrap` applies the shared hosted-pack registry and `core/python` workspace wiring for one pack, then validates the resulting steady-state contract. In copied-core rehost flows, `--replace-hosted-packs` scrubs donor hosted-pack wiring before reloading the recipient pack.
- `validate` runs the pack-contract validator directly for one hosted pack, including pack-owned command-doc, owned-root, and shared workspace registration checks. Runtime-only discovered packs validate as structured failures until bootstrap persists the shared wiring they are missing.
- First-party root packs such as `oversight/` and nested multi-pack roots such as `packs/oversight/` are both supported. Shared help and examples use the first-party root-pack shape by default unless the externalized topology itself is what you are testing.
- Use `validate all` when you want pack-interface validation included in the broader repository pass.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack list` | Lists the effective hosted packs available to runtime composition. |
| `watchtower-core pack describe` | Shows one hosted pack's effective runtime entry, runtime manifest, and integration-module status. |
| `watchtower-core pack extract-core` | Builds a donor-neutral shared-core extract for engineering repo-to-repo reuse. |
| `watchtower-core pack apply-core` | Applies a staged engineering shared-core extract into the current repository core/ tree. |
| `watchtower-core pack export` | Builds a curated staged export of shared core plus selected hosted-pack roots, or a scrubbed pack-only bundle when `--pack-only` is used. |
| `watchtower-core release check` | Preferred one-shot local release gate that runs validation and dirty-worktree checks before staging the final export. |
| `watchtower-core pack scaffold` | Creates a starter hosted-pack root and emits the pack settings path to bootstrap next. |
| `watchtower-core pack bootstrap` | Registers one hosted pack into shared host composition and shared workspace metadata. |
| `watchtower-core pack validate` | Runs the pack-contract validator directly for one hosted pack. |
| `watchtower-core validate all` | Includes pack-contract validation inside the broader repository validation pass. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_family.py`
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/control_plane/registries/pack_registry.json`

## Updated At
- `2026-03-28T04:20:00Z`
