---
id: "ref.uv"
title: "uv Reference"
summary: "This document provides a working reference for installing and using `uv` as a Python packaging, environment, and dependency-management tool."
type: "reference"
status: "active"
tags:
  - "reference"
  - "uv"
owner: "repository_maintainer"
updated_at: "2026-03-24T21:49:49Z"
audience: "shared"
authority: "reference"
---

# uv Reference
## Summary
This document provides a working reference for installing and using `uv` as a Python packaging, environment, and dependency-management tool.

## Purpose
Provide a baseline for deciding whether `uv` should be part of this repository's Python toolchain.

## Scope
- Covers `uv` at the level of project layout, dependency management, and cache behavior.
- Does not require this repository to adopt `uv`.

## Canonical Upstream
- `https://docs.astral.sh/uv/` - verified 2026-03-24; uv.
- `https://docs.astral.sh/uv/getting-started/installation/` - verified 2026-03-24; Installation methods and shell setup.
- `https://docs.astral.sh/uv/reference/installer/` - verified 2026-03-24; Installer options and PATH behavior.
- `https://docs.astral.sh/uv/concepts/projects/layout/` - verified 2026-03-24; Structure and files.
- `https://docs.astral.sh/uv/reference/settings/#cache-dir` - verified 2026-03-24; Settings.

## Related Standards and Sources
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/core/python/pyproject.toml)
- [uv.lock](/core/python/uv.lock)
- [watchtower_core_doctor.md](/core/docs/commands/core_python/watchtower_core_doctor.md)

## Quick Reference or Distilled Reference
### Common `uv` Operations
| Command | Use For | Notes |
|---|---|---|
| `uv sync` | create or update the environment from declared dependencies | good default workspace entrypoint |
| `uv run <cmd>` | run tooling inside the managed environment | keeps execution tied to the workspace |
| `uv lock` | refresh lock state when dependencies change | review diffs deliberately |
| tool or cache settings | control auxiliary behavior | keep locations explicit when repo hygiene matters |

### Install `uv`
- macOS and Linux standalone installer: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows PowerShell standalone installer: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Homebrew: `brew install uv`
- `pipx`: `pipx install uv`
- Verify the executable after install with `uv --version`.
- If the standalone installer updated shell profiles but the current shell still cannot resolve `uv`, restart the shell or add the executable directory to `PATH`. A common default on macOS and Linux is `export PATH="$HOME/.local/bin:$PATH"`.

### Core Rules
- Use `uv` when fast dependency resolution, lock management, and environment tooling are part of the Python workflow.
- Keep cache placement, lockfile ownership, and project layout explicit.
- Decide whether the repo is using `uv` only as a runner or as the primary package and environment manager.

### Common Pitfalls
- Mixing `uv` with other environment managers without a clear ownership boundary.
- Treating the lockfile as disposable when the repo expects reproducible environments.

## Local Mapping in This Repository
### Current Repository Status
- Active support. The current repository workspace contract uses `uv` as the default runner and shared environment manager for `core/python/`.

### Current Touchpoints
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/core/python/pyproject.toml)
- [uv.lock](/core/python/uv.lock)
- [watchtower_core_doctor.md](/core/docs/commands/core_python/watchtower_core_doctor.md)

### Why It Matters Here
- Use this reference if `core/docs/standards/engineering/**` starts defining Python environment tooling.
- Pair it with `pyproject.toml`, `src/` layout, and test/lint/type-check references when shaping a Python toolchain.
- Use it when onboarding a new engineer or when copied-core bootstrap fails because `uv` is missing from `PATH`.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [pyproject.toml](/core/python/pyproject.toml)
- [uv.lock](/core/python/uv.lock)
- [watchtower_core_doctor.md](/core/docs/commands/core_python/watchtower_core_doctor.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-24` while updating shared workspace onboarding and copied-core bootstrap guidance.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-24T21:49:49Z`
