# Traceability Steward Role

## Purpose
Use this role to orchestrate trace-bearing decisions, traceability reconciliation, acceptance or evidence coverage, and initiative closeout so traced planning state stays explicit from decision through terminal outcome.

## Use When
- One request spans decision capture, traceability reconciliation, acceptance or evidence checks, and closeout readiness.
- The main risk is stale or ambiguous traced state across multiple planning and governance surfaces.
- The task needs a dedicated orchestration layer that keeps trace-bearing changes coherent across the full initiative lifecycle.

## Inputs
- Scoped traceability-governance request
- In-scope trace IDs, traced planning artifacts, acceptance or evidence surfaces, and initiative state
- Current closeout intent, known link drift, or unresolved decision points

## Composes Modules
- [decision_capture.md](../modules/decision_capture.md): records durable repository decisions that should become explicit traced inputs.
- [traceability_reconciliation.md](../modules/traceability_reconciliation.md): reconciles traced planning artifacts with their companion trackers, indexes, and trace joins.
- [acceptance_evidence_reconciliation.md](../modules/acceptance_evidence_reconciliation.md): checks that acceptance intent, validator linkage, and evidence coverage remain aligned for one trace.
- [initiative_closeout.md](../modules/initiative_closeout.md): closes one traced initiative with explicit terminal-state and mirror alignment.

## Workflow
1. Confirm whether the request spans multiple traced lifecycle stages instead of one narrow traceability or closeout task.
2. Use `decision_capture.md` when a durable tradeoff or policy choice must become an explicit traced input before reconciliation or closeout can be trusted.
3. Use `traceability_reconciliation.md` to restore agreement across traced planning artifacts, trackers, indexes, and mirror surfaces.
4. Use `acceptance_evidence_reconciliation.md` when trace validity depends on explicit acceptance coverage or durable validation evidence.
5. Use `initiative_closeout.md` only after the trace state, acceptance posture, and remaining exceptions are explicit enough for a terminal outcome.

## Data Structure
- Trace-bearing artifact chain from decision inputs through reconciliation, evidence coverage, and closeout state
- Explicit exceptions or unresolved follow-up when traced state cannot be fully reconciled in one change

## Outputs
- Coordinated traceability, acceptance, and closeout updates for the scoped trace
- Explicit unresolved exceptions or follow-up work when traced lifecycle work remains open

## Done When
- Traced planning state is explicit from decision input through closeout posture.
- Acceptance and evidence posture is clear enough for handoff or terminal outcome decisions.
- The role has coordinated the traceability workflows without copying their detailed reconciliation or closeout steps.
