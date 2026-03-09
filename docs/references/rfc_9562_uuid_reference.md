---
id: "ref.rfc_9562_uuid"
title: "RFC 9562 UUID Reference"
summary: "This document provides a working reference for RFC 9562 as the current UUID standard."
type: "reference"
status: "active"
tags:
  - "reference"
  - "rfc_9562_uuid"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# RFC 9562 UUID Reference

## Summary
This document provides a working reference for RFC 9562 as the current UUID standard.

## Purpose
Provide a standard identifier baseline when UUIDs are used in structured records or system contracts.

## Scope
- Covers UUIDs as standardized by RFC 9562.
- Does not require UUIDs as the only identifier strategy in the repository.

## Canonical Upstream
- `https://www.rfc-editor.org/info/rfc9562`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use RFC 9562 as the UUID reference instead of older RFC 4122-only guidance.
- Choose UUID versions intentionally rather than defaulting by habit.
- Document where UUIDs are required and where simpler IDs are sufficient.

## Local Mapping in This Repository
- Use this reference when identifier standards are added under `docs/standards/metadata/**` or `docs/standards/data_contracts/**`.
- Pair it with timestamp and serialization references when designing event or artifact records.

## Process or Workflow
1. Read this reference before codifying RFC 9562 UUID Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how identifier format selection should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
