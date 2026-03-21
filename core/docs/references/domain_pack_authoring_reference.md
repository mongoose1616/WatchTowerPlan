---
id: "ref.domain_pack_authoring"
title: "Domain Pack Authoring Reference"
summary: "Reference for structuring a domain pack so it integrates cleanly with reusable core and a host-owned CLI."
type: "reference"
status: "active"
tags:
  - "reference"
  - "domain_pack"
  - "architecture"
owner: "repository_maintainer"
updated_at: "2026-03-21T21:58:00Z"
audience: "shared"
authority: "reference"
---

# Domain Pack Authoring Reference

## Summary
This reference describes the expected shape of a WatchTower domain pack and how that shape differs from reusable core and host-owned composition code.

## Purpose
Make future packs portable and comprehensible by documenting the intended split between shared core, host composition, and pack-native runtime code.

## Scope
- Covers the repository-facing shape of a domain pack, including machine state, durable docs, workflows, tracking, and pack-native Python code.
- Covers the intended dependency boundaries for `watchtower_core`, `watchtower_host`, and `watchtower_<pack>`.
- Does not by itself define the final validator contract; that belongs in the companion standards and schemas.

## Canonical Upstream
- `https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/` - PyPA guidance for Python plugin discovery patterns.
- `https://packaging.python.org/en/latest/specifications/pyproject-toml/` - `pyproject.toml` specification for Python package metadata and scripts.
- `https://docs.python.org/3/library/argparse.html` - Python `argparse` reference for namespaced subcommand trees.
- `https://docs.python.org/3/library/importlib.metadata.html` - Python metadata lookup reference for optional entry-point adapters.

## Related Standards and Sources
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md): captures the discovery and registration tradeoffs that shape how packs integrate with the host.
- [argparse_subcommands_reference.md](/core/docs/references/argparse_subcommands_reference.md): supports the namespaced command-tree patterns that pack-owned CLI surfaces should follow.
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md): records the packaging metadata and multi-package constraints that affect copy-out portability.
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md): turns the architectural split in this reference into an enforceable repository standard.
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): governs the machine contracts that a pack must publish to be host-loadable.
- [requirements.md](/requirements.md): provides the authoritative endstate direction for reusable core, hosted domains, and portability expectations.
- [decisions.md](/decisions.md): records the repository-level design decisions that this reference must support rather than reinterpret.

## Quick Reference or Distilled Reference
### Layer Responsibilities
| Layer | Owns | Must Not Own |
|---|---|---|
| `watchtower_core` | Reusable schemas, validators, typed contracts, loaders, pack-agnostic helpers, control-plane access. | Pack business logic, host CLI composition, direct imports of any `watchtower_<pack>`. |
| `watchtower_host` | CLI parser construction, pack discovery, manifest loading, pack dispatch, command registration composition. | Pack-specific runtime rules or authored machine state. |
| `watchtower_<pack>` | Pack-native orchestration, lifecycle behavior, rendering, domain validation semantics, pack-owned docs and workflows. | Host internals, reusable-core ownership, mirrored copies of every generic core package family. |

### Pack Root Shape
| Surface | Expected Role |
|---|---|
| `<pack>/.wt/**` | Live pack machine state and pack-owned manifests. |
| `<pack>/docs/**` | Durable pack-local guidance and command docs. |
| `<pack>/workflows/**` | Pack-local workflow modules and routing. |
| `<pack>/tracking/**` | Human-facing pack tracking views when the pack owns them. |
| `<pack>/python/**` | Pack-native Python package and tests. |
| Optional domain roots | Pack-specific runtime surfaces such as `initiatives/`, `projects/`, `targets/`, or `reviews/`. |

### Rules or Decision Points
- Keep generic logic in reusable core unless it is truly pack-specific.
- Let the host be the only layer that composes reusable core with one or more packs.
- Make the pack portable: copy-out should require packaging or installation updates, not Python code rewrites.
- Keep pack-manifest and pack-settings paths repository-relative, portable, and directly rooted under the declared machine root.
- Prefer feature-owned modules inside a pack such as `bootstrap`, `initiatives`, `projects`, `tasks`, or `reviews` instead of mirroring generic core package families.
- Keep machine interface declarations in governed manifests and registries, not hidden in Python import conventions.
- Make integration hooks describe real pack capabilities. `query_runtime` and `sync_targets` should return typed runtime summaries with non-empty command and target inventories, not placeholders.
- Keep `integration_module` under the pack’s declared `python_package`; jumping out into unrelated packages weakens copy-out portability.
- Keep pack-settings surfaces pack-local unless they intentionally consume shared `core/control_plane/**` machine authority.
- Publish the pack namespace command entry page inside the pack-owned docs root so host introspection and pack-interface validation can find it without special cases.
- Expect pack-interface validation to scan live source roots when present; pack code must stay free of `watchtower_host` imports and reusable core must stay free of pack imports.
- Use `domain_roots` for optional pack-native roots that are not part of the shared workspace baseline.
- Exercise copy-out and extensibility proofs through each pack’s own `<pack>/python/src` path instead of relying only on shared test-fixture import roots.

### Portable Pack Authoring Checklist
1. Create the pack-owned root surfaces.
   - Start from `core/docs/templates/pack/` for the shared registry entry, pack manifests, pack-owned Python package, and namespace command page.
   - Minimum roots: `<pack>/.wt/`, `<pack>/docs/`, `<pack>/workflows/`, `<pack>/tracking/`, and `<pack>/python/`.
   - Add optional `domain_roots` such as `targets/`, `reviews/`, `artifacts/`, or `assessments/` only when the pack truly owns them.
2. Publish the machine contracts.
   - Add `<pack>/.wt/manifests/pack_settings.json`.
   - Add `<pack>/.wt/manifests/pack_runtime_manifest.json`.
   - Keep both manifests under `<pack>/.wt/manifests/` and keep all declared paths repository-relative.
3. Publish the pack-native Python harness.
   - Add `<pack>/python/pyproject.toml`.
   - Add `<pack>/python/src/watchtower_<pack>/__init__.py`.
   - Add `<pack>/python/src/watchtower_<pack>/integration.py` exporting `PACK_INTEGRATION`.
   - Keep the integration module inside the declared `python_package`.
4. Publish the pack-owned command docs.
   - Add the namespace entry page at `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md`.
   - Keep pack-specific command docs under the pack’s docs root instead of shared core docs.
5. Register the pack with host composition.
   - Add one entry to `core/control_plane/registries/pack_registry.json`.
   - Keep `pack_id`, `pack_slug`, `command_namespace`, `python_distribution`, `python_package`, and manifest paths aligned across the registry and manifests.
6. Validate the contract before treating the pack as loadable.
   - Run `uv run watchtower-core pack validate --pack-settings-path <pack>/.wt/manifests/pack_settings.json --format json`.
   - Run `uv run watchtower-core pack describe --pack <slug> --format json`.
7. Prove portability and extensibility.
   - Make the pack importable from its own `<pack>/python/src` path or installed package root.
   - Run at least one namespaced CLI proof such as `uv run watchtower-core <namespace> --help` or parser-introspection coverage.
   - When the host-pack contract changes materially, prove the change against a second pack or synthetic second-pack fixture rather than validating only the default pack.

### Starter Template Set
| Template | Use |
|---|---|
| `core/docs/templates/pack/pack_registry_entry_template.json` | Seed the shared hosted-pack registry entry in `core/control_plane/registries/pack_registry.json`. |
| `core/docs/templates/pack/pack_settings_template.json` | Seed `<pack>/.wt/manifests/pack_settings.json`. |
| `core/docs/templates/pack/pack_runtime_manifest_template.json` | Seed `<pack>/.wt/manifests/pack_runtime_manifest.json`. |
| `core/docs/templates/pack/pack_python_pyproject_template.toml` | Seed `<pack>/python/pyproject.toml`. |
| `core/docs/templates/pack/pack_package_init_template.py` | Seed `<pack>/python/src/watchtower_<pack>/__init__.py`. |
| `core/docs/templates/pack/pack_integration_module_template.py` | Seed `<pack>/python/src/watchtower_<pack>/integration.py`. |
| `core/docs/templates/pack/pack_namespace_command_reference_template.md` | Seed `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md`. |
| `core/docs/templates/readme_template.md` | Seed pack-local README.md files where the starter set does not include a pack-specific doc scaffold. |
| `core/docs/templates/workflow_template.md` and `core/docs/templates/routing_table_template.md` | Seed pack-local workflow modules and routing tables when the new pack owns its own workflow root. |

### Minimum Portable Pack File Set
| File | Why It Exists |
|---|---|
| `<pack>/.wt/manifests/pack_settings.json` | Declares the pack load root and governed surfaces |
| `<pack>/.wt/manifests/pack_runtime_manifest.json` | Declares host-facing runtime metadata and owned roots |
| `<pack>/python/pyproject.toml` | Makes the pack package installable or externally importable |
| `<pack>/python/src/watchtower_<pack>/__init__.py` | Creates the pack-owned Python package root |
| `<pack>/python/src/watchtower_<pack>/integration.py` | Exports `PACK_INTEGRATION` for host discovery |
| `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md` | Publishes the pack namespace command-doc entry page |
| `core/control_plane/registries/pack_registry.json` entry | Registers the pack with shared host composition |

### Worked Comparison
| Concern | `plan` Pack Shape | Future `oversight`-style Pack Shape |
|---|---|---|
| Primary domain work | Initiative, project, task, promotion, and closeout flows. | Review, assessment, oversight trace, or evidence-heavy domain flows. |
| Shared dependency | `watchtower_core` contracts, loaders, validators, and shared helpers. | Same shared dependency set. |
| Host integration | One manifest plus one integration module loaded by the host. | Same host seam, different capabilities declared. |
| Pack-owned docs | `plan/docs/**` and `plan/workflows/**`. | `oversight/docs/**` and `oversight/workflows/**`. |

### Failure Modes
- Putting pack-native orchestration back into `watchtower_core` creates hidden coupling and blocks future pack reuse.
- Recreating `query`, `sync`, or `validation` package trees inside every pack can turn packs into mirrored copies of core instead of domain runtimes.
- Letting a pack depend on repository-specific path hacks breaks copy-out portability.
- Letting a manifest point outside the pack or shared core control-plane roots introduces hidden repository coupling.
- Importing `watchtower_host` from pack code or importing pack code from `watchtower_core` violates the hosted-pack contract and should fail validation.
- Keeping pack command docs in shared core docs muddies ownership and makes additional packs awkward.
- Omitting the pack namespace entry page breaks deterministic command-doc lookup and should fail pack validation.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository standards, workflow modules, and boundary guidance around hosted-pack integration.

### Current Touchpoints
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md)
- [domain_pack_authoring_standard.md](/core/docs/standards/engineering/domain_pack_authoring_standard.md)
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md)
- [core/workflows/modules/domain_pack_integration.md](/core/workflows/modules/domain_pack_integration.md)
- [core/workflows/modules/pack_interface_validation.md](/core/workflows/modules/pack_interface_validation.md)

### Why It Matters Here
- The repository is actively separating reusable core, host composition, and pack-native runtime code.
- This reference exists so new standards, manifests, validators, and workflow modules can converge on one pack model instead of repeating assumptions in multiple places.

### If Local Policy Tightens
- Add or update the core-owned Python-boundary standard, pack-interface contract standard, pack-interface validator guidance, workflow routes for pack authoring, and package README or AGENTS surfaces in the same slice.

## Process or Workflow
1. Define the pack's owned roots and machine surfaces.
2. Define the pack's runtime manifest and typed integration hooks.
3. Keep host composition out of pack code and pack behavior out of reusable core.
4. Validate the pack interface and dependency direction before registering commands.

## Examples
- [plan/README.md](/plan/README.md)
- [plan/python/README.md](/plan/python/README.md)
- `WatchTowerOversight` as a second-pack design reference for future capabilities and docs shape
- `core/python/tests/fixtures/python/watchtower_oversight_fixture/` as the repository’s synthetic second-pack source package for multi-pack contract tests
- `core/python/tests/integration/test_pack_externalization.py` as the externalized proof that both the default `plan` pack and a second `oversight`-style pack can load from pack-owned `python/` roots

## References
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md)
- [argparse_subcommands_reference.md](/core/docs/references/argparse_subcommands_reference.md)
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md)

## Notes
- This reference is intentionally ahead of the final contract implementation so the architecture slice can converge on one explicit shape.
- Canonical upstream sources were reviewed on 2026-03-20 during the host-pack boundary hard-cutover tranche.

## Updated At
- `2026-03-21T21:58:00Z`
