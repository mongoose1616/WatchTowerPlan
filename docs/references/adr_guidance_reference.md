---
id: "ref.adr_guidance"
title: "ADR Guidance Reference"
summary: "This document provides a working reference for architecture decision records as a durable decision-capture pattern."
type: "reference"
status: "active"
tags:
  - "reference"
  - "adr_guidance"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# ADR Guidance Reference

## Summary
This document provides a working reference for architecture decision records as a durable decision-capture pattern.

## Purpose
Provide a concise baseline for recording important architectural or policy decisions without leaving rationale scattered across unrelated docs.

## Scope
- Covers ADRs as a decision-record pattern.
- Does not define this repository's exact ADR format or lifecycle by itself.

## Canonical Upstream
- `https://adr.github.io/`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use ADRs for durable decisions with meaningful alternatives or consequences.
- Keep ADRs focused on one decision at a time.
- Consolidate accepted outcomes back into the canonical standards, design docs, or workflows that the ADR affects.

## Local Mapping in This Repository
- Use this reference when building ADR templates or decision-capture standards under `docs/standards/governance/**`.
- Treat ADRs as supporting decision history, not as the only location of active policy.

## Process or Workflow
1. Read this reference before codifying ADR Guidance Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how decision capture and governance history should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
