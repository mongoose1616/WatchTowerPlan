---
trace_id: trace.decision_supersession_and_regression_evidence_alignment
id: design.features.decision_supersession_and_regression_evidence_alignment
title: Decision Supersession and Regression Evidence Alignment Feature Design
summary: Historical design record for a cancelled slice that would have mixed decision
  supersession work with a repo-local regression-summary proposal.
type: feature_design
status: deprecated
owner: repository_maintainer
updated_at: '2026-03-13T03:21:56Z'
audience: shared
authority: historical
applies_to:
- docs/standards/governance/decision_capture_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/templates/decision_record_template.md
- docs/standards/data_contracts/decision_index_standard.md
- core/control_plane/schemas/artifacts/decision_index.v1.schema.json
- core/python/src/watchtower_core/repo_ops/sync/decision_index.py
- core/python/src/watchtower_core/repo_ops/query/decisions.py
- core/python/src/watchtower_core/cli/query_records_handlers.py
- docs/commands/core_python/watchtower_core_query_decisions.md
- docs/planning/decisions/preimplementation_machine_coordination_entrypoint.md
- docs/planning/decisions/machine_first_coordination_entry_surface.md
- docs/planning/decisions/planning_authority_unification_direction.md
- docs/references/
---

# Decision Supersession and Regression Evidence Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.decision_supersession_and_regression_evidence_alignment`
- `Design ID`: `design.features.decision_supersession_and_regression_evidence_alignment`
- `Design Status`: `deprecated`
- `Linked PRDs`: `prd.decision_supersession_and_regression_evidence_alignment`
- `Linked Decisions`: `decision.decision_supersession_and_regression_evidence_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.decision_supersession_and_regression_evidence_alignment`
- `Updated At`: `2026-03-13T03:21:56Z`

## Summary
Historical design record for a cancelled slice that would have mixed decision supersession work with a repo-local regression-summary proposal.

## Source Request
- Earlier regression-and-duplication review findings suggested two possible follow-ups: explicit decision supersession support and a separate local summary of the supplied March 2026 regression evidence set.

## Scope and Feature Boundary
- Would have covered decision supersession metadata across decision standards, schemas, sync, query, and live decision records.
- Would have covered one separate local summary of the supplied regression evidence set.
- Does not execute because the slice was cancelled before implementation.
- Does not define the active remediation plan for the still-live review defects, which now belongs to `trace.regression_duplication_and_overstep_review`.

## Current-State Context
- The initiative is already closed as cancelled, but the planning docs were still left in placeholder bootstrap form.
- The proposed local regression summary would have landed in `docs/references/**`, which is reserved for externally published authorities rather than repo-native review notes.
- The still-live repository defects from the same review theme are being fixed directly in the active regression/duplication trace, making this mixed slice unnecessary.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): bounded maintenance work should tighten the real seams rather than adding a second narrative layer.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): historical records should preserve context without competing with active authority.

## Internal Standards and Canonical References Applied
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): the cancellation should remain explicit and durable.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the cancelled trace should stay queryable while its task state becomes terminal.
- [AGENTS.md](/home/j/WatchTowerPlan/docs/references/AGENTS.md): the references subtree does not authorize a repo-native regression summary.

## Design Goals and Constraints
- Preserve the reasoning for cancelling this mixed-scope slice.
- Prevent the historical planning chain from reading like live work.
- Keep future contributors from misclassifying repo-native review notes as reference-family content.

## Options Considered
### Option 1
- Continue the original mixed slice.
- Strength: widest follow-up scope.
- Tradeoff: combines unrelated concerns and oversteps the current repository boundary.

### Option 2
- Cancel the slice and move any still-live review hardening into the active regression/duplication trace.
- Strength: keeps the real fixes inside the active authoritative review boundary.
- Tradeoff: explicit decision supersession remains future work only if fresh evidence justifies it.

## Recommended Design
### Architecture
- Historical-only planning records that preserve cancellation context.
- No new runtime or control-plane implementation for this trace.

### Data and Interface Impacts
- Planning docs and task state for this trace shift from placeholder-active to historical-cancelled.
- The active regression/duplication trace remains the authoritative home of the actual review remediation.

### Execution Flow
1. Rewrite the planning chain as historical cancelled context.
2. Cancel the remaining open tasks for this trace.
3. Rebuild derived planning surfaces so the cancelled state is visible everywhere.

### Invariants and Failure Cases
- The cancelled trace must remain queryable as historical context.
- The planning corpus must not leave active-looking placeholder docs or open tasks behind for this slice.

## Affected Surfaces
- docs/planning/prds/decision_supersession_and_regression_evidence_alignment.md
- docs/planning/decisions/decision_supersession_and_regression_evidence_alignment_direction.md
- docs/planning/design/implementation/decision_supersession_and_regression_evidence_alignment.md
- docs/planning/tasks/open/
- docs/planning/tasks/closed/
- docs/planning/tasks/task_tracking.md
- docs/planning/coordination_tracking.md
- docs/planning/initiatives/initiative_tracking.md

## Design Guardrails
- Do not revive this trace as active work without fresh evidence.
- Do not create a repo-native review summary under `docs/references/**`.

## Risks
- Historical traces can still create confusion if their authored docs and task state are not normalized consistently.

## References
- [decision_supersession_and_regression_evidence_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/decision_supersession_and_regression_evidence_alignment.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md)
