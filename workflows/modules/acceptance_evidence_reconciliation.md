# Acceptance and Evidence Reconciliation Workflow

## Purpose
Use this workflow to reconcile PRD acceptance IDs, acceptance contracts, validation evidence, validator references, and the traceability layer for one traced initiative.

## Use When
- A task changes PRD acceptance criteria, acceptance contracts, validation evidence, or traceability joins.
- A trace needs an explicit acceptance-coverage review before closeout or handoff.
- Reviewers need a reusable semantic check rather than only schema validation.
- Choose this route when one trace's acceptance intent, coverage, or evidence linkage is the main question rather than general planning or artifact-family drift.

## Inputs
- Target `trace_id`
- Current PRD acceptance IDs
- Current acceptance contract
- Current validation evidence artifacts
- Current traceability entry
- Current validator registry

## Additional Files to Load
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): defines the machine-readable acceptance boundary this workflow is reconciling.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): defines the evidence artifact shape and validation linkage this workflow should preserve.
- [watchtower_core_validate_acceptance.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_acceptance.md): documents the command surface used to run acceptance reconciliation deterministically.

## Workflow
1. Resolve the trace boundary.
   - Identify the trace, owning PRD, acceptance contract, evidence artifacts, and traceability entry.
2. Compare acceptance intent and machine boundaries.
   - Compare PRD acceptance IDs to the acceptance contract and traceability entry.
3. Check validator and evidence linkage.
   - Verify required validator IDs exist.
   - Verify evidence references known acceptance IDs and validator IDs.
4. Check coverage.
   - Confirm every acceptance ID is covered by at least one durable evidence check when the trace claims durable acceptance coverage.
5. Reconcile or record follow-up.
   - Fix drift in the current change set when possible.
   - Otherwise record explicit follow-up tasks or closeout exceptions.

## Data Structure
- Trace identifier
- PRD acceptance IDs
- Acceptance-contract acceptance IDs
- Traceability acceptance and evidence joins
- Evidence coverage map
- Reconciliation issues

## Outputs
- Reconciled acceptance and evidence surfaces, or an explicit issue list and follow-up.
- A semantic validation result from `watchtower-core validate acceptance` when Python is available.

## Done When
- PRD, contract, evidence, validator, and traceability surfaces agree for the target trace.
- Any remaining acceptance gap is explicit rather than implied.
