---
id: "std.validations.schema_surface_validation"
title: "Schema Surface Validation Standard"
summary: "This standard defines how the repository validates JSON artifact instances versus JSON Schema definition files."
type: "standard"
status: "active"
tags:
  - "standard"
  - "validations"
  - "schema"
  - "json_schema"
owner: "repository_maintainer"
updated_at: "2026-03-25T02:15:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/schemas/"
  - "core/control_plane/"
  - "pack_owned_machine_state"
  - "core/python/"
aliases:
  - "schema validation modes"
  - "schema surface validation"
---

# Schema Surface Validation Standard

## Summary
This standard defines how the repository validates JSON artifact instances versus JSON Schema definition files.

## Purpose
- Make the validation split explicit so humans and agents do not confuse schema-definition checks with artifact-instance checks.
- Keep `*.schema.json` authoring fail-closed without overloading the artifact-validator auto-selection rules.
- Give repository and pack authors one clear command path for each schema-related validation need.

## Scope
- Applies to repository-owned and pack-owned JSON artifacts, schema-definition files, and external artifact validation flows.
- Covers direct schema-definition validation, explicit external artifact validation, and the boundary between those modes.
- Does not redefine the schema catalog, validator registry, or the repository-wide validation baseline by itself.

## Use When
- Changing any `*.schema.json` file under shared core or a hosted pack.
- Validating an external JSON artifact against an explicit schema without publishing a registry entry.
- Reviewing whether a change used the correct validation command for the surface it touched.

## Related Standards and Sources
- [schema_standard.md](/core/docs/standards/data_contracts/schema_standard.md): defines how shared schemas should be authored and governed.
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md): defines the broad validation baseline for repository changes.
- [watchtower_core_validate_artifact.md](/core/docs/commands/core_python/watchtower_core_validate_artifact.md): validates artifact instances against registry-backed or explicit schemas.
- [watchtower_core_validate_schema.md](/core/docs/commands/core_python/watchtower_core_validate_schema.md): validates schema-definition files against the Draft 2020-12 metaschema.
- [watchtower_core_validate_all.md](/core/docs/commands/core_python/watchtower_core_validate_all.md): runs the broad repository validation baseline.

## Guidance
- Treat artifact-instance validation and schema-definition validation as different operations.
- Use `watchtower-core validate artifact --path <artifact>` when the target is a JSON artifact instance that should conform to a published validator or schema.
- Use `watchtower-core validate schema --path <schema>` when the target is a `*.schema.json` definition file.
- Do not expect `watchtower-core validate artifact` auto-selection to target `*.schema.json` files. That auto-selection is intentionally reserved for artifact instances.
- Use `watchtower-core validate artifact --schema-id <schema_id> --supplemental-schema-path <path>` when validating an external artifact instance against an explicit schema that is not already in the active registry.
- External artifact instances may also validate directly from the artifact document's own `$schema` when the referenced schema is available through supplemental schema paths.
- When a change touched both a schema-definition file and one or more live artifact instances that depend on it, run both `validate schema` on the changed schema files and the relevant artifact or broad repository validation on the dependent instances.
- `watchtower-core validate all` is still the broad repository baseline, but it is not a substitute for explicit `validate schema` runs on changed schema-definition files.
- `watchtower-core validate schema` also supports the standard validation-evidence flags when you need durable proof for a repository-local schema-definition check.

## Structure or Data Model
### Validation Mode Selection
| Target Kind | Preferred Command | Notes |
|---|---|---|
| Repository-local artifact instance | `watchtower-core validate artifact --path <artifact>` | Auto-selects the most specific active artifact validator. |
| External artifact instance with explicit schema | `watchtower-core validate artifact --path <artifact> --schema-id <schema_id> --supplemental-schema-path <path>` | Avoids patching the canonical validator registry for one-off validation. |
| External artifact instance with embedded `$schema` | `watchtower-core validate artifact --path <artifact> --supplemental-schema-path <path>` | Uses the artifact document's own `$schema` value. |
| JSON Schema definition file | `watchtower-core validate schema --path <schema>` | Validates the schema document against the Draft 2020-12 metaschema. |

### Minimum Validation Expectations
| Change Shape | Required Proof |
|---|---|
| Changed artifact instance only | Matching `validate artifact` result or broader validation that covers the same instance |
| Changed schema-definition file only | `validate schema` result for each touched `*.schema.json` |
| Changed schema plus dependent instances | `validate schema` plus artifact validation or `validate all`, depending on the touched surfaces |

## Operationalization
- `Modes`: `validation`; `documentation`
- `Operational Surfaces`: `core/docs/commands/core_python/watchtower_core_validate_artifact.md`; `core/docs/commands/core_python/watchtower_core_validate_schema.md`; `core/python/src/watchtower_core/validation/artifact.py`; `core/python/src/watchtower_core/validation/schema_definition.py`

## Validation
- Reviewers should reject schema-authoring changes that rely only on artifact-instance validation when `*.schema.json` files changed.
- Reviewers should reject attempts to treat `validate artifact` auto-selection as a schema-definition validator.
- Reviewers should reject external artifact validation flows that omit an explicit schema source when the artifact does not declare its own `$schema`.

## Change Control
- Update this standard when the repository changes the supported schema-definition validator, artifact auto-selection behavior, or external artifact validation path.
- Update the companion command docs, repository validation standard, and workspace README in the same change set when the schema-validation contract changes materially.

## References
- [schema_standard.md](/core/docs/standards/data_contracts/schema_standard.md)
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md)
- [watchtower_core_validate_artifact.md](/core/docs/commands/core_python/watchtower_core_validate_artifact.md)
- [watchtower_core_validate_schema.md](/core/docs/commands/core_python/watchtower_core_validate_schema.md)

## Updated At
- `2026-03-25T02:15:00Z`
