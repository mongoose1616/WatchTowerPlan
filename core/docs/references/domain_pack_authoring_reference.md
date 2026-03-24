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
updated_at: "2026-03-23T23:20:00Z"
audience: "shared"
authority: "reference"
---

# Domain Pack Authoring Reference

## Summary
This reference describes the expected shape of a WatchTower domain pack and how that shape differs from reusable core and host-owned composition code.

## Purpose
Make future packs portable and comprehensible by documenting the intended split between shared core, host composition, and pack-native runtime code.

This repository also treats copy-forward adoption as a supported operating mode: downstream WatchTower repositories may consume the shared runtime by copying `core/` alone during bring-up or by copying `core/` together with one or more hosted packs. The pack set that remains present after that copy is owned by the consuming repository, not by the donor repository.

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
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md): defines the minimum integrated pack surface set and extension rules this guide operationalizes.
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md): turns the architectural split in this reference into an enforceable repository standard.
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): governs the machine contracts that a pack must publish to be host-loadable.
- [repository_scope.md](/core/docs/foundations/repository_scope.md): defines the shared boundary between reusable core, host composition, and hosted packs.
- [engineering_design_principles.md](/core/docs/foundations/engineering_design_principles.md): records the shared architectural principles this reference operationalizes.

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
| `<pack>/.wt/runtime/**` | Optional pack-local operational runtime outputs such as telemetry sinks. |
| `<pack>/docs/**` | Durable pack-local guidance and command docs. |
| `<pack>/workflows/modules/**` | Pack-local reusable workflow modules. |
| `<pack>/workflows/roles/**` | Pack-local workflow roles and persona-oriented orchestration docs. |
| `<pack>/workflows/ROUTING_TABLE.md` | Pack-local workflow routing. |
| `<pack>/tracking/**` | Human-facing pack tracking views when the pack owns them. |
| `<pack>/python/**` | Pack-native Python package and tests. |
| Optional domain roots | Pack-specific runtime surfaces such as `initiatives/`, `projects/`, `targets/`, or `reviews/`. |

- Preferred first-party layout is a direct repository child such as `<pack>/`; `packs/<slug>/` remains a supported nested convention for multi-pack or copied-repository layouts.
- Pack discovery should key off `<pack>/.wt/manifests/pack_settings.json`, not off one required parent directory name.

### Rules or Decision Points
- Keep generic logic in reusable core unless it is truly pack-specific.
- Let the host be the only layer that composes reusable core with one or more packs.
- Make the pack portable: copy-out should require packaging or installation updates, not Python code rewrites.
- Keep pack-manifest and pack-settings paths repository-relative, portable, and directly rooted under the declared machine root.
- Keep local runtime telemetry or similar ephemeral machine outputs under `<pack>/.wt/runtime/` and ignore them in Git rather than treating them as durable governed artifacts.
- Prefer feature-owned modules inside a pack such as `bootstrap`, `initiatives`, `projects`, `tasks`, or `reviews` instead of mirroring generic core package families.
- Keep machine interface declarations in governed manifests and registries, not hidden in Python import conventions.
- Make integration hooks describe real pack capabilities. `query_runtime` and `sync_targets` should return typed runtime summaries with non-empty command and target inventories, not placeholders.
- Keep `integration_module` under the pack’s declared `python_package`; jumping out into unrelated packages weakens copy-out portability.
- Keep pack-settings surfaces pack-local unless they intentionally consume shared `core/control_plane/**` machine authority.
- Treat effective pack activation as Phase 0 for any pack-aware runtime path. Host and reusable-core runtime helpers should resolve the effective pack settings path before reading runtime manifests, owned roots, or default-pack machine outputs.
- Build the full typed `PackContext` only when the caller needs declared pack-governed surfaces such as schema catalogs, validator registries, validation suites, policy registries, or other declared governance helpers. Minimal runtime-only pack fixtures may intentionally stop short of that full surface set.
- Keep pack-local validator registries limited to pack-owned validators. Do not copy shared core validator entries into a pack-local validator registry unless the entry is intentionally identical and temporary copied-core residue.
- When the pack owns workflow documents whose `workflow.*` IDs are not already described by the shared core workflow metadata registry, publish a pack-owned `workflow_metadata_registry` and keep it limited to pack-owned entries. The loader merges that registry with the shared core workflow metadata surface and rejects conflicting duplicates.
- When the pack owns workflow roles, require each role doc to include a `Composes Modules` section that lists the reusable workflow-module docs the role directly orchestrates.
- Treat pack-owned live indexes such as `task_index` and `initiative_index` as optional capabilities. Generic host commands should read them only when the active pack declares those surfaces.
- Keep pack-local semantic validation thin. Import shared helpers such as `watchtower_core.documentation.standards`, `watchtower_core.documentation.reference_semantics`, and `watchtower_core.sync.workflow_index` instead of forking donor copies into modules like `watchtower_<pack>.standards`.
- Publish the pack namespace command entry page inside the pack-owned docs root so host introspection and pack-interface validation can find it without special cases.
- Expect pack-interface validation to scan live source roots when present; pack code must stay free of `watchtower_host` imports and reusable core must stay free of pack imports.
- Use `domain_roots` for optional pack-native roots that are not part of the shared workspace baseline.
- Exercise copy-out and extensibility proofs through each pack’s own `<pack>/python/src` path instead of relying only on shared test-fixture import roots.

### Supported Repository Adoption Modes
| Mode | What Gets Copied | What Must Stay Repo-Local |
|---|---|---|
| Shared core only | `core/` while the consuming repo prepares or rehomes its hosted-pack set. | Pack registry entries, pack manifests, and shared-workspace package wiring for the packs that repo actually hosts. |
| Shared core plus one hosted pack | `core/` plus one pack root such as `<pack>/`. | The consuming repo still owns which pack is active by default and how the shared workspace points at that pack. |
| Shared core plus multiple hosted packs | `core/` plus multiple pack roots. | The consuming repo owns the hosted-pack inventory, default-pack choice, and any pack-local docs, workflows, and machine state. |

- Do not treat the donor repository's current internal pack as a reusable-core default just because its examples appear in shared docs.
- Do not hard-code a donor pack into shared workspace metadata, host defaults, or pack-authoring guidance; those are consuming-repository choices.
- Do not copy `core/python/.venv`, editable-install metadata, caches, or pack `.wt/runtime/**` outputs into the consuming repository. Copy-forward portability assumes source surfaces plus an explicit `watchtower-core pack bootstrap --write` reconciliation step, not donor environment residue.

### Portable Pack Authoring Checklist
1. Create the pack-owned root surfaces.
   - Prefer `uv run watchtower-core pack scaffold --pack-slug <slug> --pack-root <path>` for the starter surface set.
   - Start from `core/docs/templates/pack/` directly when you need to customize the starter before the first render or when you are working outside the host CLI.
   - Minimum roots: `<pack>/.wt/`, `<pack>/docs/`, `<pack>/workflows/`, `<pack>/tracking/`, and `<pack>/python/`.
   - Add optional `domain_roots` such as `targets/`, `reviews/`, `artifacts/`, or `assessments/` only when the pack truly owns them.
2. Publish the machine contracts.
   - Add `<pack>/.wt/manifests/pack_settings.json`.
   - Add `<pack>/.wt/manifests/pack_runtime_manifest.json`.
   - Add `<pack>/.wt/registries/workflow_metadata_registry.json` when the pack owns workflow IDs outside the shared core workflow metadata registry. New-pack scaffolds should keep the starter file and replace its example entry with real workflow IDs before relying on workflow indexing or route preview.
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
   - Prefer `uv run watchtower-core pack bootstrap --pack-settings-path <pack>/.wt/manifests/pack_settings.json --write --format json` once the pack-owned surfaces exist.
   - Use the dry-run bootstrap output when you need to review the shared changes before writing them.
   - Use `--no-sync-workspace` only when a staged change or test fixture intentionally needs to defer `uv sync` and a follow-on `pack validate` run.
   - Keep `pack_id`, `pack_slug`, `command_namespace`, `python_distribution`, `python_package`, and manifest paths aligned across the registry and manifests.
6. Validate the contract before treating the pack as loadable.
   - Run `uv run watchtower-core pack validate --pack-settings-path <pack>/.wt/manifests/pack_settings.json --format json`.
   - Run `uv run watchtower-core pack describe --pack <slug> --format json`.
   - Run `uv run watchtower-core doctor --format json` after bootstrap to prove the generic host health snapshot stays pack-neutral and does not assume plan-owned live indexes.
- In copied-core bring-up mode, `pack list`, `pack describe`, `pack validate`, selected namespaces, and `validate all` can use valid local manifests plus the declared pack-owned `<python_root>/src` path before shared registry and workspace wiring is written. Treat that as temporary compatibility and finish with `pack bootstrap --write`, which also reconciles the shared command, repository-path, reference, standard, workflow, and route discovery indexes for the copied repository.
- Keep runtime-only copied-pack proofs thin: when the test or command is only checking runtime-manifest, import, or command-namespace behavior, activate the effective pack first but do not require the full `PackContext`. Save full-context requirements for validation and governed-surface helpers that actually consume those surfaces.
7. Prove portability and extensibility.
   - Make the pack importable from its own `<pack>/python/src` path or installed package root.
   - Run at least one namespaced CLI proof such as `uv run watchtower-core <namespace> --help` or parser-introspection coverage.
   - When the host-pack contract changes materially, prove the change against a second pack or synthetic second-pack fixture rather than validating only the default pack.
   - When pack-owned document semantics or standard parsing changes materially, prove the change through shared helper imports rather than by copying shared parser modules into the pack.

### Starter Template Set
| Template | Use |
|---|---|
| `core/docs/templates/pack/pack_registry_entry_template.json` | Seed the shared hosted-pack registry entry in `core/control_plane/registries/pack_registry.json`. |
| `core/docs/templates/pack/pack_settings_template.json` | Seed `<pack>/.wt/manifests/pack_settings.json`. |
| `core/docs/templates/pack/pack_runtime_manifest_template.json` | Seed `<pack>/.wt/manifests/pack_runtime_manifest.json`. |
| `core/docs/templates/pack/pack_schema_catalog_template.json` | Seed `<pack>/.wt/registries/schema_catalog.json`. |
| `core/docs/templates/pack/pack_validation_suite_registry_template.json` | Seed `<pack>/.wt/registries/validation_suite_registry.json`. |
| `core/docs/templates/pack/pack_workflow_metadata_registry_template.json` | Seed `<pack>/.wt/registries/workflow_metadata_registry.json`. |
| `core/docs/templates/pack/pack_validator_registry_template.json` | Seed `<pack>/.wt/registries/validator_registry.json`. |
| `core/docs/templates/pack/pack_note_schema_template.json` | Seed the starter pack-local note schema under `<pack>/.wt/schemas/interfaces/packs/`. |
| `core/docs/templates/pack/pack_note_artifact_template.json` | Seed the starter pack-local note artifact under `<pack>/.wt/work_items/`. |
| `core/docs/templates/pack/pack_python_pyproject_template.toml` | Seed `<pack>/python/pyproject.toml`. |
| `core/docs/templates/pack/pack_package_init_template.py` | Seed `<pack>/python/src/watchtower_<pack>/__init__.py`. |
| `core/docs/templates/pack/pack_integration_module_template.py` | Seed `<pack>/python/src/watchtower_<pack>/integration.py`. |
| `core/docs/templates/pack/pack_namespace_command_reference_template.md` | Seed `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md`. |
| `core/docs/templates/readme_template.md` | Seed pack-local README.md files where the starter set does not include a pack-specific doc scaffold. |
| `core/docs/templates/workflow_template.md` and `core/docs/templates/routing_table_template.md` | Seed pack-local workflow modules, workflow roles, and routing tables when the new pack owns its own workflow roots. |

### Minimum Portable Pack File Set
| File | Why It Exists |
|---|---|
| `<pack>/.wt/manifests/pack_settings.json` | Declares the pack load root and governed surfaces |
| `<pack>/.wt/manifests/pack_runtime_manifest.json` | Declares host-facing runtime metadata and owned roots |
| `<pack>/.wt/registries/workflow_metadata_registry.json` | Extends the shared workflow metadata registry with pack-owned workflow IDs |
| `<pack>/python/pyproject.toml` | Makes the pack package installable or externally importable |
| `<pack>/python/src/watchtower_<pack>/__init__.py` | Creates the pack-owned Python package root |
| `<pack>/python/src/watchtower_<pack>/integration.py` | Exports `PACK_INTEGRATION` for host discovery |
| `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md` | Publishes the pack namespace command-doc entry page |
| `core/control_plane/registries/pack_registry.json` entry | Registers the pack with shared host composition |

### Minimum `pack_settings.json`
Use this as the smallest practical starting point for a load-root that can satisfy both the schema and the current pack validator.

```json
{
  "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
  "surface_name": "pack_settings",
  "contract_version": "v1",
  "description": "Load root for the <pack_slug> pack.",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "pack_id": "pack.<pack_slug>",
  "surfaces": [
    {
      "surface_name": "schema_catalog",
      "surface_kind": "schema_collection",
      "path": "<pack_root>/.wt/registries/schema_catalog.json",
      "authority": "authoritative",
      "visibility": "hidden"
    },
    {
      "surface_name": "validator_registry",
      "surface_kind": "registry",
      "path": "<pack_root>/.wt/registries/validator_registry.json",
      "authority": "authoritative",
      "visibility": "hidden"
    },
    {
      "surface_name": "validation_suite_registry",
      "surface_kind": "registry",
      "path": "<pack_root>/.wt/registries/validation_suite_registry.json",
      "authority": "authoritative",
      "visibility": "hidden"
    },
    {
      "surface_name": "workflow_metadata_registry",
      "surface_kind": "registry",
      "path": "<pack_root>/.wt/registries/workflow_metadata_registry.json",
      "authority": "authoritative",
      "visibility": "hidden"
    }
  ],
  "workspace_roots": {
    "workspace_root": "<pack_root>",
    "machine_root": "<pack_root>/.wt",
    "docs_root": "<pack_root>/docs",
    "workflows_root": "<pack_root>/workflows",
    "tracking_root": "<pack_root>/tracking",
    "overview_path": "<pack_root>/<pack_slug>_overview.md",
    "domain_roots": {}
  },
  "default_validation_suite_id": "suite.<pack_slug>.validation_baseline"
}
```

- Keep `schema_catalog`, `validator_registry`, and `validation_suite_registry` present by name. The current validator treats them as required runtime surfaces, not just optional declarations.
- Keep `workflow_metadata_registry` present when the pack owns workflow IDs outside the shared core registry, and replace the starter scaffold entry with the pack's real workflow IDs before rebuilding workflow or route indexes.
- Keep `overview_path` present even when the rendered overview is still a placeholder. It is part of the current schema contract.
- Add `domain_roots` only when the pack truly owns additional roots such as `reviews`, `assessments`, or `targets`.
- Keep pack-local validator registries additive. Shared core validators belong in `core/control_plane/registries/validator_registry.json`, not as conflicting copied entries inside the pack.

### Minimum `pack_runtime_manifest.json`
Use this as the smallest practical host-facing runtime manifest.

```json
{
  "$schema": "urn:watchtower:schema:interfaces:packs:pack-runtime-manifest:v1",
  "surface_name": "pack_runtime_manifest",
  "contract_version": "v1",
  "description": "Host-facing runtime manifest for the <pack_slug> pack.",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "pack_id": "pack.<pack_slug>",
  "pack_slug": "<pack_slug>",
  "command_namespace": "<command_namespace>",
  "python_distribution": "watchtower-<pack_slug>",
  "python_package": "watchtower_<pack_slug>",
  "integration_module": "watchtower_<pack_slug>.integration",
  "declared_capabilities": [
    "command_registration",
    "query_runtime",
    "sync_targets",
    "validation_provider"
  ],
  "required_validation_suite_ids": [
    "suite.<pack_slug>.validation_baseline"
  ],
  "owned_roots": {
    "workspace_root": "<pack_root>",
    "machine_root": "<pack_root>/.wt",
    "docs_root": "<pack_root>/docs",
    "workflows_root": "<pack_root>/workflows",
    "tracking_root": "<pack_root>/tracking",
    "python_root": "<pack_root>/python",
    "domain_roots": {}
  }
}
```

- Keep `pack_id`, `pack_slug`, `command_namespace`, `python_distribution`, and `python_package` aligned with the shared `pack_registry.json` entry.
- Keep `integration_module` under the declared `python_package`.
- Keep `owned_roots` aligned with the roots declared in `pack_settings.json`.
- Only keep legacy `initiatives_root` or `projects_root` fields when the pack runtime still depends on them.

### Minimum `integration.py`
The smallest useful integration module exports one typed `PACK_INTEGRATION` with the four required capabilities.

| Hook | Why It Is Required |
|---|---|
| `command_registration` | Gives the host a pack-owned namespace registrar |
| `query_runtime` | Declares the pack query command inventory |
| `sync_targets` | Declares the pack sync target inventory |
| `validation_provider` | Supplies pack-owned validation hooks |

- Keep `query_runtime` and `sync_targets` non-empty.
- Keep the registrar pack-owned even when the handler body is initially minimal.
- Put operator-facing namespace logic behind the pack CLI package rather than hard-wiring it in reusable core.

### Building Additional Pack-Local Python
Add new pack-local Python when the behavior is truly domain-specific and does not belong in reusable core or host composition.

| Need | Canonical Location | Also Update |
|---|---|---|
| New domain workflow or lifecycle service | `<pack>/python/src/watchtower_<pack>/<feature>/service.py` | Pack docs, workflow docs, tests, and any new pack-owned surfaces |
| New pack query behavior | `<pack>/python/src/watchtower_<pack>/cli/query.py` or `<feature>/query.py` | `PACK_INTEGRATION.query_runtime`, command docs, tests |
| New pack sync target | `<pack>/python/src/watchtower_<pack>/sync/<feature>.py` | `PACK_INTEGRATION.sync_targets`, sync docs, tests |
| New domain-specific validation semantics | `<pack>/python/src/watchtower_<pack>/validation/` | `validation_provider`, validator coverage, tests |
| New rendered or reporting behavior | `<pack>/python/src/watchtower_<pack>/rendering/` or feature-owned module | Rendered surface declarations, templates, docs, tests |

- Prefer feature-owned folders such as `reviews/`, `targets/`, `bootstrap/`, `closeout/`, `rendering/`, or `sync/` over mirrored copies of reusable-core package families.
- If the behavior becomes generic across multiple packs, move it into `watchtower_core` instead of cloning helpers into each pack.
- If the behavior is about root parser construction, pack discovery, or dispatch, it belongs in `watchtower_host`, not the pack.
- Keep imports one-way: `watchtower_<pack>` may depend on `watchtower_core`, but it must not import `watchtower_host`.
- When new pack-local Python adds a new human or machine surface, extend `pack_settings.json`, `pack_runtime_manifest.json`, docs, workflows, and tests in the same change.

### Common Extension Sequence
1. Add or update the feature module under `<pack>/python/src/watchtower_<pack>/`.
2. Decide whether the feature changes only pack-local Python or also adds new pack-owned docs, workflows, tracking surfaces, or `domain_roots`.
3. Update `integration.py` if the feature changes namespace registration, query inventory, sync targets, or validation behavior.
4. Update the pack-owned namespace command docs if the operator-visible surface changed.
5. Run `watchtower-core pack validate --pack-settings-path <path> --format json`.
6. Run `watchtower-core pack describe --pack <slug> --format json`.
7. Prove at least one host-composed path still works, such as `watchtower-core <namespace> --help`.

### Hosted Pack Scaffold Command
```sh
cd core/python
uv run watchtower-core pack scaffold --pack-slug oversight --pack-root oversight --domain-root reviews --format json
```

- Use the command when you want the pack-owned starter files plus the exact shared-registry and workspace snippets needed to finish host wiring.
- The command intentionally does not mutate the shared pack registry or `core/python/pyproject.toml` automatically.
- Prefer a first-party root pack such as `oversight/` unless the repository is deliberately hosting multiple packs under `packs/<slug>/`.
- Follow scaffold with `watchtower-core pack bootstrap --pack-settings-path <path> --write --format json`.
- Use `--no-sync-workspace` only when a test fixture or staged refactor intentionally needs to defer `uv sync` and then run explicit validation afterward.

### Hosted Pack Bootstrap Command
```sh
cd core/python
uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --write --format json
```

- Use the command when you want one guarded operator path to update `pack_registry.json`, `core/python/pyproject.toml`, and immediate pack validation together.
- The command dry-runs by default, so you can inspect the shared changes before they land.
- The command validates the hosted pack after applying the shared wiring and restores the shared files if validation fails.

### Worked Comparison
| Concern | First-Party Root-Pack Shape | Nested Multi-Pack Shape |
|---|---|---|
| Primary domain work | Initiative, project, task, promotion, or closeout flows under a direct repository child pack root. | Review, assessment, evidence-heavy, or other domain flows under `packs/<slug>/`. |
| Shared dependency | `watchtower_core` contracts, loaders, validators, and shared helpers. | Same shared dependency set. |
| Host integration | One manifest plus one integration module loaded by the host. | Same host seam, different capabilities declared. |
| Pack-owned docs | `<pack>/docs/**` and `<pack>/workflows/**` under a first-party root pack. | `packs/<slug>/docs/**` and `packs/<slug>/workflows/**`. |

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
- `core/docs/templates/pack/` as the reusable starter surface for new pack roots
- `WatchTowerOversight` as a second-pack design reference for future capabilities and docs shape
- `core/python/tests/fixtures/python/watchtower_oversight_fixture/` as the repository’s synthetic second-pack source package for multi-pack contract tests
- `core/python/tests/integration/test_pack_externalization.py` as the externalized proof that both a first-party root pack and a second `oversight`-style pack can load from pack-owned `python/` roots

## References
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md)
- [argparse_subcommands_reference.md](/core/docs/references/argparse_subcommands_reference.md)
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md)

## Notes
- This reference captures the current hosted-pack contract and should move in lockstep with pack scaffolding, bootstrap, and validation behavior.
- Canonical upstream sources were reviewed on 2026-03-20 during the host-pack boundary hard-cutover tranche.
- Runtime-only discovered packs are expected during copied-core bring-up, but they do not replace the steady-state shared registry and shared workspace contract.

## Updated At
- `2026-03-23T23:20:00Z`
