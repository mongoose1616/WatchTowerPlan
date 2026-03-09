---
id: "ref.pytest"
title: "pytest Reference"
summary: "Working reference for using pytest as the default Python test framework in this repository."
type: "reference"
status: "active"
tags:
  - "reference"
  - "pytest"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# pytest Reference

## Summary
This document provides a working reference for `pytest` as the default testing framework when Python automation exists in this repo.

## Purpose
Provide a simple testing baseline so Python behavior can be validated with consistent structure and review expectations.

## Scope
- Covers the role of `pytest` in repository-level Python testing.
- Does not define a full testing policy or CI policy by itself.

## Canonical Upstream
- `https://docs.pytest.org/en/stable/` - verified 2026-03-09; pytest documentation.
- `https://docs.pytest.org/en/stable/explanation/goodpractices.html` - verified 2026-03-09; Good Integration Practices.
- `https://docs.pytest.org/en/stable/example/markers.html` - verified 2026-03-09; Working with custom markers.
- `https://docs.pytest.org/en/stable/how-to/cache.html` - verified 2026-03-09; How to re-run failed tests and maintain state between test runs.

## Related Standards and Sources
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [src_layout_reference.md](/home/j/WatchTowerPlan/docs/references/src_layout_reference.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)
- [tests](/home/j/WatchTowerPlan/core/python/tests/)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Prefer `pytest` as the default Python test runner when the repo needs Python tests.
- Write tests around observable behavior rather than private implementation detail.
- Use plain `assert` statements unless a helper provides clearer failure output.
- Keep fixtures focused and close to the tests that use them.
- Make markers and special test categories explicit instead of implicit.

### Common Test Layout Rules
| Item | Preferred Shape | Notes |
|---|---|---|
| Test directory | `tests/` | Use another layout only when there is a clear local reason. |
| Test filenames | `test_*.py` | Keeps test discovery predictable. |
| Shared fixtures | `conftest.py` | Use when sharing fixtures improves clarity rather than hiding behavior. |
| Slow or integration tests | explicit markers | Keep category boundaries visible. |
| Test behavior | deterministic | Avoid timing-, network-, or machine-state-sensitive tests by default. |

### Common Pitfalls
- Building tests around implementation detail instead of observable behavior.
- Hiding broad setup in fixtures that make tests hard to read.
- Letting special test categories exist implicitly instead of through explicit markers.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)
- [tests](/home/j/WatchTowerPlan/core/python/tests/)

### Why It Matters Here
- Use this reference when future repository automation needs a default Python test framework.
- Pair it with `pyproject.toml` guidance when test configuration needs one canonical home.
- Pair it with `src/` layout guidance when import behavior and package layout affect test execution.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [src_layout_reference.md](/home/j/WatchTowerPlan/docs/references/src_layout_reference.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)
- [tests](/home/j/WatchTowerPlan/core/python/tests/)

## Notes
- This reference supports future Python automation work and does not imply the repo already has a Python test suite.
- If test policy becomes more formal, it should move into `docs/standards/engineering/`.
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
