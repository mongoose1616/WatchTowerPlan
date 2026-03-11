---
id: "std.data_contracts.validation_evidence"
title: "Validation Evidence Standard"
summary: "This standard defines committed validation-evidence artifacts stored under `core/control_plane/ledgers/validation_evidence/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "validation_evidence"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
---

# Validation Evidence Standard

## Summary
This standard defines committed validation-evidence artifacts stored under `core/control_plane/ledgers/validation_evidence/`.

## Purpose
- Provide durable machine-readable records of validation outcomes tied to traces, acceptance items, validators, and governed artifacts.
- Keep validation history reviewable without turning runtime logs into long-lived control-plane state.
- Establish the downstream half of the trace chain after PRDs, decisions, designs, and plans.

## Scope
- Applies to validation-evidence ledger artifacts stored under `core/control_plane/ledgers/validation_evidence/`.
- Covers placement, required fields, result vocabulary, and trace-link expectations.
- Does not define validation policy or validator identity; those remain in policies and registries.
- Does not define mutable runtime event streams or transient execution logs.

## Use When
- Recording durable evidence that acceptance, schema, or trace-related validation checks were performed.
- Capturing a reviewable validation result that should remain linked to a traced initiative.
- Reviewing whether a validation outcome belongs in a committed ledger or should remain transient runtime output.

## Related Standards and Sources
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Store durable validation evidence under `core/control_plane/ledgers/validation_evidence/`.
- Use JSON for published validation-evidence artifacts.
- Treat validation evidence as append-only historical output, not mutable current-state truth.
- Every evidence artifact should publish:
  - `trace_id`
  - a stable `evidence_id`
  - an `overall_result`
  - `recorded_at`
  - covered acceptance IDs when acceptance is in scope
  - validator IDs or explicit check methods when known
  - the subject paths or artifact IDs that were checked
- Use validation-result vocabulary such as `passed`, `failed`, `warning`, and `not_applicable` for evidence results.
- Do not reuse lifecycle-status fields to describe validation outcomes.
- Prefer readable deterministic evidence IDs for durable committed evidence artifacts.
- Use UUIDs only later if the repository starts storing high-volume generated run instances rather than a curated evidence ledger.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the validation-evidence artifact family. |
| `id` | Required | Stable evidence artifact identifier. |
| `title` | Required | Human-readable evidence title. |
| `status` | Required | Lifecycle status of the evidence artifact record itself. |
| `trace_id` | Required | Shared trace identifier. |
| `overall_result` | Required | Overall validation outcome for the evidence artifact. |
| `recorded_at` | Required | RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ` for when the evidence was recorded. |
| `checks` | Required | Array of validation check records. |

### Check entry fields
| Field | Requirement | Notes |
|---|---|---|
| `check_id` | Required | Stable identifier for the check record within the evidence artifact. |
| `title` | Required | Human-readable check title. |
| `result` | Required | Use the validation-result vocabulary. |
| `subject_paths` | Optional | Concrete repository paths covered by the check. |
| `subject_ids` | Optional | Artifact or planning IDs covered by the check. |
| `validator_id` | Optional | Stable validator identifier when a cataloged validator ran. |
| `acceptance_ids` | Optional | Acceptance items covered by the check. |
| `notes` | Optional | Short explanation or outcome note. |

## Process or Workflow
1. Identify the traced initiative or artifact set being validated.
2. Record the checks that matter durably for review, closeout, or audit.
3. Link the evidence to the relevant trace, acceptance items, validators, and subject surfaces.
4. Validate the evidence artifact against its published schema.
5. Update the unified traceability index in the same change set when a new durable evidence artifact is added.

## Examples
- A traceability-baseline evidence record can show that PRD, decision, design, acceptance-contract, and traceability-index links are present and valid.
- A schema-backed check can record the validator ID and the subject artifact path it validated.
- A transient local smoke test output does not belong in this ledger unless it is being promoted to durable evidence.

## Operationalization
- `Modes`: `artifact`; `documentation`
- `Operational Surfaces`: `core/control_plane/ledgers/validation_evidence/`; `core/control_plane/ledgers/validation_evidence/README.md`; `docs/planning/prds/core_python_foundation.md`

## Validation
- Validation-evidence artifacts should validate against their published schema.
- `validator_id` values should exist in the validator registry when present.
- `acceptance_ids` should exist in the linked source acceptance contract or PRD when present.
- Reviewers should reject evidence artifacts that act like mutable logs, omit trace links, or blur validation outcome with lifecycle status.

## Change Control
- Update this standard when the repository changes the durable evidence shape or result vocabulary materially.
- Update the companion schema, examples, and live evidence artifacts in the same change set when this family changes structurally.
- Update the unified traceability index in the same change set when durable evidence is added, renamed, or removed.

## References
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/README.md)

## Notes
- This family is intentionally narrower than a generic execution log. It should capture durable evidence only.

## Updated At
- `2026-03-11T06:00:00Z`
