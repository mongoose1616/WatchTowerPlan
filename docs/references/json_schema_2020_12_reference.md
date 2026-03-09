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
updated_at: "2026-03-09T05:03:16Z"
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
- `https://json-schema.org/draft/2020-12` - verified 2026-03-09; JSON Schema.

## Related Standards and Sources
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [schemas](/home/j/WatchTowerPlan/core/control_plane/schemas/)

## Quick Reference or Distilled Reference
### Core Validation Rules
- Use JSON Schema when a machine-readable contract should reject malformed or incomplete data explicitly.
- Make object openness deliberate: properties are permissive by default unless the schema narrows them.
- Separate structural validation from business policy that the schema cannot express cleanly.

### Common Keywords
| Keyword | Use For | Notes |
|---|---|---|
| `type` | base kind constraints | objects, arrays, strings, numbers, booleans, null |
| `required` | mandatory object properties | applies only to object members |
| `properties` / `items` | nested structure | combine with required fields and length/count rules |
| `enum` / `const` | fixed vocabularies | useful for governed status or mode fields |
| `additionalProperties` / `unevaluatedProperties` | object openness control | critical when fail-closed behavior matters |

### Common Pitfalls
- Assuming unknown fields are rejected unless the schema says so.
- Treating schema validation as a substitute for versioning and migration rules.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [schemas](/home/j/WatchTowerPlan/core/control_plane/schemas/)

### Why It Matters Here
- Use this reference for schema-heavy content under `docs/standards/data_contracts/**`.
- Use it when future registries or JSON documents need an explicit validation contract.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [schemas](/home/j/WatchTowerPlan/core/control_plane/schemas/)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
