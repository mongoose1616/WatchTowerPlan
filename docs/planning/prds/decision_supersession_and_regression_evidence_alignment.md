---
trace_id: trace.decision_supersession_and_regression_evidence_alignment
id: prd.decision_supersession_and_regression_evidence_alignment
title: Decision Supersession and Regression Evidence Alignment PRD
summary: Historical record of a cancelled slice that proposed explicit decision
  supersession support and a dedicated repo-local regression-evidence summary.
type: prd
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

# Decision Supersession and Regression Evidence Alignment PRD

## Record Metadata
- `Trace ID`: `trace.decision_supersession_and_regression_evidence_alignment`
- `PRD ID`: `prd.decision_supersession_and_regression_evidence_alignment`
- `Status`: `deprecated`
- `Linked Decisions`: `decision.decision_supersession_and_regression_evidence_alignment_direction`
- `Linked Designs`: `design.features.decision_supersession_and_regression_evidence_alignment`
- `Linked Implementation Plans`: `design.implementation.decision_supersession_and_regression_evidence_alignment`
- `Updated At`: `2026-03-13T03:21:56Z`

## Summary
Historical record of a cancelled slice that proposed explicit decision supersession support and a dedicated repo-local regression-evidence summary.

## Problem Statement
At bootstrap time, the repository review surfaced two possible follow-ups: add explicit decision supersession support across decision standards, schemas, sync, and query surfaces; and preserve the supplied March 2026 regression evidence as a dedicated repo-local summary artifact. Before execution began, a deeper review determined that the proposed slice mixed two different problem types and overstepped the verified live boundary.

The still-live regression and duplication issues were better handled directly inside the active review trace, where the actual traceability, validation, and planning-surface defects were being fixed. The proposed repo-local evidence summary also conflicted with the `docs/references/**` family boundary, which is reserved for externally published authorities with canonical upstream links. Continuing this trace would have created duplicated authority rather than a clean repository fix.

## Goals
- Preserve the historical rationale for why this trace was cancelled before execution.
- Keep the cancelled trace queryable without leaving it looking like unfinished active work.
- Prevent future contributors from reopening this exact mixed-scope slice without fresh evidence.

## Non-Goals
- Implement explicit decision supersession support in this cancelled slice.
- Create a repo-local regression-evidence summary under `docs/references/**`.
- Compete with the active `trace.regression_duplication_and_overstep_review` maintenance slice.

## Requirements
- `req.decision_supersession_and_regression_evidence_alignment.001`: The cancelled trace must remain as a coherent historical record that explains why execution did not proceed and where any still-live review work moved instead.
- `req.decision_supersession_and_regression_evidence_alignment.002`: The planning chain must not contain placeholder scaffold text or raw external-input path leakage after cancellation normalization.
- `req.decision_supersession_and_regression_evidence_alignment.003`: All open tasks for this cancelled trace must be moved to terminal cancelled state so the planning corpus no longer advertises abandoned execution work as live.

## Acceptance Criteria
- `ac.decision_supersession_and_regression_evidence_alignment.001`: The PRD, decision record, feature design, and implementation plan for this trace read as historical cancelled records rather than active scaffolds.
- `ac.decision_supersession_and_regression_evidence_alignment.002`: The cancelled trace has no remaining open tasks and remains queryable as cancelled through the planning and coordination surfaces.
- `ac.decision_supersession_and_regression_evidence_alignment.003`: The planning docs point future contributors at `trace.regression_duplication_and_overstep_review` for the still-live regression-and-duplication hardening work.

## Risks and Dependencies
- If the cancelled trace retains active-looking scaffolds, contributors may reopen stale work or misread the repository’s actual current priorities.
- If the cancellation rationale is too thin, future contributors may recreate the same mixed-scope slice and repeat the same overstep.

## Cancellation Disposition
- The live regression and duplication findings moved into [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md), which fixes the authoritative planning, validation, sync, and task-lifecycle defects directly.
- The proposed repo-local regression summary was not created because `docs/references/**` is reserved for externally published authorities, not repository-native review notes.
- Explicit decision supersession remains future work only if a new review proves it is independently necessary.

## References
- [decision_supersession_and_regression_evidence_alignment_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/decision_supersession_and_regression_evidence_alignment_direction.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [AGENTS.md](/home/j/WatchTowerPlan/docs/references/AGENTS.md)
