---
id: "std.engineering.hosted_pack_integration"
title: "Hosted Pack Integration Standard"
summary: "This standard defines the minimum surfaces and extension rules a hosted pack must satisfy to integrate with reusable core and host composition."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "hosted_pack"
  - "integration"
owner: "repository_maintainer"
updated_at: "2026-04-04T21:20:00Z"
audience: "shared"
authority: "authoritative"
---

# Hosted Pack Integration Standard

## Summary
This standard defines the minimum developer-facing surface set and extension rules a hosted pack must satisfy to integrate with reusable core and host composition.

## Purpose
Make hosted-pack onboarding, extension, and review predictable by stating the smallest acceptable pack shape in one place instead of forcing contributors to reconstruct it from schemas, validators, templates, and scattered standards.

## Scope
- Applies to hosted pack roots such as `<pack>/` that are registered through the shared host runtime.
- Covers the minimum pack-owned files, required shared registration surfaces, and the rules for growing additional pack-local Python.
- Does not replace the lower-level machine-contract schemas or the reusable-core versus host boundary rules.

## Use When
- Creating a new hosted pack.
- Explaining to a contributor what surfaces a pack must publish before bootstrap or validation.
- Adding new pack-local Python behavior after the starter pack already exists.
- Reviewing whether a pack extension belongs in `watchtower_core`, `watchtower_host`, or `watchtower_<pack>`.

## Related Standards and Sources
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): defines the machine contracts and validation checks this standard summarizes for developers.
- [domain_pack_authoring_standard.md](/core/docs/standards/engineering/domain_pack_authoring_standard.md): governs the broader pack-owned root shape and packaging expectations.
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md): defines the donor-neutral bootstrap and release-scrub contract that sits above integration wiring.
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md): defines the dependency direction and ownership split between reusable core, host composition, and pack-native Python.
- [deterministic_sync_cache_standard.md](/core/docs/standards/engineering/deterministic_sync_cache_standard.md): defines the runtime cache contract pack-owned deterministic sync services should reuse.
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md): gives the practical checklist, worked file set, and extension guidance that operationalize this standard.
- [core/docs/templates/pack/README.md](/core/docs/templates/pack/README.md): provides the starter templates that should remain aligned with this minimum contract.

## Guidance
- Treat hosted-pack integration as a cross-surface contract. A pack is not considered integrated when only its Python package exists or only its manifests exist.
- The minimum pack-owned roots are `<pack>/.wt/`, `<pack>/docs/`, `<pack>/workflows/`, `<pack>/tracking/`, and `<pack>/python/`.
- The minimum pack-owned file set is:

| Surface | Required Role |
|---|---|
| `<pack>/.wt/manifests/pack_settings.json` | Pack load root for declared surfaces and defaults |
| `<pack>/.wt/manifests/pack_runtime_manifest.json` | Host-facing runtime contract |
| `<pack>/.wt/registries/workflow_metadata_registry.json` | Pack-owned workflow retrieval metadata when the pack publishes workflow IDs beyond the shared core registry |
| `<pack>/python/pyproject.toml` | Pack packaging and install surface |
| `<pack>/python/src/watchtower_<pack>/__init__.py` | Pack package root |
| `<pack>/python/src/watchtower_<pack>/integration.py` | Typed `PACK_INTEGRATION` export |
| `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md` | Pack namespace command-doc entry page |

- The minimum shared integration surfaces are:

| Surface | Required Role |
|---|---|
| `core/control_plane/registries/pack_registry.json` entry | Registers the pack with host discovery |
| `core/python/pyproject.toml` hosted-pack registration | Installs the pack into the shared Python workspace |

- `pack_settings.json` must be both schema-valid and runtime-loadable. At minimum it must declare:

| Field or Surface | Requirement |
|---|---|
| `pack_id` | Must match the runtime manifest and registry entry |
| `workspace_roots.workspace_root` | Pack root |
| `workspace_roots.machine_root` | `<pack>/.wt` |
| `workspace_roots.docs_root` | `<pack>/docs` |
| `workspace_roots.workflows_root` | `<pack>/workflows` |
| `workspace_roots.tracking_root` | `<pack>/tracking` |
| `workspace_roots.overview_path` | Pack overview or equivalent rendered entry path |
| `default_validation_suite_id` | Pack validation baseline |
| `surfaces.schema_catalog` | Required runtime surface |
| `surfaces.validator_registry` | Required runtime surface |
| `surfaces.validation_suite_registry` | Required runtime surface |
| `surfaces.workflow_metadata_registry` | Starter runtime surface for pack-owned workflow IDs; the loader merges it with the shared core workflow metadata registry |

- Treat activated `pack_settings.json` plus the merged shared and pack-owned registries as the only reusable shared-core contract for pack-aware assertions. Shared-core tests, docs, and workflow guidance may use the current repository pack as an example, but they must derive runtime expectations from the active pack contract instead of hard-coding one donor repository's validator IDs, rendered surfaces, workflow IDs, or tracking filenames.
- `pack_runtime_manifest.json` must declare `pack_id`, `pack_slug`, `command_namespace`, `python_distribution`, `python_package`, `integration_module`, `declared_capabilities`, `owned_roots`, and `required_validation_suite_ids`.
- `owned_roots` must match the pack-owned roots declared in `pack_settings.json`, and optional `domain_roots` should be used for pack-specific roots such as `reviews`, `assessments`, or `targets`.
- The integration module must live under the declared `python_package` and export one typed `PACK_INTEGRATION`.
- Required capabilities are `command_registration`, `query_runtime`, `sync_targets`, and `validation_provider`.
- Declare optional `export_cleanup` only when the pack needs pack-owned customer-release scrub logic that reusable core cannot infer generically. The hook should remove pack-local live history from staged exports and rebuild any required clean derived surfaces when shared core is present.
- `query_runtime` and `sync_targets` must publish non-empty command and target inventories.
- Keep pack-local validator registries limited to pack-owned validators. Shared core validator IDs belong in `core/control_plane/registries/validator_registry.json`; conflicting duplicates should be treated as contract drift.
- When a pack publishes workflow IDs that are not already described by the shared core workflow metadata registry, keep those entries in a pack-owned `workflow_metadata_registry` and point `pack_settings.json` at that pack-local path. The loader merges the shared core registry with the pack-owned registry and rejects conflicting duplicates.
- Treat effective pack activation as mandatory Phase 0 for any pack-aware runtime, validation, sync, or host helper. Runtime-manifest and integration loading must not guess the default pack independently of the loader-owned activation step.
- Require the full typed `PackContext` only in seams that actually consume pack-governed surfaces beyond runtime identity. Minimal runtime-only fixture packs may omit governance surfaces such as `governance_surface_map`, `path_pattern_registry`, or `status_registry` while still remaining valid for runtime-manifest and integration proofs.
- Additional pack-local Python must live under `<pack>/python/src/watchtower_<pack>/` and should be organized by domain feature rather than by mirrored copies of reusable-core package taxonomy.
- Use `watchtower_<pack>` for domain-specific lifecycle behavior, rendering, semantic validation, query handlers, sync targets, and feature services.
- Move code into `watchtower_core` when the behavior is truly cross-pack, schema-backed, or pack-agnostic.
- Reuse shared documentation, standard-parsing, and workflow-index helpers from `watchtower_core` instead of copying donor implementations into pack-local helper modules.
- Keep CLI parser construction, root command-family composition, pack discovery, and dispatch in `watchtower_host`; pack code must not import `watchtower_host`.
- Keep optional operational runtime outputs such as telemetry under `<pack>/.wt/runtime/` so they remain pack-local machine state rather than shared-core authority.
- Keep pack-owned deterministic sync cache manifests under `<pack>/.wt/runtime/sync_cache/` and out of `core/control_plane/` or other authored authority roots.
- When a pack publishes deterministic document sync services, implement `sync_cache_inputs()` and reuse the shared `watchtower_core.sync.cache` contract instead of inventing a pack-specific cache format.
- When new pack-local Python introduces new machine or human surfaces, update the companion manifests, command docs, workflows, tracking surfaces, domain-root declarations, and tests in the same change set.
- Prefer `watchtower-core pack scaffold` to create pack-owned starter surfaces and `watchtower-core pack bootstrap` to update the shared registry and shared workspace registration together.
- Treat copied-core adoption as source transfer plus explicit reconciliation. Do not copy donor `.venv`, local editable-install metadata, caches, or pack `.wt/runtime/**` outputs and expect them to be part of the hosted-pack contract.
- Treat `pack bootstrap` as shared wiring reconciliation, not as a customer-release scrub. Donor retained records, tests, fixture packs, internal assessments, and other repo-local history still need explicit exclusion from portable output.
- Treat `pack export --pack-only` as an additive pack-bundle flow. It intentionally omits shared core and therefore defers shared registry and shared workspace validation until the bundle is copied into a compatible core repository and bootstrapped there.
- Expect `watchtower-core pack bootstrap --write` to reconcile the shared hosted-pack registry, shared workspace registration, the shared command, repository-path, reference, standard, workflow, and route discovery indexes when the hosted-pack set changes, and to run the pack-local `sync all` slice when the selected pack declares it and the workspace is ready.

## Structure or Data Model
### Additional pack-local Python ownership rules
| Need | Canonical Owner | Expected Follow-up |
|---|---|---|
| Domain-specific lifecycle, queries, sync targets, rendering, or validation semantics | `watchtower_<pack>` | Update pack docs, pack manifests, tests, and any new pack-owned surfaces |
| Reusable loader, validator, schema helper, registry helper, or generic harness behavior | `watchtower_core` | Keep the public boundary pack-agnostic and update shared tests |
| CLI root parser composition, command-family registration, pack discovery, or dispatch | `watchtower_host` | Keep packs consuming host contracts rather than importing host internals |

### Minimum validation proofs
| Proof | Expected Result |
|---|---|
| `watchtower-core pack validate --pack-settings-path <path>` | Pass |
| `watchtower-core pack describe --pack <slug>` | Reports importable integration and declared runtime details |
| Shared `core/python/pyproject.toml` registration | Hosted-pack dependency and `tool.uv.sources` entry present |
| Dependency-direction scan | No `watchtower_core -> watchtower_<pack>` imports and no `watchtower_<pack> -> watchtower_host` imports |

## Operationalization
- `Modes`: `documentation`; `runtime`; `validation`
- `Operational Surfaces`: `core/docs/references/domain_pack_authoring_reference.md`; `core/docs/templates/pack/`; `core/python/src/watchtower_core/pack_integration/`; `core/python/src/watchtower_core/validation/pack_contract.py`; `core/control_plane/registries/pack_registry.json`; `core/python/pyproject.toml`

## Validation
- Reviewers should reject packs that omit any required minimum surface from this standard.
- Reviewers should reject `pack_settings.json` surfaces that omit `schema_catalog`, `validator_registry`, or `validation_suite_registry`.
- Reviewers should reject packs that publish pack-owned workflow IDs without a pack-owned `workflow_metadata_registry` surface and authored registry file.
- Reviewers should reject pack-local validator or workflow metadata registries that copy shared core entries with conflicting content.
- Reviewers should reject runtime manifests or integration modules that declare the required capabilities without exporting the matching hooks.
- Reviewers should reject new pack-local Python that mirrors generic reusable-core package families without a real domain need.
- Reviewers should reject pack-local helper modules that fork generic standard, reference, or workflow parsing logic already exported by `watchtower_core`.
- `watchtower-core pack validate --pack <slug>` or `--pack-settings-path <path>` should pass before a pack is treated as integrated.
- Reviewers should reject bootstrap guidance that implies a raw donor repository snapshot is already customer-safe once shared host wiring passes.
- Reviewers should reject shared-core tests or docs that depend on a specific donor pack's named validator, workflow, authority, or rendered-surface entries when the same assertion should be derived from the activated pack contract.

## Change Control
- Update this standard when the minimum hosted-pack surface set, required capabilities, or pack-extension ownership rules change materially.
- Update [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md), [deterministic_sync_cache_standard.md](/core/docs/standards/engineering/deterministic_sync_cache_standard.md), [core/docs/templates/pack/README.md](/core/docs/templates/pack/README.md), pack templates, pack-interface schemas, and pack-contract validation in the same change set when the minimum contract changes materially.

## References
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md)
- [domain_pack_authoring_standard.md](/core/docs/standards/engineering/domain_pack_authoring_standard.md)
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md)

## Updated At
- `2026-04-04T21:20:00Z`
