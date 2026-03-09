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
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# pyproject.toml Reference

## Summary
This document provides a working reference for `pyproject.toml` as the preferred home for Python project metadata and tool configuration when Python automation is added to this repo.

## Purpose
Provide a single configuration baseline so packaging metadata and tool settings do not drift across multiple files without clear reason.

## Scope
- Covers the role of `pyproject.toml` in Python packaging and tool configuration.
- Does not require Python tooling unless the repo actually starts using it.

## Canonical Upstream
- `https://packaging.python.org/en/latest/specifications/pyproject-toml/` - verified 2026-03-09; pyproject.toml specification.
- `https://packaging.python.org/en/latest/guides/writing-pyproject-toml/` - verified 2026-03-09; Writing your pyproject.toml.
- `https://peps.python.org/pep-0518/` - verified 2026-03-09; PEP 518 – Specifying Minimum Build System Requirements for Python Projects.
- `https://peps.python.org/pep-0621/` - verified 2026-03-09; PEP 621 – Storing project metadata in pyproject.toml.

## Related Standards and Sources
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Prefer one canonical `pyproject.toml` over scattering Python tool configuration across many files.
- Keep project metadata in `[project]` when packaging metadata is needed.
- Put tool-specific settings under `[tool.<name>]`.
- Avoid duplicating the same setting in multiple config files.
- Keep comments and structure clear enough that contributors can find the relevant tool section quickly.

### Common Sections
| Section | Use For | Notes |
|---|---|---|
| `[build-system]` | Build backend requirements | Needed when packaging or building distributions. |
| `[project]` | Package metadata and dependencies | Use when the repo becomes a Python package. |
| `[tool.pytest.ini_options]` | pytest configuration | Good default home for test settings. |
| `[tool.ruff]` | Ruff configuration | Keep lint settings centralized when Ruff is used. |
| `[tool.mypy]` | mypy configuration | Use when static type checking is adopted. |

### Common Pitfalls
- Spreading tool configuration across multiple files without a strong reason.
- Treating `[project]` as a dumping ground for settings that belong under `[tool.<name>]`.
- Forgetting to keep tool choices and config layout aligned.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)

### Why It Matters Here
- Use this reference if repository automation adopts shared Python tooling and needs one canonical configuration file.
- Pair it with `pytest`, `Ruff`, and `mypy` references when deciding where their local settings should live.
- Use it with packaging and `src/` layout guidance if the repository becomes an installable Python project.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)

## Notes
- This reference is intentionally practical rather than exhaustive.
- If the repo never adopts Python tooling, this reference remains optional background material.
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
