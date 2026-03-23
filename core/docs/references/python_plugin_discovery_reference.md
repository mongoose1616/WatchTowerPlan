---
id: "ref.python_plugin_discovery"
title: "Python Plugin Discovery Reference"
summary: "Distilled reference for choosing plugin discovery patterns for host-pack integration in this repository."
type: "reference"
status: "active"
tags:
  - "reference"
  - "python"
  - "plugins"
owner: "repository_maintainer"
updated_at: "2026-03-20T17:12:07Z"
audience: "shared"
authority: "reference"
---

# Python Plugin Discovery Reference

## Summary
This reference distills the Python packaging guidance that matters when this repository needs one reusable host runtime to discover and compose multiple domain packs.

## Purpose
Keep plugin-discovery decisions explicit so pack integration does not drift into ad hoc imports, hidden path coupling, or host-specific assumptions that break pack portability.

## Scope
- Covers the main Python plugin discovery patterns described by PyPA and how they apply to this repository.
- Covers how those patterns interact with host-owned CLI composition and pack-owned runtime packages.
- Does not define this repository's final pack contract by itself; that policy belongs in the companion standards.

## Canonical Upstream
- `https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/` - PyPA guide on plugin discovery patterns.
- `https://docs.python.org/3/library/importlib.metadata.html` - Python standard-library reference for package metadata and entry points.
- `https://packaging.python.org/en/latest/specifications/pyproject-toml/` - `pyproject.toml` specification for scripts and entry-point declarations.

## Related Standards and Sources
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md): captures the packaging metadata surfaces that plugin discovery strategies rely on.
- [argparse_subcommands_reference.md](/core/docs/references/argparse_subcommands_reference.md): complements discovery guidance with the CLI tree shape needed once packs are loaded.
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): turns the selected discovery model into an explicit governed contract.
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md): anchors the chosen discovery model inside the repository’s layer boundaries.
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md): constrains where discovery helpers and pack adapters should live in Python code.
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): constrains where the host runtime, pack code, and packaging metadata live in the workspace.

## Quick Reference or Distilled Reference
### Discovery Modes
| Mode | How It Works | Strengths | Weaknesses | Fit Here |
|---|---|---|---|---|
| Naming convention | Scan installed modules for a prefix pattern. | Simple for public ecosystems. | Brittle, global, and hard to validate deterministically. | Poor fit for governed host-pack wiring. |
| Namespace package | Discover implementations under one shared namespace. | Useful for large extension ecosystems. | Couples package layout to extension strategy and complicates copy-out portability. | Acceptable only as a future adapter, not the primary contract. |
| Entry points | Resolve advertised plugins from installed package metadata. | Standardized discovery for separately installed distributions. | Resolution depends on package installation state and metadata rather than repo-governed artifacts. | Good future adapter for external packages, but not the primary monorepo contract. |
| Repo-governed manifest | Host loads pack manifests from governed artifacts, then imports the declared integration module. | Deterministic, reviewable, validator-friendly, and portable inside this repo. | Requires repository-owned schema, validation, and manifest discipline. | Preferred primary contract here. |

### Rules or Decision Points
- Use governed manifest discovery as the primary contract when the repository already has schema-backed control-plane governance.
- Treat Python entry points as optional compatibility adapters for externally installed packs, not as the authoritative source of truth for hosted packs.
- Keep pack discovery declarative and validator-visible. Hidden import wiring inside CLI code is the failure mode to avoid.
- Separate pack discovery from pack load roots. `pack_settings` should define workspace and governed-surface roots, while runtime integration details belong in a distinct runtime manifest.
- Discover packs before command registration so namespace collisions and missing hooks fail before dispatch time.

### Decision Table
| Question | Preferred Answer | Why |
|---|---|---|
| What should the host validate first? | Repo-governed pack registry and pack runtime manifest. | Validation can fail before Python import side effects. |
| What should the host import after manifest validation? | One declared integration module exporting one typed descriptor. | Keeps the runtime seam explicit and testable. |
| Should the host scan Python packages heuristically? | No. | Heuristic scanning hides contract drift and weakens portability. |
| Should entry points disappear entirely? | No, but treat them as a later adapter. | External pack installation may still benefit from standard Python metadata. |

### Pitfalls and Failure Modes
- Importing pack modules directly from reusable core creates a hard architectural dependency that prevents reuse.
- Treating entry points as the only source of truth hides missing repo-governed surfaces and makes review harder.
- Letting packs self-register commands implicitly at import time makes command coverage and collision checks harder to validate.
- Mirroring host or core package taxonomy inside every pack increases sprawl without improving extensibility.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [pyproject.toml](/core/python/pyproject.toml)
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)

### Why It Matters Here
- The repository is moving from direct reusable-core to pack imports toward a reusable core plus host-composition model.
- This reference supports the decision to make a governed pack manifest the primary integration contract instead of relying on implicit imports or Python packaging metadata alone.
- It also preserves a clean path to later add an entry-point adapter for copied-out packs without changing the internal contract.

### If Local Policy Tightens
- Update the companion Python-boundary standard, pack-manifest standard, validation standard, and CLI command docs in the same slice.
- Update any host-runtime workflow modules and pack-authoring references when the chosen discovery mechanism or allowed adapters change.

## Process or Workflow
1. Choose the authoritative discovery surface first: governed repo manifest or external adapter.
2. Validate the governed surfaces before importing any pack integration module.
3. Import one integration module and resolve typed hooks from that module rather than scattering direct pack imports across the host.

## Examples
- Host-owned pack registry listing one discovered pack and pointing to that pack's runtime manifest.
- Pack-owned runtime manifest naming one integration module such as `watchtower_<pack>.integration`.

## References
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md)
- [argparse_subcommands_reference.md](/core/docs/references/argparse_subcommands_reference.md)

## Notes
- Canonical upstream sources were reviewed on 2026-03-20 during the host-pack boundary hard-cutover tranche.
- PyPA documents multiple legitimate plugin discovery patterns. This repository narrows those choices because it values governed artifacts, deterministic validation, and pack portability.

## Updated At
- `2026-03-20T17:12:07Z`
