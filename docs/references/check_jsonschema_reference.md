---
id: "ref.check_jsonschema"
title: "check-jsonschema Reference"
summary: "This document provides a working reference for `check-jsonschema` as a schema-validation tool."
type: "reference"
status: "active"
tags:
  - "reference"
  - "check_jsonschema"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# check-jsonschema Reference

## Summary
This document provides a working reference for `check-jsonschema` as a schema-validation tool.

## Purpose
Provide a lightweight validator reference for enforcing JSON Schema-backed contracts in automation.

## Scope
- Covers `check-jsonschema` as a validation tool.
- Does not require this repository to adopt it.

## Canonical Upstream
- `https://check-jsonschema.readthedocs.io/en/latest/usage.html`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use it when a simple validator is enough to enforce schema-backed files.
- Keep schema locations and validation commands explicit.
- Pair it with a clear schema ownership model rather than treating validation as detached from the contract source.

## Local Mapping in This Repository
- Use this reference if repository validation tooling is added under `docs/standards/validations/**` or future CI scripts.
- Pair it with JSON Schema references when deciding how contracts should be enforced.

## Process or Workflow
1. Read this reference before codifying check-jsonschema Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how schema validation tooling should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
