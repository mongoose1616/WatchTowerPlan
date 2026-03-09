---
id: "ref.regal"
title: "Regal Reference"
summary: "This document provides a working reference for Regal as a linter and language server for Rego."
type: "reference"
status: "active"
tags:
  - "reference"
  - "regal"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# Regal Reference

## Summary
This document provides a working reference for Regal as a linter and language server for Rego.

## Purpose
Provide a quality and tooling baseline for Rego policy authoring when policy-as-code is adopted.

## Scope
- Covers Regal as a Rego tooling companion.
- Does not require Rego linting unless the repository adopts Rego.

## Canonical Upstream
- `https://www.openpolicyagent.org/projects/regal`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use Regal when Rego policy quality, idioms, and tooling feedback need to be enforced consistently.
- Keep lint policy explicit instead of relying on tool defaults alone.
- Treat Regal as a companion to Rego, not as the policy definition itself.

## Local Mapping in This Repository
- Use this reference only if the repository later adopts OPA/Rego.
- Pair it with OPA/Rego policy standards or validation workflows.

## Process or Workflow
1. Read this reference before codifying Regal Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how Rego linting and policy developer tooling should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
