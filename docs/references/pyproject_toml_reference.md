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
updated: "2026-03-08"
audience: "shared"
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
- `https://packaging.python.org/specifications/declaring-project-metadata/`
- `https://packaging.python.org/guides/writing-pyproject-toml/`
- `https://peps.python.org/pep-0518/`
- `https://peps.python.org/pep-0621/`

## Related Standards and Sources
- `pyproject.toml` Python packaging specification
- `docs/standards/engineering/` once formal engineering standards are written.

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
- Use this reference if repository automation adopts shared Python tooling and needs one canonical configuration file.
- Pair it with `pytest`, `Ruff`, and `mypy` references when deciding where their local settings should live.
- Use it with packaging and `src/` layout guidance if the repository becomes an installable Python project.

## Process or Workflow
1. Decide whether the repository needs shared Python tooling or packaging metadata.
2. Centralize Python tool configuration in `pyproject.toml` unless a tool has a strong reason to live elsewhere.
3. If `pyproject.toml` structure becomes a repository standard, move the normative rule into `docs/standards/engineering/**` and keep this file as supporting reference context.

## References
- `pyproject.toml` Python packaging specification
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This reference is intentionally practical rather than exhaustive.
- If the repo never adopts Python tooling, this reference remains optional background material.

## Last Synced
- `2026-03-08`
