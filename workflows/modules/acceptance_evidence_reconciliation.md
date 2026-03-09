# Acceptance and Evidence Reconciliation Workflow

## Purpose
Use this workflow to reconcile PRD acceptance IDs, acceptance contracts, validation evidence, validator references, and the traceability layer for one traced initiative.

## Use When
- A task changes PRD acceptance criteria, acceptance contracts, validation evidence, or traceability joins.
- A trace needs an explicit acceptance-coverage review before closeout or handoff.
- Reviewers need a reusable semantic check rather than only schema validation.

## Inputs
- Target `trace_id`
- Current PRD acceptance IDs
- Current acceptance contract
- Current validation evidence artifacts
- Current traceability entry
- Current validator registry

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

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
