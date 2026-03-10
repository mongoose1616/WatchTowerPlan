---
id: "std.data_contracts.reference_index"
title: "Reference Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable reference indexes stored under `core/control_plane/indexes/references/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "reference_index"
owner: "repository_maintainer"
updated_at: "2026-03-10T00:55:31Z"
audience: "shared"
authority: "authoritative"
---

# Reference Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable reference indexes stored under `core/control_plane/indexes/references/`.

## Purpose
Provide a compact lookup and discovery surface for governed reference documents, their canonical upstream authority, their local repository touchpoints, and their downstream citation footprint without forcing tooling to scan Markdown directly.

## Scope
- Applies to machine-readable reference index artifacts stored under `core/control_plane/indexes/references/`.
- Covers placement, entry shape, update expectations, and the relationship between the index and the authored reference documents under `docs/references/`.
- Does not replace the reference documents themselves.

## Use When
- Adding a new governed reference under `docs/references/`.
- Refreshing reference-tracking data after a reference document is renamed, removed, or materially retargeted.
- Building lookup or routing tooling that needs a compact machine-readable view over the reference corpus.

## Related Standards and Sources
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md): family entrypoint and inventory surface this standard should stay aligned with.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/references/README.md): family entrypoint and inventory surface this standard should stay aligned with.
## Guidance
- Model reference lookup as an index, not as a registry.
- Treat the reference index as a machine-readable lookup surface rather than the authority for reference content.
- Store published reference indexes under `core/control_plane/indexes/references/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published reference index artifact.
- Every reference index entry must point to an existing governed reference under `docs/references/`.
- Carry stable `reference_id` values from the governed reference front matter.
- Capture whether the reference document publishes internal repository touchpoints and external canonical upstream sources.
- Capture the canonical upstream URLs explicitly so tooling can trace the local reference corpus back to its source authority.
- Capture reverse citation paths so tooling can answer where a governed reference is cited or applied across foundations, standards, workflows, and planning docs.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the reference-index artifact family. |
| `id` | Required | Stable identifier for the reference index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of reference records. |

### Reference entry fields
| Field | Requirement | Notes |
|---|---|---|
| `reference_id` | Required | Stable reference identifier from governed front matter. |
| `title` | Required | Human-readable reference title. |
| `summary` | Required | Concise description of the reference document. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `doc_path` | Required | Repository-relative path to the reference document. |
| `updated_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, matching the reference document’s `Updated At` value. |
| `uses_internal_references` | Required | Whether the reference document explicitly maps to local repository surfaces. |
| `uses_external_references` | Required | Whether the reference document explicitly publishes external canonical upstream URLs. |
| `canonical_upstream_urls` | Required | External authority URLs from the `Canonical Upstream` section. |
| `cited_by_paths` | Optional | Governed Markdown paths under `docs/**` or `workflows/**` that cite the reference doc or its canonical upstream URLs. |
| `applied_by_paths` | Optional | Governed Markdown paths under `docs/**` or `workflows/**` that apply the reference in an applied-reference section or a workflow `Additional Files to Load` section. |
| `related_paths` | Optional | Internal repository paths explicitly mapped from the reference document. |
| `aliases` | Optional | Retrieval-oriented aliases from front matter or curated index data. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Validation
- The reference index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `docs/references/`.
- Every entry should have a stable `reference_id`.
- Every entry should publish at least one canonical upstream URL.
- The internal and external reference flags should reflect the actual reference document sections rather than inferred prose.
- Reverse citation paths should point only to real governed documents or workflow modules that cite or apply the reference.

## Change Control
- Update this standard when the repository changes how references are indexed or queried.
- Update the companion artifact schema, examples, and live reference index in the same change set when the reference-index family changes structurally.
- Update reference-command docs and lookup surfaces in the same change set when the reference index changes how engineers or agents are expected to use it.

## References
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)

## Updated At
- `2026-03-10T00:55:31Z`
