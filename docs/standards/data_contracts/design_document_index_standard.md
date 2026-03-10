---
id: "std.data_contracts.design_document_index"
title: "Design Document Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable design-document indexes stored under `core/control_plane/indexes/design_documents/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "design_document_index"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:11:26Z"
audience: "shared"
authority: "authoritative"
---

# Design Document Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable design-document indexes stored under `core/control_plane/indexes/design_documents/`.

## Purpose
Provide a compact lookup and tracking surface for feature designs and implementation plans without forcing future tooling to scan Markdown directly.

## Scope
- Applies to machine-readable design-document index artifacts stored under `core/control_plane/indexes/design_documents/`.
- Covers placement, entry shape, update expectations, and the relationship between the index and the human-readable design tracker in `docs/planning/design/`.
- Does not replace the design documents themselves or turn the index into design authority.

## Use When
- Adding a new feature design or implementation plan under `docs/planning/design/`.
- Refreshing design-tracking data after a design document is renamed, removed, or materially retargeted.
- Building query or routing tools that need a compact machine-readable view over the design corpus.

## Related Standards and Sources
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [design_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/design_tracking.md): companion planning or design surface this standard should remain consistent with.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/design_documents/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Model design-document tracking as an index, not as a registry.
- Treat the design-document index as a machine-readable lookup and relationship surface rather than the authority for design content.
- Keep design semantics in the documents under `docs/planning/design/**`.
- Store published design-document indexes under `core/control_plane/indexes/design_documents/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published design-document index artifact.
- Catalog only durable feature designs and implementation plans that live under `docs/planning/design/features/` or `docs/planning/design/implementation/`.
- Source stable identity and summary fields from the governed design-document front matter rather than reconstructing them from body prose.
- Every index entry must point to an existing design document under `docs/planning/design/`.
- Carry a shared `trace_id` in every entry so designs and plans can join to PRDs and decisions cleanly.
- Use a stable `document_id` per design document.
- Record the document family explicitly as `feature_design` or `implementation_plan`.
- Require `source_paths` for implementation plans so the plan-to-design relationship is explicit.
- Capture whether the design explicitly used internal or external references so reference use is queryable without reparsing Markdown.
- Keep the human-readable design tracker and the machine-readable index aligned in the same change set.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the design-document-index artifact family. |
| `id` | Required | Stable identifier for the design-document index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of design-document records. |

### Design-document entry fields
| Field | Requirement | Notes |
|---|---|---|
| `document_id` | Required | Stable machine-usable document identifier. |
| `trace_id` | Required | Shared umbrella identifier for the traced initiative. |
| `family` | Required | Use `feature_design` or `implementation_plan`. |
| `title` | Required | Human-readable design document title. |
| `summary` | Required | Concise description of the design document. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `doc_path` | Required | Repository-relative path to the Markdown design document. |
| `updated_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, matching the design document front matter `updated_at` value and the `Record Metadata` value. |
| `uses_internal_references` | Required | Whether the design document explicitly cited internal repository references. |
| `uses_external_references` | Required | Whether the design document explicitly cited external sources. |
| `source_paths` | Required for implementation plans | Paths to the driving feature design, PRD, or other source surfaces. |
| `related_paths` | Optional | Related repo paths strongly associated with the design document. |
| `internal_reference_paths` | Optional | Internal repository paths explicitly cited in the design document reference sections. |
| `external_reference_urls` | Optional | External URLs explicitly cited in the design document reference sections. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Process or Workflow
1. Add or update the design document under `docs/planning/design/`.
2. Update the human-readable design tracker in `docs/planning/design/design_tracking.md` in the same change set.
3. Add or update the design document front matter before generating or editing the machine-readable index entry.
4. Add or update the corresponding entry in the machine-readable design-document index.
5. Validate that every indexed `doc_path` and any listed related paths exist.
6. Validate the design-document index artifact against its published schema before treating the change as complete.

## Examples
- A feature design like `docs/planning/design/features/schema_resolution_and_index_search.md` should appear as a `feature_design` entry with its design title and summary.
- An implementation plan like `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` should appear as an `implementation_plan` entry and name the feature designs it depends on in `source_paths`.
- A directory README does not belong in this index because it is orientation, not a design document.

## Validation
- The design-document index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `docs/planning/design/`.
- Every implementation-plan entry should include `source_paths`.
- The reference-presence flags should reflect the actual design-document sections that cite internal or external sources.
- Reviewers should reject index entries that point to stale design docs or leave plan-to-design relationships implicit.

## Change Control
- Update this standard when the repository changes how design documents are tracked or looked up.
- Update the companion artifact schema, examples, and live design-document index in the same change set when the index family changes structurally.
- Update the human-readable design tracker in the same change set when indexed design documents change materially.

## References
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md)
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)
- [design_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/design_tracking.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/design_documents/README.md)

## Notes
- The human tracker is for quick scanning and editorial review.
- The machine index is for lookup, query, and future tooling. Neither surface replaces the design documents themselves.

## Updated At
- `2026-03-10T16:11:26Z`
