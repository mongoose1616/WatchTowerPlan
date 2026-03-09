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
owner: "repository_maintainer"
updated_at: "2026-03-09T18:45:00Z"
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
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)
- [prd_tracking.md](/home/j/WatchTowerPlan/docs/planning/prds/prd_tracking.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/prds/README.md)

## Guidance
- Model PRD tracking as an index, not as a registry.
- Treat the PRD index as a machine-readable lookup and trace surface rather than the authority for PRD content.
- Store published PRD indexes under `core/control_plane/indexes/prds/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published PRD index artifact.
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
| `updated_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, matching the PRD’s `Updated At` value. |
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

## Validation
- The PRD index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `docs/planning/prds/`.
- Every entry should have both `trace_id` and `prd_id`.
- The reference-presence flags should reflect the actual PRD sections that cite internal or external sources.
- Reviewers should reject entries that point to stale PRDs or omit durable IDs that exist in the PRD itself.

## Change Control
- Update this standard when the repository changes how PRDs are indexed or traced.
- Update the companion artifact schema, examples, and live PRD index in the same change set when the PRD-index family changes structurally.
- Update the human-readable PRD tracker in the same change set when indexed PRDs change materially.

## References
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [prd_tracking.md](/home/j/WatchTowerPlan/docs/planning/prds/prd_tracking.md)

## Updated At
- `2026-03-09T18:45:00Z`
