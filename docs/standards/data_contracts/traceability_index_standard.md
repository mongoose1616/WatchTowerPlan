---
id: "std.data_contracts.traceability_index"
title: "Traceability Index Standard"
summary: "This standard defines the unified machine-readable traceability index stored under `core/control_plane/indexes/traceability/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "traceability_index"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:23:35Z"
audience: "shared"
authority: "authoritative"
---

# Traceability Index Standard

## Summary
This standard defines the unified machine-readable traceability index stored under `core/control_plane/indexes/traceability/`.

## Purpose
- Provide one compact join surface for PRDs, decisions, designs, implementation plans, acceptance contracts, validators, and validation evidence.
- Let Python query services and workflows answer trace questions without parsing multiple indexes and documents ad hoc.
- Complete the baseline machine-readable trace chain established by the repository planning model.

## Scope
- Applies to traceability index artifacts stored under `core/control_plane/indexes/traceability/`.
- Covers placement, root fields, entry fields, and synchronization expectations with family-specific indexes.
- Does not replace PRD, decision, design, or evidence artifacts as their primary authoritative surfaces.
- Does not replace human-readable planning trackers.

## Use When
- Publishing or refreshing the unified join surface for traced initiatives.
- Reviewing whether downstream trace links are discoverable without prose parsing.
- Adding a new durable artifact family that should participate in end-to-end traceability.

## Related Standards and Sources
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [prd_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/prd_index_standard.md)
- [decision_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/decision_index_standard.md)
- [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/design_document_index_standard.md)
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md)
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md)
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/README.md)

## Guidance
- Model end-to-end trace lookup as an index, not a registry.
- Store published traceability indexes under `core/control_plane/indexes/traceability/`.
- Use JSON for the published traceability index artifact.
- Keep family-specific indexes as their local lookup surfaces and use the unified traceability index as the cross-family join layer.
- Every traceability entry should publish:
  - `trace_id`
  - a concise title and summary
  - upstream planning IDs
  - downstream acceptance, validator, and evidence IDs when they exist
  - key related paths and an `updated_at` RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`
- Keep one traceability entry per shared `trace_id`.
- Update the traceability index in the same change set when a traced artifact is added, renamed, removed, or materially retargeted.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the traceability-index artifact family. |
| `id` | Required | Stable identifier for the traceability index artifact. |
| `title` | Required | Human-readable title. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of per-trace join records. |

### Trace entry fields
| Field | Requirement | Notes |
|---|---|---|
| `trace_id` | Required | Shared trace identifier. |
| `title` | Required | Human-readable trace title. |
| `summary` | Required | Concise description of what the traced initiative covers. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `updated_at` | Required | Last meaningful content update RFC 3339 UTC timestamp for the joined record. |
| `prd_ids` | Optional | Linked PRD identifiers. |
| `decision_ids` | Optional | Linked decision identifiers. |
| `design_ids` | Optional | Linked feature-design identifiers. |
| `plan_ids` | Optional | Linked implementation-plan identifiers. |
| `requirement_ids` | Optional | Linked requirement identifiers. |
| `acceptance_ids` | Optional | Linked acceptance identifiers. |
| `acceptance_contract_ids` | Optional | Linked acceptance contract identifiers. |
| `validator_ids` | Optional | Validators materially relevant to the trace. |
| `evidence_ids` | Optional | Linked validation-evidence artifacts. |
| `related_paths` | Optional | High-signal repository paths related to the trace. |
| `tags` | Optional | Retrieval-oriented tags. |
| `notes` | Optional | Short join note. |

## Process or Workflow
1. Gather the traced artifact IDs from PRD, decision, design, implementation-plan, acceptance, and evidence surfaces.
2. Publish or refresh the matching traceability entry under the shared `trace_id`.
3. Validate the index artifact against its published schema.
4. Check that linked IDs and related paths still resolve.
5. Update the family-specific indexes in the same change set if the traceability refresh reveals drift there.

## Examples
- A core Python foundation trace should join the PRD, workspace-root decision, feature designs, implementation plan, acceptance contract, and validation evidence under `trace.core_python_foundation`.
- A future trace with no decision record can omit `decision_ids` while still joining PRD, design, plan, and evidence artifacts.
- A generic folder README does not belong in the traceability index unless it is a high-signal related path for a traced initiative.

## Validation
- The traceability index should validate against its published artifact schema.
- Linked IDs should exist in the relevant family-specific indexes or artifacts.
- `related_paths` should exist in the repository.
- Reviewers should reject traceability entries that point to stale IDs or that duplicate detailed artifact semantics better kept in the family-specific surfaces.

## Change Control
- Update this standard when the repository changes the joined trace model materially or adds a new first-class traced family that belongs in the unified index.
- Update the companion schema, examples, and live traceability index in the same change set when this family changes structurally.
- Update related family-specific indexes and evidence artifacts in the same change set when a trace entry changes materially.

## References
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/README.md)

## Notes
- This index is the machine-readable join surface, not the sole authoritative source of the linked artifacts themselves.

## Updated At
- `2026-03-09T05:23:35Z`
