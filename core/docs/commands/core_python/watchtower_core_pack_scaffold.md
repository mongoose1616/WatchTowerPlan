# `watchtower-core pack scaffold`

## Summary
This command renders a starter hosted-pack root and emits the shared host-wiring snippets needed to register the new pack deliberately.

## Use When
- You are creating a new hosted pack and want the minimum pack-owned machine, docs, workflow, tracking, and Python surfaces generated consistently.
- You want the exact `pack_registry.json` entry and `core/python/pyproject.toml` snippets needed to finish host composition without editing those shared files blindly.

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
- `--pack-root <repo_relative_pack_root>`: Required repository-relative pack root such as `packs/oversight`.
- `--command-namespace <namespace>`: Optional namespace override. Defaults to `--pack-slug`.
- `--python-distribution <distribution>`: Optional distribution override. Defaults to `watchtower-<pack_slug>`.
- `--python-package <python_package>`: Optional package override. Defaults to `watchtower_<pack_slug>`.
- `--domain-root <name>`: Optional pack-local domain root name. Repeat for multiple roots.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug oversight --pack-root packs/oversight
```

```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug reviews --pack-root packs/reviews --domain-root assessments --domain-root reviews --format json
```

## Behavior and Outputs
- Renders pack-owned starter files under the requested pack root, including pack manifests, minimal validation registries, a starter note schema and artifact, namespace command docs, workflow guidance, tracking guidance, and the pack-native Python package skeleton.
- Fails closed when the requested pack slug, namespace, distribution, or package would collide with an existing hosted pack already declared in the shared pack registry.
- Does not mutate `core/control_plane/registries/pack_registry.json` or `core/python/pyproject.toml` automatically, because a newly registered pack that is not yet installed would break subsequent parser boot.
- Emits the exact `pack_registry_entry` and `core_python_workspace_registration` snippets needed to complete host wiring deliberately.
- After the emitted snippets are applied and `uv sync` has installed the new pack package, validate the pack with `watchtower-core pack validate --pack-settings-path <path> --format json`.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core pack` | Parent command group for hosted-pack inspection, scaffold, and validation flows. |
| `watchtower-core pack validate` | Validates the generated pack after the shared registry and workspace metadata are wired. |
| `watchtower-core validate all` | Includes pack-contract validation after the generated pack is registered and installed. |

## Source Surface
- `core/python/src/watchtower_host/cli/pack_handlers.py`
- `core/python/src/watchtower_core/pack_integration/scaffold.py`
- `core/docs/templates/pack/`

## Updated At
- `2026-03-22T03:35:00Z`
