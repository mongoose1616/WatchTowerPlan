---
id: "std.data_contracts.planning_catalog"
title: "Planning Catalog Standard"
summary: "This standard defines the role, structure, and boundary rules for the canonical machine-readable planning catalog stored under `core/control_plane/indexes/planning/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "planning_catalog"
  - "planning_index_family"
owner: "repository_maintainer"
updated_at: "2026-03-13T20:01:23Z"
audience: "shared"
authority: "authoritative"
---

# Planning Catalog Standard

## Summary
This standard defines the role, structure, and boundary rules for the canonical machine-readable planning catalog stored under `core/control_plane/indexes/planning/`.

## Purpose
- Provide one canonical machine-readable deep-planning join for one trace.
- Reduce machine join cost across PRDs, decisions, design docs, tasks, acceptance contracts, validation evidence, and per-trace coordination state.
- Make planning status semantics explicit so machine consumers do not confuse artifact lifecycle, initiative outcome, decision outcome, and task execution state.
- Keep the planning catalog derived so it does not compete with the source planning records, task records, contracts, or evidence artifacts as the governing authorities.

## Scope
- Applies to machine-readable planning-catalog artifacts stored under `core/control_plane/indexes/planning/`.
- Covers placement, root artifact fields, planning-entry shape, explicit status-field naming, and update expectations.
- Does not replace coordination, initiative, traceability, or family-specific indexes as supporting projections or source joins.

## Use When
- Building agent or automation workflows that need one canonical machine planning record after current-state coordination routing.
- Reviewing whether one trace has coherent PRD, design, task, acceptance, evidence, and next-step state without reopening several index families.
- Updating the canonical planning join or its query surface.

## Related Standards and Sources
- [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md): defines the shared derived-index baseline and discoverability contract this canonical planning join narrows.
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): defines the current-phase and per-trace coordination projection the planning catalog embeds.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): defines the trace-linked source join and initiative outcome fields the planning catalog must preserve.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): defines the contract-family source data the planning catalog summarizes.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): defines the evidence-family source data the planning catalog summarizes.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): defines the schema-catalog update expectations for this artifact family.
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md): governs the explicit status vocabulary the planning catalog should preserve rather than collapsing into one ambiguous field.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/planning/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Apply the shared planning-index-family baseline in [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md).
- Treat the planning catalog as the canonical deep-planning machine join after coordination identifies the trace of interest.
- Use explicit field names such as `artifact_status`, `initiative_status`, `record_status`, `decision_status`, and `task_status` instead of one generic `status` field inside planning entries.
- Embed one coordination section per trace rather than forcing machines to reopen the initiative index immediately after loading the planning catalog.
- Keep nested planning, task, acceptance, and evidence summaries compact. The planning catalog should reduce join cost, not mirror every field from every source family.
- Keep the catalog narrow to trace-linked planning context. Do not broaden it into a generic repository encyclopedia.
- Fail closed when the catalog cannot resolve the companion initiative entry for a traceability record.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the planning-catalog artifact family. |
| `id` | Required | Stable identifier for the planning catalog artifact. |
| `title` | Required | Human-readable title for the artifact. |
| `status` | Required | Use the governed artifact lifecycle vocabulary for the catalog artifact itself. |
| `entries` | Required | Array of canonical planning records keyed by trace. |

### Planning entry fields
| Field | Requirement | Notes |
|---|---|---|
| `trace_id` | Required | Shared umbrella identifier for the trace. |
| `title` | Required | Human-readable trace title. |
| `summary` | Required | Concise description of the trace. |
| `artifact_status` | Required | Lifecycle state mirrored from the traceability entry. |
| `initiative_status` | Required | Initiative outcome mirrored from the traceability entry. |
| `updated_at` | Required | RFC 3339 UTC timestamp matching the latest governing source in the joined record. |
| `coordination` | Required | Per-trace coordination section containing `current_phase`, next-step guidance, open-task counts, and current owner projection. |
| `prds` | Optional | Compact PRD summaries with `artifact_status` and linked IDs when present. |
| `decisions` | Optional | Compact decision summaries with explicit `record_status` and `decision_status`. |
| `design_documents` | Optional | Compact feature-design and implementation-plan summaries with `artifact_status`. |
| `tasks` | Optional | Compact task summaries with both `artifact_status` and `task_status`. |
| `acceptance_contracts` | Optional | Compact acceptance-contract summaries including linked acceptance IDs and required validator IDs when present. |
| `validation_evidence` | Optional | Compact evidence summaries including explicit overall result and linked check IDs when present. |
| `prd_ids`, `decision_ids`, `design_ids`, `plan_ids`, `task_ids`, `requirement_ids`, `acceptance_ids`, `acceptance_contract_ids`, `evidence_ids`, `validator_ids` | Optional | Top-level identifier lists preserved from trace-linked sources for lookup and compatibility. |
| `related_paths` | Optional | Consolidated related repository paths associated with the planning record. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short carried-forward notes from the traceability source. |
| `closed_at`, `closure_reason`, `superseded_by_trace_id` | Optional | Required when the initiative status is terminal and especially when superseded. |

## Operationalization
- `Modes`: `artifact`; `schema`
- `Operational Surfaces`: `core/control_plane/indexes/planning/`; `core/control_plane/schemas/artifacts/`; `core/control_plane/indexes/planning/README.md`; `core/control_plane/examples/valid/indexes/planning_catalog*.example.json`; `core/control_plane/examples/invalid/indexes/planning_catalog*.example.json`

## Validation
- In addition to the shared planning-index-family validation contract:
- Every planning entry should correspond to one traceability entry and one initiative entry.
- The coordination section should agree with the current initiative index for the same trace.
- Nested summaries should preserve explicit status semantics rather than collapsing them into a generic `status` field.
- Top-level identifier lists should agree with the traceability record when those identifiers exist there.

## Change Control
- In addition to the shared planning-index-family change-control contract:
- Update this standard when the repository changes the canonical deep-planning join boundary or planning-entry shape.
- Update the query and navigation docs in the same change set when canonical planning precedence changes materially.

## References
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md)
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md)
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md)
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/planning/README.md)

## Updated At
- `2026-03-13T20:01:23Z`
