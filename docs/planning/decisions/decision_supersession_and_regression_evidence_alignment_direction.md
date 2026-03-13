---
trace_id: trace.decision_supersession_and_regression_evidence_alignment
id: decision.decision_supersession_and_regression_evidence_alignment_direction
title: Decision Supersession and Regression Evidence Alignment Direction Decision
summary: Historical decision record explaining why the mixed decision-supersession
  and local-regression-summary slice was cancelled before execution.
type: decision_record
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

# Decision Supersession and Regression Evidence Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.decision_supersession_and_regression_evidence_alignment`
- `Decision ID`: `decision.decision_supersession_and_regression_evidence_alignment_direction`
- `Record Status`: `deprecated`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.decision_supersession_and_regression_evidence_alignment`
- `Linked Designs`: `design.features.decision_supersession_and_regression_evidence_alignment`
- `Linked Implementation Plans`: `design.implementation.decision_supersession_and_regression_evidence_alignment`
- `Updated At`: `2026-03-13T03:21:56Z`

## Summary
Historical decision record explaining why the mixed decision-supersession and local-regression-summary slice was cancelled before execution.

## Decision Statement
Cancel this slice before execution, keep it only as historical context, move any still-live regression-and-duplication hardening into `trace.regression_duplication_and_overstep_review`, and do not create a repo-local regression summary under `docs/references/**`.

## Trigger or Source Request
- The earlier regression-and-duplication review identified a possible follow-up around explicit decision supersession and a separate local summary of the supplied March 2026 regression evidence set.
- Before execution began, the user redirected work toward adjacent live repository cleanup, and a follow-up review showed that this trace had mixed unrelated concerns and would overstep the correct boundary.

## Current Context and Constraints
- The trace was already closed as `cancelled`, but its planning docs still looked like active bootstrap scaffolds.
- `docs/references/**` is reserved for external published authorities with canonical upstream links, so a repository-native regression summary there would be category drift.
- The active `trace.regression_duplication_and_overstep_review` now owns the still-live traceability, validation, and planning-hygiene defects from the same review theme.

## Applied References and Implications
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): the cancellation should still be captured as a durable decision record instead of leaving an unexplained abandoned slice.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): cancelled initiatives should not leave open execution tasks behind.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): historical planning records should remain queryable without competing with active execution traces.
- [AGENTS.md](/home/j/WatchTowerPlan/docs/references/AGENTS.md): the references family boundary rules out a repo-local regression summary in that subtree.

## Affected Surfaces
- docs/planning/prds/decision_supersession_and_regression_evidence_alignment.md
- docs/planning/design/features/decision_supersession_and_regression_evidence_alignment.md
- docs/planning/design/implementation/decision_supersession_and_regression_evidence_alignment.md
- docs/planning/tasks/open/
- docs/planning/tasks/closed/
- docs/planning/tasks/task_tracking.md
- docs/planning/coordination_tracking.md
- docs/planning/initiatives/initiative_tracking.md
- docs/references/AGENTS.md
- docs/references/README.md
- docs/planning/prds/regression_duplication_and_overstep_review.md

## Options Considered
### Option 1
- Continue the original slice and implement both explicit decision supersession plus a dedicated local regression summary.
- Strength: would maximize follow-up breadth.
- Tradeoff: oversteps the confirmed live boundary and creates a repo-local summary in the wrong document family.

### Option 2
- Narrow the slice to only the proposed repo-local regression summary.
- Strength: smaller than the full mixed initiative.
- Tradeoff: still conflicts with the `docs/references/**` boundary and duplicates planning authority.

### Option 3
- Cancel the slice, rewrite its planning chain as historical context, cancel the leftover execution tasks, and capture the still-live hardening work in the active regression/duplication trace.
- Strength: preserves history while keeping the actual repository fixes in the correct active boundary.
- Tradeoff: leaves explicit decision supersession unimplemented unless future evidence proves it is needed.

## Chosen Outcome
Adopt option 3. This trace remains only as a historical cancelled record, its open tasks are cancelled, and the still-live review hardening work proceeds in `trace.regression_duplication_and_overstep_review`.

## Rationale and Tradeoffs
- The mixed-scope slice bundled one possible governance enhancement with one document-family misuse, which was the wrong shape for a bounded maintenance follow-up.
- The active regression/duplication review trace already owns the real live defects and can record the review conclusions without creating another authority surface.
- The tradeoff is that explicit decision supersession is deferred, but no live review finding in this loop proved it was required to restore repository correctness.

## Consequences and Follow-Up Impacts
- The planning chain for this trace should read as historical cancelled context, not as active implementation work.
- The remaining open tasks for this trace should move to terminal cancelled state.
- Future contributors should open a new bounded trace only if fresh evidence proves explicit decision supersession is needed independently of this cancelled review follow-up.

## Risks, Dependencies, and Assumptions
- Assumes the active regression/duplication review trace is the right home for the still-live repository hardening work.
- Risks future confusion if the cancelled trace retains active-looking placeholder language or open tasks after this rewrite.
- Depends on keeping the planning trackers and coordination outputs aligned with the cancelled task state.

## References
- [decision_supersession_and_regression_evidence_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/decision_supersession_and_regression_evidence_alignment.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md)
- [AGENTS.md](/home/j/WatchTowerPlan/docs/references/AGENTS.md)
