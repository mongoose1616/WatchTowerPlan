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
owner: "repository_maintainer"
updated_at: "2026-03-09T05:23:35Z"
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
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md)
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)
- [decision_tracking.md](/home/j/WatchTowerPlan/docs/planning/decisions/decision_tracking.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/decisions/README.md)

## Guidance
- Model decision tracking as an index, not as a registry.
- Treat the decision index as a machine-readable lookup and trace surface rather than the authority for decision content.
- Store published decision indexes under `core/control_plane/indexes/decisions/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published decision index artifact.
- Every decision index entry must point to an existing decision record under `docs/planning/decisions/`.
- Carry a shared `trace_id` in every entry so decisions can join to their PRDs, designs, and plans.
- Carry stable `decision_id` values in every entry.
- Distinguish lifecycle `record_status` from `decision_status`.
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
| `updated_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`, matching the decision document’s `Updated At` value. |
| `linked_prd_ids` | Optional | Related PRD IDs when they exist. |
| `linked_design_ids` | Optional | Related feature-design IDs when they exist. |
| `linked_plan_ids` | Optional | Related implementation-plan IDs when they exist. |
| `related_paths` | Optional | Related repository paths strongly associated with the decision. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short tracking notes. |

## Validation
- The decision index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a file under `docs/planning/decisions/`.
- Every entry should have both `trace_id` and `decision_id`.
- Reviewers should reject entries that point to stale decision records or conflate document lifecycle with decision outcome.

## Change Control
- Update this standard when the repository changes how decisions are indexed or traced.
- Update the companion artifact schema, examples, and live decision index in the same change set when the decision-index family changes structurally.
- Update the human-readable decision tracker in the same change set when indexed decision records change materially.

## References
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md)
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)

## Updated At
- `2026-03-09T05:23:35Z`
