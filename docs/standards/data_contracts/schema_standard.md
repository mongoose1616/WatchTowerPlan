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
updated_at: "2026-03-09T23:02:08Z"
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
- Covers schema format, placement, minimum schema metadata, reuse rules, fail-closed object design, examples, and synchronized updates.
- Does not define every identifier pattern, status set, or compatibility rule by itself.

## Use When
- Adding a new governed artifact type under `core/control_plane/`.
- Publishing an external validation interface.
- Reviewing whether a schema change is breaking, incomplete, or improperly placed.

## Related Standards and Sources
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): foundation intent this standard must remain aligned with.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): foundation intent this standard must remain aligned with.
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [json_schema_2020_12_reference.md](/home/j/WatchTowerPlan/docs/references/json_schema_2020_12_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [check_jsonschema_reference.md](/home/j/WatchTowerPlan/docs/references/check_jsonschema_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [pydantic_strict_mode_reference.md](/home/j/WatchTowerPlan/docs/references/pydantic_strict_mode_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/README.md): family entrypoint and inventory surface this standard should stay aligned with.

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
- Pair published schemas with canonical valid and invalid examples under `core/control_plane/examples/` when the schema describes a reusable artifact family or external interface.
- Update related contracts, registries, policies, examples, and validation logic in the same change set when a schema change alters behavior or acceptance boundaries.

## Structure or Data Model
### Required placement rules
| Schema Type | Canonical Location | Notes |
|---|---|---|
| Shared fragment or reusable field group | `core/control_plane/schemas/common/` | Use for shared ids, refs, timestamps, status fragments, and common object shapes. |
| Core-owned artifact schema | `core/control_plane/schemas/artifacts/` | Use for registries, policies, contracts, indexes, ledgers, or other core-authored artifacts. |
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
- Use filenames that make artifact purpose and version discoverable in review.
- Keep reusable fragments small enough that reviewers can understand why they are shared.
- Do not place generated schemas, caches, or validator output in the canonical schema tree.

## Process or Workflow
1. Decide whether the artifact is a core-owned artifact schema or an external validation interface.
2. Author or update the schema in the correct subtree with the required root metadata and explicit object boundaries.
3. Add or update canonical valid and invalid examples when the schema defines a reusable artifact family or external interface.
4. Update related contracts, registries, policies, or compatibility declarations when the schema changes acceptance or behavior.
5. Run local schema validation and any aligned typed runtime validation before treating the change as complete.

## Examples
- A schema for a core validator-registry record belongs in `core/control_plane/schemas/artifacts/`.
- A schema for an external artifact bundle accepted by core belongs in `core/control_plane/schemas/interfaces/`.
- A shared timestamp, identifier, or status fragment belongs in `core/control_plane/schemas/common/`.
- The shared UTC timestamp fragment belongs in `core/control_plane/schemas/common/` and should be reused by artifact and interface schemas that carry governed mutable timestamps.

## Validation
- New or changed schemas should be validated locally with a JSON Schema validator before merge.
- Canonical `valid/` and `invalid/` examples should prove the acceptance boundary for reusable schema families and external interfaces.
- Reviewers should be able to identify whether a schema change also requires updates to contracts, registries, policies, or compatibility rules.
- If runtime models reject data that the published schema accepts, tighten the schema or document the stricter runtime rule explicitly rather than leaving hidden divergence.

## Change Control
- Update this standard when the repository changes the schema baseline, schema placement model, or fail-closed rules.
- Update related files in the same change set when schema changes affect `core/control_plane/contracts/`, `core/control_plane/registries/`, `core/control_plane/policies/`, or `core/control_plane/examples/`.
- Record breaking acceptance or compatibility changes in the relevant compatibility contract and committed migration history when that structure is in use.

## References
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/README.md)
- [json_schema_2020_12_reference.md](/home/j/WatchTowerPlan/docs/references/json_schema_2020_12_reference.md)
- [check_jsonschema_reference.md](/home/j/WatchTowerPlan/docs/references/check_jsonschema_reference.md)
- [pydantic_strict_mode_reference.md](/home/j/WatchTowerPlan/docs/references/pydantic_strict_mode_reference.md)

## Notes
- This standard deliberately keeps schema structure separate from identifier naming policy. Schema IDs must be stable now, while exact repository-wide naming patterns can be tightened later under `docs/standards/metadata/`.
- If a future format standard introduces more specific serialization or naming rules for schema files, it should refine rather than weaken this standard.

## Updated At
- `2026-03-09T23:02:08Z`
