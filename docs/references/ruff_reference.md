---
id: "ref.ruff"
title: "Ruff Reference"
summary: "Working reference for fast linting and code-quality checks in repository Python code."
type: "reference"
status: "active"
tags:
  - "reference"
  - "ruff"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# Ruff Reference

## Summary
This document provides a working reference for `Ruff` as a fast linting baseline when the repository adopts Python automation.

## Purpose
Provide a simple quality gate for Python code so style drift, unused imports, and common correctness issues are caught early.

## Scope
- Covers the role of `Ruff` in repository-level Python linting.
- Does not define a complete lint policy or required rule set by itself.

## Canonical Upstream
- `https://docs.astral.sh/ruff/` - verified 2026-03-09; Ruff.
- `https://docs.astral.sh/ruff/configuration/` - verified 2026-03-09; Configuring Ruff.
- `https://docs.astral.sh/ruff/settings/` - verified 2026-03-09; Settings.

## Related Standards and Sources
- [pep8_reference.md](/home/j/WatchTowerPlan/docs/references/pep8_reference.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Prefer one fast linting baseline over many overlapping tools when possible.
- Keep the enabled rule set intentional and reviewable.
- Use auto-fix carefully and still read the resulting diff.
- Treat lint failures as signals to improve clarity, not as box-checking noise.
- Document local rule exceptions when they are intentional.

### Common Commands and Configuration
| Item | Use For | Notes |
|---|---|---|
| `ruff check` | Core lint run | Good default command for local and CI linting. |
| `pyproject.toml` | Central configuration home | Keep settings discoverable when Python tooling exists. |
| Rule selection | readability and correctness first | Add niche style rules only when they help more than they churn. |
| Exceptions | targeted suppressions | Avoid broad exemptions that hide real problems. |

### Common Pitfalls
- Adding many overlapping lint tools without a clear reason.
- Accepting auto-fixes without reading the resulting diff.
- Growing the exception list until the rule set stops meaning anything.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)

### Why It Matters Here
- Use this reference when repository automation needs a fast default linting layer.
- Pair it with `pyproject.toml` guidance if lint configuration is centralized there.
- Use it with PEP 8 and docstring references when lint rules are meant to reinforce local engineering standards.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [pep8_reference.md](/home/j/WatchTowerPlan/docs/references/pep8_reference.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)

## Notes
- This reference is most useful once repository Python code is shared or maintained over time.
- If a formal engineering standard is added later, it should define the approved rule set and exception policy.
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
