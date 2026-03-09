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
updated: "2026-03-08"
audience: "shared"
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
- `https://docs.pytest.org/en/stable/`
- `https://docs.pytest.org/en/stable/explanation/goodpractices.html`
- `https://docs.pytest.org/en/stable/example/markers.html`
- `https://docs.pytest.org/en/stable/how-to/cache.html`

## Related Standards and Sources
- `pytest`
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [src_layout_reference.md](/home/j/WatchTowerPlan/docs/references/src_layout_reference.md)

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
- Use this reference when future repository automation needs a default Python test framework.
- Pair it with `pyproject.toml` guidance when test configuration needs one canonical home.
- Pair it with `src/` layout guidance when import behavior and package layout affect test execution.

## Process or Workflow
1. Decide whether the repository has enough Python logic to justify a shared `pytest` baseline.
2. Keep test layout, markers, and configuration explicit in documentation and configuration files.
3. If `pytest` becomes the repository standard, move the normative rule into `docs/standards/engineering/**` and keep this file as supporting reference context.

## References
- `pytest`
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)

## Notes
- This reference supports future Python automation work and does not imply the repo already has a Python test suite.
- If test policy becomes more formal, it should move into `docs/standards/engineering/`.

## Last Synced
- `2026-03-08`
