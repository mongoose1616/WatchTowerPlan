---
id: "std.data_contracts.schema"
title: "Schema Standard"
summary: "This standard defines how governed structured data is modeled with JSON Schema in this repository and how those schemas are organized under `core/control_plane/schemas/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "schema"
owner: "repository_maintainer"
updated_at: "2026-03-16T20:30:00Z"
audience: "shared"
authority: "authoritative"
---

# Schema Standard

## Summary
This standard defines how governed structured data is modeled with JSON Schema in this repository and how those schemas are organized under `core/control_plane/schemas/`.

## Purpose
Define one consistent schema baseline so core-owned artifacts and externally validated inputs can be checked locally, fail closed, and evolve without hidden contract drift.

## Scope
- Applies to machine-readable artifacts treated as governed inputs, governed outputs, or canonical core authority.
- Covers schema format, placement, minimum schema metadata, reuse rules, fail-closed object design, and synchronized updates.
- Does not define every identifier pattern, status set, or compatibility rule by itself.

## Use When
- Adding a new governed artifact type under `core/control_plane/`.
- Publishing an external validation interface.
- Reviewing whether a schema change is breaking, incomplete, or improperly placed.

## Related Standards and Sources
- [repository_standards_posture.md](/core/docs/foundations/repository_standards_posture.md): foundation intent this standard must remain aligned with.
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md): foundation intent this standard must remain aligned with.
- [format_selection_standard.md](/core/docs/standards/data_contracts/format_selection_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [naming_and_ids_standard.md](/core/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/core/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [json_schema_2020_12_reference.md](/core/docs/references/json_schema_2020_12_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [check_jsonschema_reference.md](/core/docs/references/check_jsonschema_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [pydantic_strict_mode_reference.md](/core/docs/references/pydantic_strict_mode_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [README.md](/core/control_plane/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Treat the schema as the canonical contract for any governed machine-readable artifact that core owns or formally accepts.
- Use JSON Schema Draft 2020-12 as the repository baseline for schema-authored validation.
- Keep schema-authored governed artifacts aligned with the repository format-selection standard.
- Keep canonical schemas under `core/control_plane/schemas/`.
- Place shared reusable fragments in `core/control_plane/schemas/common/`.
- Place schemas for core-owned artifacts in `core/control_plane/schemas/artifacts/`.
- Place schemas for external accepted inputs in `core/control_plane/schemas/interfaces/`.
- Keep schema `$id` values aligned with the repository naming and IDs standard.
- Keep schemas versioned and reviewable. Do not rely on git history alone to understand which contract version is current.
- Require a schema before an artifact type becomes canonical, accepted by automation, or referenced by a validator registry.
- Keep runtime typed models aligned with schemas. Typed validation may add stricter runtime behavior, but it must not silently replace the published schema contract.
- Object-shaped schemas must declare object boundaries explicitly. `properties`, `required`, and `additionalProperties` should be intentional rather than implied.
- Default to fail-closed object contracts. Set `additionalProperties: false` unless the artifact intentionally supports open-ended maps.
- Reuse definitions through `$defs` and `$ref` instead of copying shared field definitions across multiple schemas.
- Keep enums and other shared constrained values in shared reusable schema fragments when reuse materially reduces drift.
- Reuse the shared UTC timestamp fragment for governed `updated_at`, `recorded_at`, and `generated_at` fields instead of open-coding separate timestamp rules.
- Keep interface schemas separate from core-authored artifact schemas even when the fields overlap. Accepted external input is a different contract boundary from core-owned canonical state.
- When external validation needs schemas that do not belong in the canonical catalog, load them through explicit supplemental schema paths or in-memory supplemental schema documents instead of mutating the repository-owned catalog opportunistically.
- Prefer live governed artifacts and inline test payloads over repository fixture corpora when validating schema behavior.
- Update related contracts, registries, manifests, indexes, ledgers, and validation logic in the same change set when a schema change alters behavior or acceptance boundaries.

## Structure or Data Model
### Required placement rules
| Schema Type | Canonical Location | Notes |
|---|---|---|
| Shared fragment or reusable field group | `core/control_plane/schemas/common/` | Use for shared ids, refs, timestamps, status fragments, and common object shapes. |
| Core-owned artifact schema | `core/control_plane/schemas/artifacts/` | Use for registries, manifests, contracts, indexes, ledgers, or other core-authored artifacts. |
| External validation interface | `core/control_plane/schemas/interfaces/` | Use for artifacts core validates but does not own. |

### Minimum root expectations
| Element | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Must target JSON Schema Draft 2020-12. |
| `$id` | Required | Must be unique and stable for the life of the contract version. |
| `title` | Required | Keep it short and artifact-specific. |
| `description` | Required | Explain the artifact boundary and intent. |
| `type` | Required when the root is constrained to an object or array | Do not rely on implicit typing. |
| `properties` | Required for object roots | Define governed fields explicitly. |
| `required` | Explicit for object roots | Make mandatory fields visible in review. |
| `additionalProperties` | Explicit for object roots | Default to `false` unless openness is intentional and documented. |

### File conventions
- Store published schemas as JSON files under `core/control_plane/schemas/**`.
- Name published schema files with the suffix `.schema.json`.
- Use filenames that make artifact purpose discoverable in review and keep compatibility signaling inside schema content rather than the path.
- Do not place the literal word `version` or path-level version tokens such as `.v1` or `_v1_0` in schema filenames.
- Keep reusable fragments small enough that reviewers can understand why they are shared.
- Do not place generated schemas, caches, or validator output in the canonical schema tree.

## Process or Workflow
1. Decide whether the artifact is a core-owned artifact schema or an external validation interface.
2. Author or update the schema in the correct subtree with the required root metadata and explicit object boundaries.
3. Add or update live governed artifacts, inline tests, or direct validator coverage when the schema family changes materially.
4. Update related contracts, registries, manifests, or compatibility declarations when the schema changes acceptance or behavior.
5. Run local schema validation and any aligned typed runtime validation before treating the change as complete.

## Examples
- A schema for a core validator-registry record belongs in `core/control_plane/schemas/artifacts/`.
- A schema for an external artifact bundle accepted by core belongs in `core/control_plane/schemas/interfaces/`.
- A shared timestamp, identifier, or status fragment belongs in `core/control_plane/schemas/common/`.
- The shared UTC timestamp fragment belongs in `core/control_plane/schemas/common/` and should be reused by artifact and interface schemas that carry governed mutable timestamps.

## Operationalization
- `Modes`: `artifact`; `schema`
- `Operational Surfaces`: `core/control_plane/`; `core/control_plane/schemas/`; `core/control_plane/README.md`; `core/control_plane/contracts/`; `core/control_plane/manifests/`; `core/control_plane/registries/`; `core/control_plane/indexes/`; `core/control_plane/ledgers/`

## Validation
- New or changed schemas should be validated locally with a JSON Schema validator before merge.
- Schema changes should stay covered by live governed artifacts, inline test payloads, or direct validator assertions.
- Reviewers should be able to identify whether a schema change also requires updates to contracts, registries, manifests, or compatibility rules.
- If runtime models reject data that the published schema accepts, tighten the schema or document the stricter runtime rule explicitly rather than leaving hidden divergence.
- Supplemental schema loading should fail closed on missing paths, invalid JSON, invalid schemas, or duplicate `$id` values.

## Change Control
- Update this standard when the repository changes the schema baseline, schema placement model, or fail-closed rules.
- Update related files in the same change set when schema changes affect `core/control_plane/contracts/`, `core/control_plane/manifests/`, `core/control_plane/registries/`, `core/control_plane/indexes/`, or `core/control_plane/ledgers/`.
- Record breaking acceptance or compatibility changes in the relevant compatibility contract and committed migration history when that structure is in use.

## References
- [repository_standards_posture.md](/core/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md)
- [format_selection_standard.md](/core/docs/standards/data_contracts/format_selection_standard.md)
- [naming_and_ids_standard.md](/core/docs/standards/metadata/naming_and_ids_standard.md)
- [timestamp_standard.md](/core/docs/standards/metadata/timestamp_standard.md)
- [README.md](/core/control_plane/README.md)
- [json_schema_2020_12_reference.md](/core/docs/references/json_schema_2020_12_reference.md)
- [check_jsonschema_reference.md](/core/docs/references/check_jsonschema_reference.md)
- [pydantic_strict_mode_reference.md](/core/docs/references/pydantic_strict_mode_reference.md)

## Notes
- This standard deliberately keeps schema structure separate from identifier naming policy. Schema IDs must be stable now, while exact repository-wide naming patterns can be tightened later under `core/docs/standards/metadata/`.
- If a future format standard introduces more specific serialization or naming rules for schema files, it should refine rather than weaken this standard.

## Updated At
- `2026-03-16T20:30:00Z`
