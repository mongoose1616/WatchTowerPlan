---
id: "std.governance.acceptance_evidence_reconciliation"
title: "Acceptance and Evidence Reconciliation Standard"
summary: "This standard defines how PRD acceptance IDs, acceptance contracts, validation evidence, validator references, and traceability should reconcile for one traced initiative."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "acceptance"
  - "validation_evidence"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/prds/"
  - "core/control_plane/contracts/acceptance/"
  - "core/control_plane/ledgers/validation_evidence/"
  - "core/control_plane/indexes/traceability/traceability_index.v1.json"
aliases:
  - "acceptance reconciliation"
  - "evidence reconciliation"
---

# Acceptance and Evidence Reconciliation Standard

## Summary
This standard defines how PRD acceptance IDs, acceptance contracts, validation evidence, validator references, and traceability should reconcile for one traced initiative.

## Purpose
- Close the semantic gap between PRD acceptance intent and durable validation proof.
- Make acceptance drift visible without relying on reviewers to reconstruct joins manually from prose.
- Provide a narrow repository rule for when acceptance coverage is complete enough to treat it as reconciled.

## Scope
- Applies to traced initiatives that publish PRD acceptance IDs and machine-readable acceptance contracts.
- Applies to the relationship between PRD acceptance IDs, acceptance contracts, validation evidence, validator references, and traceability entries.
- Covers semantic reconciliation rules rather than schema syntax alone.
- Does not redefine the separate schema-validation rules for the underlying artifact families.

## Use When
- A trace publishes PRD acceptance criteria and a machine-readable acceptance contract.
- Validation evidence is expected to prove acceptance coverage durably.
- Reviewing whether acceptance and evidence drift exists across a traced initiative.

## Related Standards and Sources
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [acceptance_evidence_reconciliation.md](/home/j/WatchTowerPlan/workflows/modules/acceptance_evidence_reconciliation.md): workflow surface that operationalizes or depends on this standard.

## Guidance
- Reconcile acceptance at the shared `trace_id` level.
- Treat PRD acceptance IDs as the human source of acceptance intent.
- Treat the acceptance contract as the machine-readable acceptance boundary.
- Treat validation evidence as the durable proof layer.
- Treat the traceability index as the joined current-state lookup surface.
- For a trace with governed acceptance:
  - exactly one PRD should own the active acceptance IDs
  - exactly one acceptance contract should publish the same acceptance IDs
  - traceability should publish the same `acceptance_ids`
  - traceability should list the matching acceptance-contract and evidence IDs
  - required validator IDs in the acceptance contract should exist in the validator registry
  - every acceptance ID in the acceptance contract should be covered by at least one durable evidence check
- Reject silent gaps where acceptance IDs exist but no durable evidence claims to cover them.

## Structure or Data Model
| Surface | Responsibility |
|---|---|
| PRD acceptance criteria | Human acceptance intent |
| Acceptance contract | Machine-readable acceptance boundary |
| Validation evidence | Durable proof of covered checks |
| Validator registry | Stable validator identities |
| Traceability index | Joined lookup across all of the above |

## Process or Workflow
1. Resolve the trace, PRD, acceptance contract, traceability entry, and validation evidence artifacts.
2. Compare the PRD acceptance IDs to the acceptance contract and traceability entry.
3. Verify validator references against the validator registry.
4. Verify evidence IDs and evidence acceptance coverage against the acceptance contract.
5. Record explicit issues for missing joins, unknown validator references, or uncovered acceptance IDs.

## Operationalization
- `Modes`: `documentation`; `artifact`
- `Operational Surfaces`: `docs/planning/prds/`; `core/control_plane/contracts/acceptance/`; `core/control_plane/ledgers/validation_evidence/`; `core/control_plane/indexes/traceability/traceability_index.v1.json`

## Validation
- PRD acceptance IDs, acceptance-contract acceptance IDs, and traceability acceptance IDs should match exactly.
- Traceability should list the current acceptance-contract and evidence IDs for the same trace.
- Validation-evidence checks should not reference unknown acceptance IDs or unknown validator IDs.
- Every acceptance ID should be covered by at least one durable evidence check once the trace claims durable acceptance coverage.

## Change Control
- Update this standard when the repository changes the acceptance-reconciliation rules or the meaning of durable evidence coverage.
- Update the workflow module, Python reconciliation command, validator registry, and any affected evidence artifacts in the same change set when this rule changes materially.

## References
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md)
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md)
- [acceptance_evidence_reconciliation.md](/home/j/WatchTowerPlan/workflows/modules/acceptance_evidence_reconciliation.md)

## Updated At
- `2026-03-11T06:00:00Z`
