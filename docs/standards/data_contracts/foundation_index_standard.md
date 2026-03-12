---
id: "std.data_contracts.foundation_index"
title: "Foundation Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable foundation indexes stored under `core/control_plane/indexes/foundations/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "foundation_index"
owner: "repository_maintainer"
updated_at: "2026-03-12T23:12:00Z"
audience: "shared"
authority: "authoritative"
---

# Foundation Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable foundation indexes stored under `core/control_plane/indexes/foundations/`.

## Purpose
Provide a compact lookup and governance-audit surface for the repository's intent-layer foundation documents without forcing tooling to rescan Markdown directly.

## Scope
- Applies to machine-readable foundation index artifacts stored under `core/control_plane/indexes/foundations/`.
- Covers placement, entry shape, reverse-citation expectations, and the relationship between the index and governed foundation docs under `docs/foundations/**`.
- Does not replace the foundation documents themselves as the normative intent authority.

## Use When
- Adding or materially updating a governed foundation document under `docs/foundations/**`.
- Building query or review tooling that needs a compact view over the foundations corpus.
- Auditing where foundation documents are currently cited or applied across standards, workflows, and planning surfaces.

## Related Standards and Sources
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md): foundation docs must publish stable metadata, references, and timestamps so the index can derive from them cleanly.
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md): reverse-citation behavior should stay aligned with the broader reference-audit model.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): the foundation index complements path lookup with intent-specific retrieval and audit signals.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): foundation index timestamps must use UTC RFC 3339 values.
- [README.md](/home/j/WatchTowerPlan/docs/foundations/README.md): family entrypoint and inventory surface for the governed foundation documents this index summarizes.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/foundations/README.md): family entrypoint and inventory surface for the published foundation-index artifacts.

## Guidance
- Model foundation lookup as an index, not as a registry.
- Treat the foundation index as a machine-readable lookup and governance-audit surface rather than the authority for foundation content.
- Store published foundation indexes under `core/control_plane/indexes/foundations/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published foundation-index artifact.
- Every foundation index entry must point to an existing governed foundation document under `docs/foundations/`.
- Carry stable `foundation_id` values from governed front matter.
- Carry front-matter `audience` into the index so intent-layer routing is queryable without reparsing Markdown.
- Capture reverse citation and reverse application paths so repo tooling can answer which standards, workflows, and planning docs currently rely on a foundation doc.
- When a foundation doc depends on external authority, prefer citing a local governed reference doc in `docs/references/**` rather than only raw external URLs.
- Publish compact operationalization metadata that covers the authoritative sync, query, and bounded documentation surfaces for the foundation-index family so tooling can resolve the contract from the surfaces engineers actually touch.
- Keep the index aligned with the foundations corpus in the same change set.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the foundation-index artifact family. |
| `id` | Required | Stable identifier for the foundation index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of foundation records. |

### Foundation entry fields
| Field | Requirement | Notes |
|---|---|---|
| `foundation_id` | Required | Stable foundation identifier from governed front matter. |
| `title` | Required | Human-readable foundation title. |
| `summary` | Required | Concise description of the foundation document. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `audience` | Required | Retrieval-oriented readership signal mirrored from front matter. |
| `authority` | Required | Retrieval and precedence signal from front matter. |
| `doc_path` | Required | Repository-relative path to the foundation document. |
| `updated_at` | Required | RFC 3339 UTC timestamp matching the foundation doc’s `Updated At` value. |
| `uses_internal_references` | Required | Whether the foundation doc explicitly cites internal repository references. |
| `uses_external_references` | Required | Whether the foundation doc explicitly depends on external authority, directly or through cited local reference docs. |
| `reference_doc_paths` | Optional | Paths to governed local reference docs cited by the foundation doc. |
| `internal_reference_paths` | Optional | Internal repository paths explicitly cited in the foundation doc’s `References` section. |
| `external_reference_urls` | Optional | External URLs explicitly cited by the foundation doc or transitively inherited from cited local reference docs. |
| `cited_by_paths` | Optional | Standards, workflows, or planning docs that cite the foundation doc. |
| `applied_by_paths` | Optional | Standards, workflows, or planning docs that apply the foundation doc in an explained applied-reference section. |
| `related_paths` | Optional | Repository paths from front matter `applies_to` or other strongly related paths. |
| `aliases` | Optional | Retrieval-oriented alternate search terms. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Operationalization
- `Modes`: `sync`; `query`; `documentation`; `schema`; `artifact`
- `Operational Surfaces`: `core/python/src/watchtower_core/repo_ops/sync/foundation_index.py`; `core/python/src/watchtower_core/repo_ops/query/foundations.py`; `docs/commands/core_python/watchtower_core_query_foundations.md`; `docs/commands/core_python/watchtower_core_sync_foundation_index.md`; `core/control_plane/schemas/artifacts/`; `core/control_plane/indexes/foundations/`; `core/control_plane/indexes/foundations/README.md`; `core/control_plane/examples/valid/indexes/foundation_index*.example.json`; `core/control_plane/examples/invalid/indexes/foundation_index*.example.json`

## Validation
- The foundation index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `docs/foundations/`.
- Every entry should have a stable `foundation_id`.
- Every entry should preserve the governed front-matter `audience` value.
- `reference_doc_paths` should point only to governed reference docs under `docs/references/`.
- Reverse citation and application paths should point only to Markdown docs under `docs/**` or `workflows/**`.
- Operationalization should explicitly cover the authoritative sync/query owners and the bounded family documentation surfaces that explain how to read or rebuild the foundation index.
- Reviewers should reject entries that omit material citation or application usage already present in the source docs.

## Change Control
- Update this standard when the repository changes how foundation documents are indexed, queried, or audited.
- Update the companion artifact schema, examples, live foundation index, family README, command docs, and query or sync surfaces in the same change set when the foundation-index family changes structurally.

## References
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md)
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/foundations/README.md)

## Updated At
- `2026-03-12T23:12:00Z`
