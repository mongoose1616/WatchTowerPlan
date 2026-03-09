---
id: "ref.mypy"
title: "mypy Reference"
summary: "Working reference for static type checking in repository Python code."
type: "reference"
status: "active"
tags:
  - "reference"
  - "mypy"
owner: "repository_maintainer"
updated: "2026-03-08"
audience: "shared"
---

# mypy Reference

## Summary
This document provides a working reference for `mypy` when the repository needs static type checking for Python automation or helper code.

## Purpose
Provide a practical baseline for using type checks to catch interface drift, unchecked assumptions, and ambiguous data handling before runtime.

## Scope
- Covers the role of `mypy` in repository-level Python engineering.
- Does not require full strict typing everywhere by default.

## Canonical Upstream
- `https://www.mypy-lang.org/`
- `https://mypy.readthedocs.io/en/stable/`
- `https://mypy.readthedocs.io/en/stable/common_issues.html`
- `https://mypy.readthedocs.io/en/stable/config_file.html`

## Related Standards and Sources
- `mypy`
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [pep8_reference.md](/home/j/WatchTowerPlan/docs/references/pep8_reference.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use type hints to make module boundaries and important data shapes explicit.
- Prefer gradual adoption over a noisy one-time strictness jump.
- Keep `Any` at the edges where it is unavoidable instead of letting it spread everywhere.
- Type check reusable utilities and higher-risk logic before low-value glue code.
- Align type annotations with actual runtime behavior.

### Common Typing Priorities
| Priority | Apply To | Notes |
|---|---|---|
| Highest | Shared interfaces and cross-module data shapes | These are easiest to misuse and hardest to reason about implicitly. |
| Medium | Non-trivial functions with meaningful return behavior | Prefer explicit return types here. |
| Lower | Thin glue code or throwaway scripts | Type only when the value outweighs the noise. |

### Common Pitfalls
- Letting `Any` spread into core logic without clear boundaries.
- Adding type hints that do not match actual runtime behavior.
- Trying to jump to maximum strictness before the codebase is ready.

## Local Mapping in This Repository
- Use this reference when repository automation grows large enough that typed interfaces reduce review and maintenance risk.
- Pair it with `pyproject.toml` guidance if local type-check configuration is introduced.
- Use it alongside Python style and docstring references when a fuller engineering baseline is needed.

## Process or Workflow
1. Decide whether the repository has enough reusable Python code to justify static type checking.
2. Type the highest-risk interfaces, shared data shapes, and cross-module boundaries first.
3. If `mypy` becomes the repository standard, move the normative rule into `docs/standards/engineering/**` and keep this file as supporting reference context.

## References
- `mypy`
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This reference is most useful once the repo has reusable Python modules rather than only one-off scripts.
- If a formal engineering standard is added later, it should define the target strictness and rollout strategy.

## Last Synced
- `2026-03-08`
