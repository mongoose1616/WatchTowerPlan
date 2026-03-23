# `watchtower-core pack scaffold`

## Summary
This command renders a starter hosted-pack root so the new pack can be registered through the guarded bootstrap flow.

## Use When
- You are creating a new hosted pack and want the minimum pack-owned machine, docs, workflow, tracking, and Python surfaces generated consistently.
- You want the exact pack settings path and shared-wiring preview needed to hand the new pack off to `watchtower-core pack bootstrap`.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core pack scaffold` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/pack_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug <pack_slug> --pack-root <repo_relative_pack_root> [--command-namespace <namespace>] [--python-distribution <distribution>] [--python-package <python_package>] [--domain-root <name>]... [--format <human|json>]
```

## Arguments and Options
- `--pack-slug <pack_slug>`: Required hosted-pack slug such as `oversight`.
- `--pack-root <repo_relative_pack_root>`: Required repository-relative pack root such as `oversight` or `packs/oversight`.
- `--command-namespace <namespace>`: Optional namespace override. Defaults to `--pack-slug`.
- `--python-distribution <distribution>`: Optional distribution override. Defaults to `watchtower-<pack_slug>`.
- `--python-package <python_package>`: Optional package override. Defaults to `watchtower_<pack_slug>`.
- `--domain-root <name>`: Optional pack-local domain root name. Repeat for multiple roots.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug oversight --pack-root oversight
```

```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug reviews --pack-root packs/reviews --domain-root assessments --domain-root reviews --format json
```

## Behavior and Outputs
- Renders pack-owned starter files under the requested pack root, including pack manifests, minimal validation registries, a starter note schema and artifact, namespace command docs, workflow guidance, tracking guidance, and the pack-native Python package skeleton.
- Renders a starter pack-owned `workflow_metadata_registry` and wires the starter `pack_settings.json`, validator registry, and validation suite to it so new packs have a place to publish pack-specific workflow IDs immediately.
- Fails closed when the requested pack slug, namespace, distribution, or package would collide with an existing hosted pack already declared in the shared pack registry.
- Does not mutate `core/control_plane/registries/pack_registry.json` or `core/python/pyproject.toml` automatically.
- Emits the exact shared-registry and shared-workspace registration data that `watchtower-core pack bootstrap` will apply.
- Supports both first-party root-pack shapes and nested `packs/<slug>` shapes. Use a direct root such as `oversight/` unless you are deliberately hosting the pack beneath a multi-pack directory.
- After scaffold, use `watchtower-core pack bootstrap --pack-settings-path <path> --write --format json` to register the pack and validate the resulting host wiring.
- Replace the starter workflow metadata entry with the pack's real workflow IDs before relying on workflow indexing, route preview, or pack-owned workflow docs.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection, scaffold, bootstrap, and validation flows. |
| `watchtower-core pack bootstrap` | Registers the generated pack into the shared registry and shared workspace metadata. |
| `watchtower-core pack validate` | Validates the generated pack after bootstrap or deliberate shared-wiring updates. |
| `watchtower-core validate all` | Includes pack-contract validation after the generated pack is registered and installed. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/python/src/watchtower_core/pack_integration/scaffold.py`
- `core/docs/templates/pack/`

## Updated At
- `2026-03-23T05:10:00Z`
