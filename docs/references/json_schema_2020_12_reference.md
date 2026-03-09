---
id: "ref.json_schema_2020_12"
title: "JSON Schema 2020-12 Reference"
summary: "This document provides a working reference for JSON Schema Draft 2020-12 as a fail-closed schema validation baseline."
type: "reference"
status: "active"
tags:
  - "reference"
  - "json_schema_2020_12"
owner: "repository_maintainer"
updated: "2026-03-09"
audience: "shared"
authority: "reference"
---

# JSON Schema 2020-12 Reference

## Summary
This document provides a working reference for JSON Schema Draft 2020-12 as a fail-closed schema validation baseline.

## Purpose
Provide a schema-validation baseline for structured data contracts that need machine validation.

## Scope
- Covers JSON Schema Draft 2020-12 as a schema standard.
- Does not define every repository schema by itself.

## Canonical Upstream
- `https://json-schema.org/draft/2020-12`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use schemas for data contracts that benefit from explicit machine validation.
- Keep schema versions and evolution rules deliberate.
- Treat unknown required fields, missing required fields, and malformed payloads as contract issues rather than as informal warnings.

## Local Mapping in This Repository
- Use this reference for schema-heavy content under `docs/standards/data_contracts/**`.
- Use it when future registries or JSON documents need an explicit validation contract.

## Process or Workflow
1. Read this reference before codifying JSON Schema 2020-12 Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how data contracts and schema validation should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
