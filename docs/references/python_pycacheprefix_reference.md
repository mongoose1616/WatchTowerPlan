---
id: "ref.python_pycacheprefix"
title: "PYTHONPYCACHEPREFIX Reference"
summary: "This document provides a working reference for `PYTHONPYCACHEPREFIX` as a Python cache-placement control."
type: "reference"
status: "active"
tags:
  - "reference"
  - "python_pycacheprefix"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# PYTHONPYCACHEPREFIX Reference
## Summary
This document provides a working reference for `PYTHONPYCACHEPREFIX` as a Python cache-placement control.

## Purpose
Provide a baseline for keeping Python bytecode caches in controlled locations rather than scattered across the repository.

## Scope
- Covers the `PYTHONPYCACHEPREFIX` environment variable.
- Does not define the repository's complete Python cache policy by itself.

## Canonical Upstream
- `https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPYCACHEPREFIX` - verified 2026-03-09; 1. Command line and environment.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What It Does
- Redirects bytecode cache files away from the source tree into a dedicated prefix path.
- Helps keep working directories clean when tooling or CI should not leave scattered `__pycache__` directories.
- Changes cache placement, not import semantics or packaging layout.

### Common Decisions
| Question | Preferred answer | Why |
|---|---|---|
| redirect caches | yes when repo cleanliness or temp isolation matters | keeps the source tree cleaner |
| env var vs command-line switch | choose one clear mechanism | avoids hidden behavior differences |
| cache location | explicit temp or workspace path | easier cleanup and review |

### Common Pitfalls
- Assuming cache redirection changes import behavior rather than only cache placement.
- Setting a prefix but never cleaning or documenting the resulting cache path.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if the repo adopts Python tooling and needs explicit cache placement rules.
- Pair it with `uv`, Ruff, mypy, pytest, and coverage guidance when shaping a clean Python environment.

### If Local Policy Tightens
- Promote any adopted repository rule into a narrower standard or workflow instead of leaving the rule only in this reference.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- If this topic becomes active repository policy later, move the enforceable rule into `docs/standards/**` or the relevant workflow module.

## Updated At
- `2026-03-09T05:03:16Z`
