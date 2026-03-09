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
updated: "2026-03-09"
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
- `https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPYCACHEPREFIX`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use the variable when cache placement needs to be explicit.
- Keep cache redirection aligned with the repository's artifact and temp-file hygiene rules.
- Do not rely on ambient default cache placement if the repo requires deterministic layout.

## Local Mapping in This Repository
- Use this reference if the repo adopts Python tooling and needs explicit cache placement rules.
- Pair it with `uv`, Ruff, mypy, pytest, and coverage guidance when shaping a clean Python environment.

## Process or Workflow
1. Read this reference before codifying PYTHONPYCACHEPREFIX Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how Python cache placement should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
