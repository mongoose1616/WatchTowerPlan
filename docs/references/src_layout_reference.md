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
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
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
- `https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/` - verified 2026-03-09; src layout vs flat layout.

## Related Standards and Sources
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [pytest_reference.md](/home/j/WatchTowerPlan/docs/references/pytest_reference.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [src](/home/j/WatchTowerPlan/core/python/src/)

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
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [src](/home/j/WatchTowerPlan/core/python/src/)

### Why It Matters Here
- Use this reference if repository automation grows from one-off scripts into reusable Python packages or shared modules.
- Pair it with `pyproject.toml` when packaging metadata and tool configuration are introduced.
- Pair it with `pytest` when test imports should reflect installed-package behavior instead of accidental local-path success.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [pytest_reference.md](/home/j/WatchTowerPlan/docs/references/pytest_reference.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [src](/home/j/WatchTowerPlan/core/python/src/)

## Notes
- This reference matters only if the repo starts to contain reusable Python modules or packages.
- A flat layout can still be acceptable for very small scripts or one-off utilities.
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
