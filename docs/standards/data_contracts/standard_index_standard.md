---
id: "std.data_contracts.standard_index"
title: "Standard Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable standard indexes stored under `core/control_plane/indexes/standards/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "standard_index"
owner: "repository_maintainer"
updated_at: "2026-03-12T01:02:00Z"
audience: "shared"
authority: "authoritative"
---

# Standard Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable standard indexes stored under `core/control_plane/indexes/standards/`.

## Purpose
Provide a compact lookup and governance surface for repository standards and best-practice documents without forcing tooling to scan Markdown directly.

## Scope
- Applies to machine-readable standard index artifacts stored under `core/control_plane/indexes/standards/`.
- Covers placement, entry shape, update expectations, and the relationship between the index and governed standards under `docs/standards/**`.
- Does not replace the standard documents themselves as the normative authority.

## Use When
- Adding or materially updating a standard under `docs/standards/**`.
- Building query, retrieval, or review tooling that needs a compact view over the standards corpus.
- Auditing whether standards use internal references, external references, and repo-local distilled references consistently.

## Related Standards and Sources
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/standards/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Model standard lookup as an index, not as a registry.
- Treat the standard index as a machine-readable lookup and governance-audit surface rather than the authority for standard content.
- Store published standard indexes under `core/control_plane/indexes/standards/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published standard-index artifact.
- Every standard index entry must point to an existing governed standard under `docs/standards/`.
- Carry stable `standard_id` values from governed front matter.
- Record the top-level standards category from the document path, such as `data_contracts`, `documentation`, `engineering`, `governance`, `metadata`, or `workflows`.
- Capture whether the standard explicitly uses internal references or external authority.
- Capture the standard owner and the authored `applies_to` targets from standard front matter instead of hiding that information behind generic related-path retrieval.
- Capture the subset of references that materially shape the standard so applied source use is auditable instead of only cited.
- Capture local reference-doc paths so repo tooling can distinguish raw internal citations from links into `docs/references/**`.
- Capture compact operationalization metadata so tooling can answer which modes and repository surfaces currently enforce or embody a standard, using exact repo paths, directories, or bounded repo-relative glob patterns when a standard governs a repeating file family.
- When a standard materially depends on external authority, prefer citing a local governed reference doc in `docs/references/**` rather than only raw external URLs.
- Keep the index aligned with the standards corpus in the same change set.

## Operationalization
- `Modes`: `sync`; `query`; `artifact`; `schema`
- `Operational Surfaces`: `core/python/src/watchtower_core/repo_ops/sync/standard_index.py`; `core/python/src/watchtower_core/repo_ops/query/standards.py`; `core/control_plane/indexes/standards/`; `core/control_plane/schemas/artifacts/`

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the standard-index artifact family. |
| `id` | Required | Stable identifier for the standard index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of standard records. |

### Standard entry fields
| Field | Requirement | Notes |
|---|---|---|
| `standard_id` | Required | Stable standard identifier from governed front matter. |
| `category` | Required | Top-level standards category derived from the document path. |
| `title` | Required | Human-readable standard title. |
| `summary` | Required | Concise description of the standard. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `owner` | Required | Standard owner from governed front matter. |
| `doc_path` | Required | Repository-relative path to the standard document. |
| `updated_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, matching the standard document’s `Updated At` value. |
| `uses_internal_references` | Required | Whether the standard explicitly cites internal repository references. |
| `uses_external_references` | Required | Whether the standard explicitly depends on external authority, directly or through cited local reference docs. |
| `applies_to` | Optional | Full authored `applies_to` values from standard front matter, including path or concept entries. |
| `related_paths` | Optional | Repository paths from front matter `applies_to` or other strongly related paths. |
| `reference_doc_paths` | Optional | Paths to governed local reference docs cited by the standard. |
| `internal_reference_paths` | Optional | Internal repository paths explicitly cited in the standard’s source sections. |
| `applied_reference_paths` | Optional | Internal repository paths explicitly used in `Related Standards and Sources`. |
| `external_reference_urls` | Optional | External URLs explicitly cited by the standard or transitively inherited from cited local reference docs. |
| `applied_external_reference_urls` | Optional | External URLs explicitly used in `Related Standards and Sources`, directly or through cited local reference docs. |
| `operationalization_modes` | Required | Compact lower_snake_case modes such as `validation`, `sync`, or `workflow`. |
| `operationalization_paths` | Required | Repository paths or bounded repo-relative glob patterns for the operational surfaces named in the standard’s `Operationalization` section. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Validation
- The standard index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `docs/standards/`.
- Every entry should have a stable `standard_id`.
- Every entry should carry the authored `owner` value and, when present, the full `applies_to` list from standard front matter.
- `reference_doc_paths` should point only to governed reference docs under `docs/references/`.
- `operationalization_modes` should be compact lower_snake_case values, and every `operationalization_path` should resolve to a real repository surface or be a bounded repo-relative glob pattern that matches one or more live repository surfaces.
- Standards that rely on external authority should cite a governed local reference doc rather than only raw external URLs.
- Applied reference fields should reflect the actual `Related Standards and Sources` section rather than inferred prose.
- Reviewers should reject entries that point to stale standard docs or omit material reference usage already present in the source doc.

## Change Control
- Update this standard when the repository changes how standards are indexed, queried, or audited.
- Update the companion artifact schema, examples, live standard index, command docs, and query or sync surfaces in the same change set when the standard-index family changes structurally.

## References
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md)

## Updated At
- `2026-03-12T01:02:00Z`
