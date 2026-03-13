---
id: "std.data_contracts.decision_index"
title: "Decision Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable decision indexes stored under `core/control_plane/indexes/decisions/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "decision_index"
  - "planning_index_family"
owner: "repository_maintainer"
updated_at: "2026-03-13T20:01:23Z"
audience: "shared"
authority: "authoritative"
---

# Decision Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable decision indexes stored under `core/control_plane/indexes/decisions/`.

## Purpose
Provide a compact lookup and tracking surface for durable decision records, their shared trace IDs, and their outcome states without forcing tooling to scan Markdown directly.

## Scope
- Applies to machine-readable decision index artifacts stored under `core/control_plane/indexes/decisions/`.
- Covers placement, entry shape, update expectations, and the relationship between the index and the human-readable decision tracker in `docs/planning/decisions/`.
- Does not replace the decision documents themselves.

## Use When
- Adding a new decision record under `docs/planning/decisions/`.
- Refreshing decision-tracking data after a decision record is renamed, removed, or materially retargeted.
- Building lookup or traceability tooling that needs a compact machine-readable view over the decision corpus.

## Related Standards and Sources
- [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md): defines the shared derived-index baseline and discoverability contract this decision-family standard narrows.
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [decision_tracking.md](/home/j/WatchTowerPlan/docs/planning/decisions/decision_tracking.md): companion planning or design surface this standard should remain consistent with.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/decisions/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Apply the shared planning-index-family baseline in [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md).
- Every decision index entry must point to an existing decision record under `docs/planning/decisions/`.
- Carry a shared `trace_id` in every entry so decisions can join to their PRDs, designs, and plans.
- Carry stable `decision_id` values in every entry.
- Distinguish lifecycle `record_status` from `decision_status`.
- Capture whether the decision explicitly used internal or external references so reference use is queryable without reparsing Markdown.
- Capture the subset of references that materially shaped the outcome so “applied” source use stays auditable instead of only cited.
- Keep the human-readable decision tracker and the machine-readable decision index aligned in the same change set.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the decision-index artifact family. |
| `id` | Required | Stable identifier for the decision index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of decision records. |

### Decision entry fields
| Field | Requirement | Notes |
|---|---|---|
| `trace_id` | Required | Shared umbrella identifier for the traced initiative. |
| `decision_id` | Required | Stable decision identifier. |
| `title` | Required | Human-readable decision title. |
| `summary` | Required | Concise description of the decision. |
| `record_status` | Required | Use the governed lifecycle vocabulary for the document record. |
| `decision_status` | Required | Use the decision outcome vocabulary from the decision-capture standard. |
| `doc_path` | Required | Repository-relative path to the decision record. |
| `updated_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, matching the decision record front matter `updated_at` value and the `Record Metadata` value. |
| `uses_internal_references` | Required | Whether the decision explicitly cited internal repository references. |
| `uses_external_references` | Required | Whether the decision explicitly cited external sources. |
| `linked_prd_ids` | Optional | Related PRD IDs when they exist. |
| `linked_design_ids` | Optional | Related feature-design IDs when they exist. |
| `linked_plan_ids` | Optional | Related implementation-plan IDs when they exist. |
| `related_paths` | Optional | Related repository paths strongly associated with the decision. |
| `internal_reference_paths` | Optional | Internal repository paths explicitly cited in the decision references. |
| `applied_reference_paths` | Optional | Internal repository paths explicitly used in `Applied References and Implications`. |
| `external_reference_urls` | Optional | External URLs explicitly cited in the decision references. |
| `applied_external_reference_urls` | Optional | External URLs explicitly used in `Applied References and Implications`. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Operationalization
- `Modes`: `artifact`; `schema`; `documentation`
- `Operational Surfaces`: `core/control_plane/indexes/decisions/`; `core/control_plane/schemas/artifacts/`; `core/control_plane/indexes/decisions/README.md`; `core/control_plane/examples/valid/indexes/decision_index*.example.json`; `core/control_plane/examples/invalid/indexes/decision_index*.example.json`; `docs/planning/decisions/`

## Validation
- In addition to the shared planning-index-family validation contract:
- Every `doc_path` should exist and point to a file under `docs/planning/decisions/`.
- Every entry should have both `trace_id` and `decision_id`.
- The reference-presence flags should reflect the actual decision sections that cite internal or external sources.
- Applied reference fields should reflect the actual `Applied References and Implications` section rather than inferred prose.
- Reviewers should reject entries that point to stale decision records or conflate document lifecycle with decision outcome.

## Change Control
- In addition to the shared planning-index-family change-control contract:
- Update this standard when the repository changes how decisions are indexed or traced.
- Update the human-readable decision tracker in the same change set when indexed decision records change materially.

## References
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md)
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)

## Updated At
- `2026-03-13T20:01:23Z`
