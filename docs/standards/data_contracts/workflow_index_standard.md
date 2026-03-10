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
updated_at: "2026-03-10T06:39:00Z"
audience: "shared"
authority: "authoritative"
---

# Workflow Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable workflow indexes stored under `core/control_plane/indexes/workflows/`.

## Purpose
Provide a compact lookup and governance surface for workflow modules and their task-specific extra context without forcing tools to rescan `workflows/modules/**` directly for every query, routing, or review task.

## Scope
- Applies to machine-readable workflow index artifacts stored under `core/control_plane/indexes/workflows/`.
- Covers placement, entry shape, and how workflow-specific extra files to load should be published for query and review tooling.
- Does not replace the workflow modules themselves as the procedural authority.

## Use When
- Adding or materially updating a workflow module under `workflows/modules/**`.
- Building query or routing tooling that needs a compact view over workflow modules and their extra files to load.
- Auditing whether workflows publish only the task-specific extra files that materially change execution.

## Related Standards and Sources
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): workflow modules must keep their required headings and optional additional-load bullets aligned so the index can derive from them cleanly.
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md): distilled external guidance for keeping workflow modules small and publishing only task-specific extra files.
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
- Publish retrieval metadata that helps routing and query tooling distinguish workflow phase, task family, common trigger terms, and companion workflows.
- Capture whether the workflow explicitly publishes extra repo-local files to load and whether those files carry external authority transitively through governed local reference docs.
- Capture local governed reference-doc paths separately from broader internal path references.
- Derive workflow reference fields from the optional `Additional Files to Load` section rather than from generic routing-baseline boilerplate.
- When a workflow materially depends on external authority, prefer citing a local governed reference doc in `docs/references/**` rather than only raw external URLs.
- Do not treat `AGENTS.md`, `workflows/ROUTING_TABLE.md`, `workflows/modules/core.md`, or the generic workflow standards as task-specific additional-load files.
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
| `phase_type` | Required | Retrieval-oriented workflow phase such as `inspection`, `execution`, `validation`, or `reconciliation`. |
| `task_family` | Required | Stable retrieval-oriented task family such as `engineering_validation` or `traceability`. |
| `uses_internal_references` | Required | Whether the workflow publishes extra repo-local files to load. |
| `uses_external_references` | Required | Whether the workflow’s extra files to load depend on external authority, transitively through governed local reference docs. |
| `primary_risks` | Required | Short controlled list of the main failure modes this workflow is meant to manage. |
| `trigger_tags` | Required | Retrieval-oriented trigger terms used for workflow lookup. |
| `companion_workflow_ids` | Optional | Stable workflow identifiers that are commonly paired with this workflow. |
| `related_paths` | Optional | Internal repository paths explicitly related to the workflow entry, including task-specific extra load files. |
| `reference_doc_paths` | Optional | Governed reference-doc paths cited in `Additional Files to Load`. |
| `internal_reference_paths` | Optional | Internal repository paths cited in `Additional Files to Load`. |
| `external_reference_urls` | Optional | External URLs reached transitively through governed local reference docs cited in `Additional Files to Load`. |
| `aliases` | Optional | Retrieval-oriented alternate search terms. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Validation
- The workflow index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `workflows/modules/`.
- Every entry should have a stable `workflow_id`.
- `phase_type`, `task_family`, and `trigger_tags` should stay retrieval-oriented and should not duplicate whole workflow prose blocks.
- `reference_doc_paths` should point only to governed reference docs under `docs/references/`.
- `companion_workflow_ids`, when present, should resolve to other entries in the same workflow index artifact.
- Workflows that rely on external authority should cite a governed local reference doc rather than only raw external URLs.
- Generic routing-baseline files should not appear as workflow additional-load paths.
- Reviewers should reject entries that omit material task-specific additional files already present in the source workflow module.

## Change Control
- Update this standard when the repository changes how workflows are indexed, queried, or audited.
- Update the companion artifact schema, examples, live workflow index, command docs, and query or sync surfaces in the same change set when the workflow-index family changes structurally.

## References
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md)
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md)
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)

## Updated At
- `2026-03-10T06:39:00Z`
