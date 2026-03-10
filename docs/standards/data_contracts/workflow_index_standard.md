---
id: "std.data_contracts.workflow_index"
title: "Workflow Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable workflow indexes stored under `core/control_plane/indexes/workflows/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "workflow_index"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:59:23Z"
audience: "shared"
authority: "authoritative"
---

# Workflow Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable workflow indexes stored under `core/control_plane/indexes/workflows/`.

## Purpose
Provide a compact lookup and governance surface for workflow modules without forcing tools to rescan `workflows/modules/**` directly for every query, routing, or review task.

## Scope
- Applies to machine-readable workflow index artifacts stored under `core/control_plane/indexes/workflows/`.
- Covers placement, entry shape, and how workflow reference use should be published for query and review tooling.
- Does not replace the workflow modules themselves as the procedural authority.

## Use When
- Adding or materially updating a workflow module under `workflows/modules/**`.
- Building query or routing tooling that needs a compact view over workflow modules and their governing sources.
- Auditing whether workflows cite the correct internal standards, references, or canonical files.

## Related Standards and Sources
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): workflow modules must keep their required headings and explained source bullets aligned so the index can derive from them cleanly.
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md): workflow reference capture should stay aligned with the broader governed reference model.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): the workflow index complements path lookup with workflow-specific retrieval.
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md): published workflow indexes use JSON as the governed machine-readable format.

## Guidance
- Model workflow lookup as an index, not as a registry.
- Treat the workflow index as a machine-readable lookup surface rather than the authority for workflow behavior.
- Store published workflow indexes under `core/control_plane/indexes/workflows/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published workflow-index artifact.
- Every workflow index entry must point to an existing workflow module under `workflows/modules/`.
- Carry stable `workflow_id` values derived from the workflow module filename in the form `workflow.<module_name>`.
- Capture whether the workflow explicitly uses internal references or external authority.
- Capture local governed reference-doc paths separately from broader internal path references.
- When a workflow materially depends on external authority, prefer citing a local governed reference doc in `docs/references/**` rather than only raw external URLs.
- Keep the workflow index aligned with the workflow corpus in the same change set.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the workflow-index artifact family. |
| `id` | Required | Stable identifier for the workflow index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of workflow records. |

### Workflow entry fields
| Field | Requirement | Notes |
|---|---|---|
| `workflow_id` | Required | Stable workflow identifier derived from the workflow module filename. |
| `title` | Required | Human-readable workflow title from the document H1. |
| `summary` | Required | Concise description derived from the workflow `Purpose` section. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `doc_path` | Required | Repository-relative path to the workflow module. |
| `uses_internal_references` | Required | Whether the workflow explicitly cites internal repository sources. |
| `uses_external_references` | Required | Whether the workflow explicitly depends on external authority, directly or through governed local reference docs. |
| `related_paths` | Optional | Internal repository paths explicitly cited by the workflow. |
| `reference_doc_paths` | Optional | Governed reference-doc paths cited by the workflow. |
| `internal_reference_paths` | Optional | Internal repository paths cited by the workflow’s governing-source section. |
| `external_reference_urls` | Optional | External URLs cited by the workflow, directly or transitively through governed local reference docs. |
| `aliases` | Optional | Retrieval-oriented alternate search terms. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Validation
- The workflow index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `workflows/modules/`.
- Every entry should have a stable `workflow_id`.
- `reference_doc_paths` should point only to governed reference docs under `docs/references/`.
- Workflows that rely on external authority should cite a governed local reference doc rather than only raw external URLs.
- Reviewers should reject entries that omit material governing sources already present in the source workflow module.

## Change Control
- Update this standard when the repository changes how workflows are indexed, queried, or audited.
- Update the companion artifact schema, examples, live workflow index, command docs, and query or sync surfaces in the same change set when the workflow-index family changes structurally.

## References
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md)
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)

## Updated At
- `2026-03-09T23:59:23Z`
