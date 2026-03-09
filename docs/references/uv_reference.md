---
id: "ref.uv"
title: "uv Reference"
summary: "This document provides a working reference for `uv` as a Python packaging, environment, and dependency-management tool."
type: "reference"
status: "active"
tags:
  - "reference"
  - "uv"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# uv Reference
## Summary
This document provides a working reference for `uv` as a Python packaging, environment, and dependency-management tool.

## Purpose
Provide a baseline for deciding whether `uv` should be part of this repository's Python toolchain.

## Scope
- Covers `uv` at the level of project layout, dependency management, and cache behavior.
- Does not require this repository to adopt `uv`.

## Canonical Upstream
- `https://docs.astral.sh/uv/` - verified 2026-03-09; uv.
- `https://docs.astral.sh/uv/concepts/projects/layout/` - verified 2026-03-09; Structure and files.
- `https://docs.astral.sh/uv/reference/settings/#cache-dir` - verified 2026-03-09; Settings.

## Related Standards and Sources
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)
- [uv.lock](/home/j/WatchTowerPlan/core/python/uv.lock)
- [watchtower_core_doctor.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_doctor.md)

## Quick Reference or Distilled Reference
### Common `uv` Operations
| Command | Use For | Notes |
|---|---|---|
| `uv sync` | create or update the environment from declared dependencies | good default workspace entrypoint |
| `uv run <cmd>` | run tooling inside the managed environment | keeps execution tied to the workspace |
| `uv lock` | refresh lock state when dependencies change | review diffs deliberately |
| tool or cache settings | control auxiliary behavior | keep locations explicit when repo hygiene matters |

### Core Rules
- Use `uv` when fast dependency resolution, lock management, and environment tooling are part of the Python workflow.
- Keep cache placement, lockfile ownership, and project layout explicit.
- Decide whether the repo is using `uv` only as a runner or as the primary package and environment manager.

### Common Pitfalls
- Mixing `uv` with other environment managers without a clear ownership boundary.
- Treating the lockfile as disposable when the repo expects reproducible environments.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)
- [uv.lock](/home/j/WatchTowerPlan/core/python/uv.lock)
- [watchtower_core_doctor.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_doctor.md)

### Why It Matters Here
- Use this reference if `docs/standards/engineering/**` starts defining Python environment tooling.
- Pair it with `pyproject.toml`, `src/` layout, and test/lint/type-check references when shaping a Python toolchain.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml)
- [uv.lock](/home/j/WatchTowerPlan/core/python/uv.lock)
- [watchtower_core_doctor.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_doctor.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
