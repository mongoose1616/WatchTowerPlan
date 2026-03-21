---
id: "std.data_contracts.pack_interface_contract"
title: "Pack Interface Contract Standard"
summary: "This standard defines the governed machine contracts that connect hosted packs to reusable core and host composition."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "pack_interface"
owner: "repository_maintainer"
updated_at: "2026-03-21T21:05:00Z"
audience: "shared"
authority: "authoritative"
---

# Pack Interface Contract Standard

## Summary
This standard defines the governed machine contracts that connect hosted packs to reusable core and host composition.

## Purpose
Make hosted-pack discovery, validation, and runtime wiring deterministic and fail-closed by governing the pack registry, pack runtime manifest, and typed integration hooks explicitly.

## Scope
- Applies to the hosted-pack registry, pack runtime manifests, typed pack integration descriptors, and pack-interface validation behavior.
- Covers required fields, ownership boundaries, and validation expectations.
- Does not redefine pack-internal business logic or human-facing pack workflow content.

## Use When
- Adding or changing a hosted pack.
- Updating `pack_registry`, `pack_runtime_manifest`, or typed pack-integration hooks.
- Reviewing whether a pack is valid, importable, and portable.

## Related Standards and Sources
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md): defines the dependency-direction and ownership boundaries that this machine contract must reinforce.
- [domain_pack_authoring_standard.md](/core/docs/standards/engineering/domain_pack_authoring_standard.md): constrains what a hosted pack must publish and own beyond the registry and manifest fields.
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md): requires pack-interface drift to fail closed in the normal repository validation loop.
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md): captures the primary-source plugin-discovery tradeoffs behind the declarative manifest approach.
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md): records packaging and metadata constraints that shape the explicit distribution and import-name fields.

## Guidance
- Keep hosted-pack discovery declarative and schema-backed.
- `pack_settings` remains the pack load-root contract for owned surfaces and defaults.
- `pack_runtime_manifest` owns Python integration declarations, command namespace, declared capabilities, and owned runtime roots.
- `pack_registry` is the shared hosted-pack inventory used by host composition and validation.
- Keep manifest and registry paths repository-relative and portable. Absolute paths and parent traversal are invalid hosted-pack contract input.
- Keep `pack_settings.json` and `pack_runtime_manifest.json` directly under the declared `machine_root/manifests/` directory.
- Validate machine contracts before importing any pack integration module.
- Declare one integration module exporting one typed `PACK_INTEGRATION` descriptor per hosted pack.
- Keep `integration_module` under the declared `python_package`; host composition must not reach sideways into unrelated packages.
- `query_runtime` must return a typed query runtime describing the pack-owned query command surface.
- `sync_targets` must return a typed sync runtime describing the pack-owned sync target surface.
- Keep command namespaces unique across the hosted-pack registry.
- Keep pack-settings surfaces pack-local unless they intentionally point at shared core control-plane authority under `core/control_plane/`.
- Keep each pack namespace's command docs under the pack-owned docs root and publish the namespace entry page at `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md`.
- Let pack-interface validation scan live source roots when they exist so reusable core cannot import a hosted pack and a hosted pack cannot import host composition.
- Do not hide primary hosted-pack discovery behind Python entry points or naming conventions alone.
- Use `domain_roots` for optional pack-specific roots beyond the shared workspace roots. Legacy plan-specific `initiatives_root` and `projects_root` remain allowed only where the current plan runtime still depends on them, and they must agree with `domain_roots` when both are present.

## Structure or Data Model
### Required machine contracts
| Surface | Canonical Owner | Purpose |
|---|---|---|
| `core/control_plane/registries/pack_registry.json` | shared core | Hosted-pack inventory for discovery and validation |
| `<pack>/.wt/manifests/pack_settings.json` | owning pack | Pack load roots, validation defaults, governed surfaces |
| `<pack>/.wt/manifests/pack_runtime_manifest.json` | owning pack | Host-facing runtime manifest |
| `watchtower_<pack>.integration.PACK_INTEGRATION` | owning pack Python package | Typed runtime descriptor |

### Required runtime-manifest fields
| Field | Requirement | Notes |
|---|---|---|
| `pack_id`, `pack_slug` | Required | Must match registry and pack settings |
| `command_namespace` | Required | Must be unique across hosted packs |
| `python_distribution`, `python_package` | Required | Distribution and import names must be explicit |
| `integration_module` | Required | Import string for the typed pack descriptor |
| `declared_capabilities` | Required | Must align with the integration descriptor hooks |
| `owned_roots` | Required | Must match the owning pack roots |
| `owned_roots.domain_roots` | Optional | Names optional pack-specific roots such as `reviews`, `assessments`, or `targets` |
| `required_validation_suite_ids` | Required | Used by pack-interface validation |

### Required validation checks
| Check | Expected Result |
|---|---|
| Schema validity | Pass |
| Registry-manifest field parity | Pass |
| Integration module import | Pass |
| Typed descriptor export | Pass |
| Declared capability hooks present | Pass |
| Validation-provider runtime shape | Pass |
| Query-runtime command set shape | Pass |
| Sync-runtime target set shape | Pass |
| Owned-root consistency | Pass |
| Owned-root existence and pack-local placement | Pass |
| Manifest path parity with `machine_root` | Pass |
| Pack-settings surface locality | Pass |
| Integration module stays under `python_package` | Pass |
| Named `domain_roots` parity across settings and runtime manifest | Pass |
| Pack namespace command-doc entry page present | Pass |
| Required validation suites present | Pass |
| Dependency-direction scan across core, host, and pack source roots | Pass |

## Operationalization
- `Modes`: `artifact`; `validation`; `runtime`
- `Operational Surfaces`: `core/control_plane/registries/pack_registry.json`; `plan/.wt/manifests/pack_runtime_manifest.json`; `core/python/src/watchtower_core/pack_integration/`; `core/python/src/watchtower_core/validation/pack_contract.py`; `plan/docs/commands/core_python/`

## Validation
- `watchtower-core validate all` should fail closed on pack-interface contract drift.
- `watchtower-core validate all` and `watchtower-core pack validate --pack <slug>` should fail closed when live source roots contain forbidden `watchtower_core -> watchtower_<pack>` or `watchtower_<pack> -> watchtower_host` imports.
- Reviewers should reject hosted-pack changes that update only Python hooks or only manifests without the companion governed artifacts.
- Reviewers should reject command namespace collisions, missing declared hooks, or pack manifests that point at non-existent roots.
- Reviewers should reject pack manifests that point pack-owned command docs back at shared core docs or omit the pack namespace command page entirely.
- Reviewers should reject pack manifests or pack-settings surfaces that use absolute paths, parent traversal, or non-pack-local paths outside `core/control_plane/`.
- Reviewers should reject runtime manifests whose integration module falls outside the declared pack python package.

## Change Control
- Update this standard when the hosted-pack registry shape, runtime-manifest contract, or required validation behavior changes materially.
- Update pack schemas, validators, local references, and workflow modules in the same change set when the contract changes.

## References
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md)
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)

## Notes
- Entry points may exist as a later adapter, but they are not the primary hosted-pack contract.
- The machine contract is intentionally explicit so pack discovery remains reviewable and portable.

## Updated At
- `2026-03-21T21:05:00Z`
