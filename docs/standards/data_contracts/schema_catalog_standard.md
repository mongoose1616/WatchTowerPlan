# Schema Catalog Standard

## Summary
This standard defines the role, structure, and boundary rules for the authored schema catalog registry stored under `core/control_plane/registries/schema_catalog/`.

## Purpose
Provide deterministic local resolution from published schema `$id` values to canonical repository files without hardcoding schema lookup tables in Python or overloading the repository path index with schema-authority concerns.

## Scope
- Applies to authored schema catalog registry artifacts stored under `core/control_plane/registries/schema_catalog/`.
- Covers placement, record shape, identifier use, update expectations, and the boundary between the schema catalog and the schema files it references.
- Does not replace published schemas, schema validation, repository path indexes, or validator selection policy.

## Use When
- Adding a new published schema under `core/control_plane/schemas/`.
- Refreshing the local schema-resolution surface used by core automation.
- Reviewing whether schema lookup metadata belongs in a registry or an index.

## Related Standards and Sources
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [validator_registry.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/validators/validator_registry.v1.json)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/registries/schema_catalog/README.md)

## Guidance
- Model schema lookup as a registry, not as an index.
- Treat the schema catalog as the canonical machine-readable mapping from published schema `$id` values to canonical repository paths.
- Store published schema catalog artifacts under `core/control_plane/registries/schema_catalog/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published schema catalog artifact.
- Catalog only published governed schemas that core expects automation to resolve locally.
- Use the schema file's published `$id` as the canonical record key. Do not invent separate hidden schema identifiers in code.
- Keep `canonical_path` values repository-relative. Do not store absolute filesystem paths in the canonical catalog.
- Keep schema catalog records small. The catalog should point to the authoritative schema file, not duplicate the schema body.
- Include lookup-oriented metadata such as `schema_family`, `subject_kind`, `version`, and optional `aliases` only when it materially improves local resolution or review clarity.
- Use `schema_family` to describe the published schema subtree family such as `artifact`, `interface`, or `common`.
- Update the schema catalog in the same change set whenever a published schema is added, renamed, deprecated, or removed.
- Prefer deletion over long-lived deprecated catalog records when the underlying schema has been removed and no local compatibility surface still depends on it.
- Do not use the schema catalog as a substitute for validator registries, contracts, or repository path indexes.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the schema-catalog artifact family. |
| `id` | Required | Stable identifier for the schema catalog artifact. |
| `title` | Required | Human-readable title for the registry artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `schemas` | Required | Array of schema catalog records. |

### Schema catalog record fields
| Field | Requirement | Notes |
|---|---|---|
| `schema_id` | Required | Published schema `$id` value. |
| `title` | Required | Human-readable schema name. |
| `description` | Required | Short description of the schema boundary. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `schema_family` | Required | Use `artifact`, `interface`, or `common`. |
| `subject_kind` | Required | Short machine-usable label for the governed subject such as `validator_registry` or `documentation_front_matter`. |
| `version` | Required | Major schema version token such as `v1`. |
| `canonical_path` | Required | Repository-relative path to the published schema file. |
| `aliases` | Optional | Alternate lookup terms that materially improve local resolution. |
| `notes` | Optional | Short implementation or resolution notes. |

## Process or Workflow
1. Add or update the published schema under `core/control_plane/schemas/`.
2. Add or update the matching schema catalog record in the same change set.
3. Validate that the catalog record points to the correct schema file and that the schema file publishes the same `$id`.
4. Update related validators, contracts, examples, or local loaders in the same change set when schema-resolution behavior changes.
5. Validate the schema catalog artifact against its published artifact schema before treating the change as complete.

## Examples
- The validator registry schema belongs in the catalog as an `artifact` schema with a canonical path under `core/control_plane/schemas/artifacts/`.
- The reference front matter schema belongs in the catalog as an `interface` schema with a canonical path under `core/control_plane/schemas/interfaces/documentation/`.
- A generated repository path catalog does not belong in the schema catalog because it is an index, not a stable schema-identity registry.

## Validation
- The schema catalog should validate against its published artifact schema.
- Every `canonical_path` should exist and point to a published schema file.
- Every cataloged `schema_id` should match the `$id` inside the file referenced by `canonical_path`.
- Reviewers should reject duplicate published `schema_id` values, stale paths, or catalog records that point to non-schema files.
- Reviewers should reject schema-resolution logic that depends on hidden hardcoded ID-to-path mappings when the schema catalog already defines them.

## Change Control
- Update this standard when the repository changes how published schemas are cataloged or resolved locally.
- Update the companion artifact schema, examples, and live catalog in the same change set when the schema-catalog artifact family changes structurally.
- Update related validator, contract, or loader surfaces in the same change set when schema lookup behavior changes materially.

## References
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [validator_registry.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/validators/validator_registry.v1.json)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/registries/schema_catalog/README.md)

## Notes
- The schema catalog exists because published schema identities are stable governed artifacts, not just filesystem paths.
- The repository path index remains the right place for broad repository navigation and retrieval. The schema catalog is narrower and authoritative for schema resolution only.

## Last Synced
- `2026-03-09`
