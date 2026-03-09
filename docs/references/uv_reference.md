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
updated: "2026-03-09"
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
- `https://docs.astral.sh/uv/`
- `https://docs.astral.sh/uv/concepts/projects/layout/`
- `https://docs.astral.sh/uv/reference/settings/#cache-dir`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use `uv` when fast dependency resolution, environment management, and clear project layout are valuable.
- Keep cache placement explicit when repository cleanliness matters.
- Align `uv` usage with the repository's chosen Python packaging layout rather than treating it as a standalone decision.

## Local Mapping in This Repository
- Use this reference if `docs/standards/engineering/**` starts defining Python environment tooling.
- Pair it with `pyproject.toml`, `src/` layout, and test/lint/type-check references when shaping a Python toolchain.

## Process or Workflow
1. Read this reference before codifying uv Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how Python environment and dependency tooling should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
