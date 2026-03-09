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
updated_at: "2026-03-09T05:03:16Z"
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
- `https://check-jsonschema.readthedocs.io/en/latest/usage.html` - verified 2026-03-09; Usage.

## Related Standards and Sources
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)

## Quick Reference or Distilled Reference
### When It Fits
- Use `check-jsonschema` for schema-backed files in local validation or CI when you want explicit fail-fast validation.
- Keep schema location and file selection explicit so reviewers can see what is being validated.
- Validate both the governed files and the schema itself when schema changes are in scope.

### Common Validation Moves
| Need | Typical approach | Notes |
|---|---|---|
| validate files against one schema | `--schemafile <schema> <files...>` | keep file globs narrow and reviewable |
| use built-in schema targets | built-in schema option | useful for common ecosystem file types |
| validate the schema artifact | metaschema check | catches invalid schemas before downstream use |

### Common Pitfalls
- Treating validation as sufficient when schema ownership and versioning are still unclear.
- Using globs that silently miss files or include unrelated ones.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)

### Why It Matters Here
- Use this reference if repository validation tooling is added under `docs/standards/validations/**` or future CI scripts.
- Pair it with JSON Schema references when deciding how contracts should be enforced.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
