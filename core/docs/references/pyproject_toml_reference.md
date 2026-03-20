---
id: "ref.pyproject_toml"
title: "pyproject.toml Reference"
summary: "Working reference for centralizing Python project metadata and tool configuration in this repository."
type: "reference"
status: "active"
tags:
  - "reference"
  - "pyproject_toml"
owner: "repository_maintainer"
updated_at: "2026-03-20T17:12:07Z"
audience: "shared"
authority: "reference"
---

# pyproject.toml Reference

## Summary
This document provides a working reference for `pyproject.toml` as the preferred home for Python project metadata, console scripts, and Python tool configuration in this repository.

## Purpose
Provide a single configuration baseline so Python package metadata, console entrypoints, and tool settings do not drift across multiple files without clear reason.

## Scope
- Covers the role of `pyproject.toml` in Python packaging and tool configuration.
- Covers how scripts and entry-point groups interact with local package layout and host-pack integration.
- Does not by itself define the repository's pack integration contract.

## Canonical Upstream
- `https://packaging.python.org/en/latest/specifications/pyproject-toml/` - verified 2026-03-20; pyproject.toml specification.
- `https://packaging.python.org/en/latest/guides/writing-pyproject-toml/` - verified 2026-03-20; Writing your pyproject.toml.
- `https://peps.python.org/pep-0518/` - verified 2026-03-20; PEP 518 – Specifying Minimum Build System Requirements for Python Projects.
- `https://peps.python.org/pep-0621/` - verified 2026-03-20; PEP 621 – Storing project metadata in pyproject.toml.

## Related Standards and Sources
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md): constrains how packaging configuration changes should stay aligned with Python module ownership.
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): defines the repository package layout that the `pyproject.toml` configuration must represent.
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): depends on explicit distribution and import-name metadata that packaging config must keep stable.
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md): builds on these packaging rules when evaluating plugin discovery choices.
- [pyproject.toml](/core/python/pyproject.toml): is the live repository configuration surface this reference is interpreting.

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Prefer one canonical `pyproject.toml` over scattering Python tool configuration across many files.
- Keep project metadata in `[project]` when packaging metadata is needed.
- Put tool-specific settings under `[tool.<name>]`.
- Use `[project.scripts]` for stable console commands such as `watchtower-core`.
- Use `[project.entry-points]` only when you intentionally need install-time plugin advertisement; do not hide the primary repo pack contract there.
- Treat package metadata as packaging truth, not as a substitute for governed repo manifests.
- Avoid duplicating the same setting in multiple config files.
- Keep comments and structure clear enough that contributors can find the relevant tool section quickly.

### Common Sections
| Section | Use For | Notes |
|---|---|---|
| `[build-system]` | Build backend requirements | Needed when packaging or building distributions. |
| `[project]` | Package metadata and dependencies | Use when the repo becomes a Python package. |
| `[project.scripts]` | Console entrypoints | Best place for the stable CLI binary mapping. |
| `[project.entry-points]` | Plugin groups | Useful for optional external adapters, not required for repo-governed manifests. |
| `[tool.pytest.ini_options]` | pytest configuration | Good default home for test settings. |
| `[tool.ruff]` | Ruff configuration | Keep lint settings centralized when Ruff is used. |
| `[tool.mypy]` | mypy configuration | Use when static type checking is adopted. |

### Packaging and Runtime Decisions
| Question | Preferred Answer | Why |
|---|---|---|
| Where should the CLI binary be declared? | `[project.scripts]` in the host package. | Console script ownership belongs to packaging metadata. |
| Where should repo pack integration be declared? | Governed manifests in the repo. | Repo validation should not depend only on installation metadata. |
| Should all pack wiring live in `[project.entry-points]`? | No. | That makes monorepo validation and review less explicit. |
| What should `[project]` say about import ownership? | Name the distribution accurately and keep importable package boundaries clear. | Avoid confusion between distribution names and Python import names. |

### Common Pitfalls
- Spreading tool configuration across multiple files without a strong reason.
- Treating `[project]` as a dumping ground for settings that belong under `[tool.<name>]`.
- Confusing the distribution name with the import package name.
- Making plugin or pack integration depend only on install-time metadata when repo-governed validation is required.
- Forgetting to keep tool choices and config layout aligned.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/core/python/pyproject.toml)

### Why It Matters Here
- Use this reference for the shared Python workspace and any host-owned console entrypoint.
- Pair it with `pytest`, `Ruff`, and `mypy` references when deciding where their local settings should live.
- Use it with packaging and `src/` layout guidance when a reusable core package, host package, or domain pack package is installable.
- Use it with the plugin-discovery reference when deciding which integration details belong in packaging metadata versus governed repo manifests.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/core/python/pyproject.toml)

## Notes
- This reference is intentionally practical rather than exhaustive.
- Canonical upstream sources were rechecked on `2026-03-20` during the host-pack boundary hard-cutover pass.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-20T17:12:07Z`
