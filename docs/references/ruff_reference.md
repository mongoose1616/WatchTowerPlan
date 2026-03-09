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
updated: "2026-03-08"
audience: "shared"
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
- `https://docs.astral.sh/ruff/`
- `https://docs.astral.sh/ruff/configuration/`
- `https://docs.astral.sh/ruff/settings/`

## Related Standards and Sources
- `Ruff`
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [pep8_reference.md](/home/j/WatchTowerPlan/docs/references/pep8_reference.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)

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
- Use this reference when repository automation needs a fast default linting layer.
- Pair it with `pyproject.toml` guidance if lint configuration is centralized there.
- Use it with PEP 8 and docstring references when lint rules are meant to reinforce local engineering standards.

## Process or Workflow
1. Decide whether the repository has enough maintained Python code to justify a shared lint baseline.
2. Choose a small, reviewable Ruff configuration before expanding the rule set.
3. If Ruff becomes the repository standard, move the normative rule into `docs/standards/engineering/**` and keep this file as supporting reference context.

## References
- `Ruff`
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)

## Notes
- This reference is most useful once repository Python code is shared or maintained over time.
- If a formal engineering standard is added later, it should define the approved rule set and exception policy.

## Last Synced
- `2026-03-08`
