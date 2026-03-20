---
id: "std.engineering.core_host_pack_python_boundary"
title: "Core Host Pack Python Boundary Standard"
summary: "This standard defines the required split between reusable core, host composition, and pack-native Python code for WatchTower packages."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "python_boundary"
  - "domain_pack"
owner: "repository_maintainer"
updated_at: "2026-03-20T23:40:00Z"
audience: "shared"
authority: "authoritative"
---

# Core Host Pack Python Boundary Standard

## Summary
This standard defines the required split between reusable core, host composition, and pack-native Python code for WatchTower packages.

## Purpose
Keep `watchtower_core`, `watchtower_host`, and `watchtower_<pack>` explicit enough that new domain packs can integrate through the same contract without reintroducing direct imports, pack-flavored mirrors of core, or repository-coupled hacks.

## Scope
- Applies to Python package code under `core/python/src/watchtower_core/`, `core/python/src/watchtower_host/`, and pack-owned package roots such as `plan/python/src/watchtower_plan/`.
- Covers dependency direction, command ownership, pack-owned runtime placement, and portability expectations.
- Does not redefine the lower-level schema details of the pack registry or pack runtime manifest; those belong to the pack-interface contract standard.

## Use When
- Introducing or refactoring reusable-core, host-runtime, or pack-runtime code.
- Deciding where a new CLI registrar, validation hook, lifecycle service, or query helper belongs.
- Reviewing whether a pack is externalizable without code rewrites.

## Related Standards and Sources
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md): provides the lower-level Python design rules that must stay consistent with this boundary split.
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): defines the workspace and package-root layout that this boundary standard specializes.
- [domain_pack_authoring_standard.md](/core/docs/standards/engineering/domain_pack_authoring_standard.md): applies this boundary model to the shape and responsibilities of an individual hosted pack.
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): governs the machine contracts that connect these three layers at runtime.
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md): gives the worked pack-authoring examples that motivated this reusable boundary.
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md): distills the primary-source plugin-discovery guidance behind the host-owned composition model.
- [argparse_subcommands_reference.md](/core/docs/references/argparse_subcommands_reference.md): supports the namespaced subcommand structure used by the host-composed CLI.

## Guidance
- `watchtower_core` owns reusable loaders, schemas, typed contracts, validators, shared query or sync helpers, rebuild helpers, routing, workflow execution, evidence, and other pack-agnostic runtime behavior.
- `watchtower_host` owns CLI parser construction, pack discovery, pack registration, command dispatch, and other composition logic that joins reusable core with one or more hosted packs.
- `watchtower_<pack>` owns pack-native orchestration, pack-native command registration, pack-native lifecycle behavior, pack-native rendering, and pack-native semantic validation rules.
- `watchtower_core` must not import `watchtower_plan` or any future `watchtower_<pack>`.
- `watchtower_<pack>` must not import `watchtower_host`.
- The host is the only layer allowed to compose reusable core with pack runtime.
- Packs must depend on `watchtower_core` contracts, not on host internals or repo-local `sys.path` mutation.
- Keep packs feature-owned. Prefer modules such as `bootstrap`, `initiatives`, `projects`, `tasks`, `promotion`, `closeout`, and `rendering` over mirrored infra-family package trees.
- Keep pack-native command docs, workflows, and durable guidance under the owning pack root instead of shared core docs when the command or behavior is pack-specific.

## Structure or Data Model
### Dependency direction
| Layer | Allowed Imports | Forbidden Imports | Primary Role |
|---|---|---|---|
| `watchtower_core` | stdlib, third-party libs, `watchtower_core.*` | `watchtower_host`, any `watchtower_<pack>` | Reusable runtime and contracts |
| `watchtower_host` | `watchtower_core`, declared `watchtower_<pack>` integrations | reverse host imports from packs | Host composition and CLI dispatch |
| `watchtower_<pack>` | `watchtower_core`, same-pack modules | `watchtower_host` | Pack-native runtime |

### Ownership checkpoints
| Concern | Canonical Owner | Notes |
|---|---|---|
| Pack registry and runtime-manifest schemas | `watchtower_core` | Shared contract surfaces |
| CLI entrypoint and parser tree | `watchtower_host` | Shared binary, composed behavior |
| Pack namespace command registration | owning pack | Loaded through the host |
| Pack lifecycle orchestration | owning pack | Must not live in reusable core |
| Shared query or validation helpers | `watchtower_core` | Extract before growing pack sprawl |

## Operationalization
- `Modes`: `documentation`; `artifact`; `workflow`
- `Operational Surfaces`: `core/python/src/watchtower_core/`; `core/python/src/watchtower_host/`; `plan/python/src/watchtower_plan/`; `core/workflows/modules/domain_pack_integration.md`; `core/workflows/modules/pack_interface_validation.md`

## Validation
- Reviewers should reject new `watchtower_core -> watchtower_<pack>` imports.
- Reviewers should reject new `watchtower_<pack> -> watchtower_host` imports.
- Pack-native command registration should route through the host-pack contract, not flat root-command wiring in reusable core.
- Pack portability checks should fail when a pack requires hidden repository-only Python import tricks.

## Change Control
- Update this standard when the repository changes the core-host-pack split, allowed dependency direction, or command ownership model.
- Update the companion Python workspace, Python code-design, pack-interface, and domain-pack authoring standards in the same change set when this standard changes materially.
- Update package READMEs, AGENTS files, and affected workflow modules in the same change set when contributor-facing expectations change.

## References
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md)
- [argparse_subcommands_reference.md](/core/docs/references/argparse_subcommands_reference.md)

## Notes
- This standard locks the three-layer model even when only one hosted pack currently exists.
- The stable CLI binary name may remain `watchtower-core` even when the owning Python package is `watchtower_host`.

## Updated At
- `2026-03-20T23:40:00Z`
