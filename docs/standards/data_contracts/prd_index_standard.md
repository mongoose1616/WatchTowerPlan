---
id: "std.data_contracts.prd_index"
title: "PRD Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable PRD indexes stored under `core/control_plane/indexes/prds/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "prd_index"
  - "planning_index_family"
owner: "repository_maintainer"
updated_at: "2026-03-13T20:01:23Z"
audience: "shared"
authority: "authoritative"
---

# PRD Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable PRD indexes stored under `core/control_plane/indexes/prds/`.

## Purpose
Provide a compact lookup and tracking surface for PRDs, their trace IDs, and their requirement-level anchors without forcing tooling to scan Markdown directly.

## Scope
- Applies to machine-readable PRD index artifacts stored under `core/control_plane/indexes/prds/`.
- Covers placement, entry shape, update expectations, and the relationship between the index and the human-readable PRD tracker in `docs/planning/prds/`.
- Does not replace the PRD documents themselves.

## Use When
- Adding a new PRD under `docs/planning/prds/`.
- Refreshing PRD-tracking data after a PRD is renamed, removed, or materially retargeted.
- Building lookup or traceability tooling that needs a compact machine-readable view over the PRD corpus.

## Related Standards and Sources
- [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md): defines the shared derived-index baseline and discoverability contract this PRD-family standard narrows.
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [prd_tracking.md](/home/j/WatchTowerPlan/docs/planning/prds/prd_tracking.md): companion planning or design surface this standard should remain consistent with.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/prds/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Apply the shared planning-index-family baseline in [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md).
- Every PRD index entry must point to an existing PRD under `docs/planning/prds/`.
- Carry a shared `trace_id` in every entry so PRDs can join to decisions, designs, and plans.
- Carry stable `prd_id` values in every entry.
- Carry durable `requirement_ids` and `acceptance_ids` when the PRD publishes them.
- Capture whether the PRD explicitly used internal or external references so reference use is queryable without reparsing Markdown.
- Keep the human-readable PRD tracker and the machine-readable PRD index aligned in the same change set.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the PRD-index artifact family. |
| `id` | Required | Stable identifier for the PRD index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of PRD records. |

### PRD entry fields
| Field | Requirement | Notes |
|---|---|---|
| `trace_id` | Required | Shared umbrella identifier for the traced initiative. |
| `prd_id` | Required | Stable PRD identifier. |
| `title` | Required | Human-readable PRD title. |
| `summary` | Required | Concise description of the PRD. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `doc_path` | Required | Repository-relative path to the PRD. |
| `updated_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, matching the PRD front matter `updated_at` value and the `Record Metadata` value. |
| `uses_internal_references` | Required | Whether the PRD explicitly cited internal repository references. |
| `uses_external_references` | Required | Whether the PRD explicitly cited external sources. |
| `requirement_ids` | Optional | Durable requirement identifiers published by the PRD. |
| `acceptance_ids` | Optional | Durable acceptance identifiers published by the PRD. |
| `linked_decision_ids` | Optional | Related decision IDs when they exist. |
| `linked_design_ids` | Optional | Related feature-design IDs when they exist. |
| `linked_plan_ids` | Optional | Related implementation-plan IDs when they exist. |
| `related_paths` | Optional | Related repository paths strongly associated with the PRD. |
| `internal_reference_paths` | Optional | Internal repository paths explicitly cited in the PRD reference sections. |
| `external_reference_urls` | Optional | External URLs explicitly cited in the PRD reference sections. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Operationalization
- `Modes`: `artifact`; `schema`; `documentation`
- `Operational Surfaces`: `core/control_plane/indexes/prds/`; `core/control_plane/schemas/artifacts/`; `core/control_plane/indexes/prds/README.md`; `core/control_plane/examples/valid/indexes/prd_index*.example.json`; `core/control_plane/examples/invalid/indexes/prd_index*.example.json`; `docs/planning/prds/`

## Validation
- In addition to the shared planning-index-family validation contract:
- Every `doc_path` should exist and point to a file under `docs/planning/prds/`.
- Every entry should have both `trace_id` and `prd_id`.
- The reference-presence flags should reflect the actual PRD sections that cite internal or external sources.
- Reviewers should reject entries that point to stale PRDs or omit durable IDs that exist in the PRD itself.

## Change Control
- In addition to the shared planning-index-family change-control contract:
- Update this standard when the repository changes how PRDs are indexed or traced.
- Update the human-readable PRD tracker in the same change set when indexed PRDs change materially.

## References
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [prd_tracking.md](/home/j/WatchTowerPlan/docs/planning/prds/prd_tracking.md)

## Updated At
- `2026-03-13T20:01:23Z`
