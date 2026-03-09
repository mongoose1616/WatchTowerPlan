---
id: "ref.src_layout"
title: "src/ Layout Reference"
summary: "Working reference for the `src/` Python project layout in this repository."
type: "reference"
status: "active"
tags:
  - "reference"
  - "src_layout"
owner: "repository_maintainer"
updated: "2026-03-08"
audience: "shared"
---

# src/ Layout Reference

## Summary
This document provides a working reference for the `src/` layout when the repository needs installable or reusable Python packages.

## Purpose
Provide a simple layout baseline that keeps import behavior closer to installed reality and makes package boundaries clearer.

## Scope
- Covers when the `src/` layout is useful and what problem it solves.
- Does not require the repository to become a Python package if that is unnecessary.

## Canonical Upstream
- `https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/`

## Related Standards and Sources
- `src/` Python project layout guidance
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [pytest_reference.md](/home/j/WatchTowerPlan/docs/references/pytest_reference.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Prefer the `src/` layout when the repo has installable or reusable Python packages.
- Keep application code under `src/` and tests outside the package tree.
- Use the layout to make accidental local-import success less likely.
- Do not force `src/` onto tiny one-file scripts that do not benefit from packaging structure.
- Keep the package boundary obvious so imports, tests, and tooling stay predictable.

### Typical Shape

```text
src/
  package_name/
tests/
pyproject.toml
```

### Common Decisions
| Question | Preferred Direction | Notes |
|---|---|---|
| Does import parity matter? | Use `src/` | Helps match installed-package behavior. |
| Where should tests live? | `tests/` | Keep tests outside the package tree unless there is a strong reason not to. |
| Is packaging involved? | Pair with `pyproject.toml` | The layout is most useful when packaging or reusable modules exist. |

### Common Pitfalls
- Adding `src/` to tiny single-file utilities that do not benefit from package structure.
- Mixing package code and tests in ways that blur the import boundary.
- Treating the layout as mandatory style rather than as a tool for specific packaging and import problems.

## Local Mapping in This Repository
- Use this reference if repository automation grows from one-off scripts into reusable Python packages or shared modules.
- Pair it with `pyproject.toml` when packaging metadata and tool configuration are introduced.
- Pair it with `pytest` when test imports should reflect installed-package behavior instead of accidental local-path success.

## Process or Workflow
1. Decide whether the repository has reusable Python code that benefits from installed-package import parity.
2. Keep package code under `src/` and tests outside the package tree if that layout is adopted.
3. If `src/` layout becomes the repository standard, move the normative rule into `docs/standards/engineering/**` and keep this file as supporting reference context.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [pytest_reference.md](/home/j/WatchTowerPlan/docs/references/pytest_reference.md)

## Notes
- This reference matters only if the repo starts to contain reusable Python modules or packages.
- A flat layout can still be acceptable for very small scripts or one-off utilities.

## Last Synced
- `2026-03-08`
