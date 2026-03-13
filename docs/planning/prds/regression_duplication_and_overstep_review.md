---
trace_id: trace.regression_duplication_and_overstep_review
id: prd.regression_duplication_and_overstep_review
title: Regression Duplication and Overstep Review PRD
summary: Review and harden planning, sync, query, validation, and governed artifact
  surfaces against regression, duplicated effort, repeated work, and overstep.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T03:21:56Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/standards/
- workflows/
---

# Regression Duplication and Overstep Review PRD

## Record Metadata
- `Trace ID`: `trace.regression_duplication_and_overstep_review`
- `PRD ID`: `prd.regression_duplication_and_overstep_review`
- `Status`: `active`
- `Linked Decisions`: `decision.regression_duplication_and_overstep_review_direction`
- `Linked Designs`: `design.features.regression_duplication_and_overstep_review`
- `Linked Implementation Plans`: `design.implementation.regression_duplication_and_overstep_review`
- `Updated At`: `2026-03-13T03:21:56Z`

## Summary
Review and harden planning, sync, query, validation, and governed artifact surfaces against regression, duplicated effort, repeated work, and overstep.

## Problem Statement
The regression-and-duplication review reproduced a live cluster of failures under one stable boundary: authoritative planning and governed companion surfaces could silently drift apart, stale relationships could survive sync, and incomplete or cancelled planning chains could remain visible as if they were trustworthy execution state. The failures were not isolated one-off defects. They shared one pattern: traceability and companion-artifact behavior was too permissive, so repeated work and stale state could hide inside otherwise valid-looking docs, indexes, and ledgers.

The confirmed issues included:
- traced tasks that listed a `trace.*` related ID but omitted `trace_id`, which caused them to fall out of initiative, planning-catalog, and traceability joins
- task moves that updated the task document path without repairing acceptance-contract and validation-evidence path references
- acceptance reconciliation that validated structure but not whether repo-local path references still existed
- sync builders that preserved stale `related_paths` from existing derived indexes, rehydrating deleted references
- placeholder planning docs and stale task state in the current review trace and an adjacent cancelled trace, which made the planning corpus noisier than the real repository state

## Goals
- Build one explicit coverage map across planning docs, task state, machine-readable control-plane artifacts, sync/query code paths, validators, loaders, tests, and adjacent governed surfaces before remediation.
- Fix every confirmed regression or duplication issue in the reviewed boundary without weakening validation, fidelity, determinism, or performance.
- Keep companion docs, governed artifacts, indexes, schemas, examples, and tests aligned in the same change set whenever one authoritative surface changes.
- Run repeated post-fix review and confirmation passes until no new actionable issues appear under the same theme.
- Close the trace with durable evidence, task closure, and commit-ready repository state.

## Non-Goals
- Loosen validation rules to tolerate stale or incomplete planning, contract, or evidence state.
- Create a new hidden registry or pseudo-reference surface just to restate repository-native review conclusions.
- Reopen unrelated historical initiatives that the review did not confirm as live defects.
- Expand this maintenance trace into product implementation or broader planning-model redesign work.

## Requirements
- `req.regression_duplication_and_overstep_review.001`: The trace must publish and follow an explicit coverage map across planning docs, tasks, indexes, contracts, evidence ledgers, schemas, examples, validators, loaders, sync paths, query paths, command docs, and adjacent standards before remediation begins.
- `req.regression_duplication_and_overstep_review.002`: Traced task handling must fail closed: tasks that declare trace-linked related IDs must carry matching `trace_id`, and task moves must repair governed acceptance/evidence path references in the same write flow.
- `req.regression_duplication_and_overstep_review.003`: Validation and sync surfaces must reject stale or missing repo-local path references, including acceptance-contract targets, evidence subject paths, and reused `related_paths` in derived planning indexes.
- `req.regression_duplication_and_overstep_review.004`: Touched planning and task documents must be free of placeholder scaffold text, free of raw external-input path leakage, and coherent with the real initiative and task state, including adjacent cancelled traces when they intersect the same review theme.
- `req.regression_duplication_and_overstep_review.005`: The review must maintain a findings ledger, run targeted validation and full-repository validation, perform post-fix and adversarial confirmation passes, refresh durable evidence, close the trace tasks, and finish in a clean committed state.

## Acceptance Criteria
- `ac.regression_duplication_and_overstep_review.001`: The planning corpus for `trace.regression_duplication_and_overstep_review` contains an active PRD, accepted direction decision, active feature design, active implementation plan, acceptance contract, validation evidence, closed bootstrap task, bounded execution tasks, and final closeout metadata.
- `ac.regression_duplication_and_overstep_review.002`: Traced tasks no longer disappear from joins when `trace.*` related IDs are present, and task moves automatically repair governed acceptance/evidence references under regression coverage.
- `ac.regression_duplication_and_overstep_review.003`: Acceptance reconciliation and aggregate validation fail on missing repo-local acceptance or evidence paths, and derived planning indexes no longer preserve stale `related_paths`.
- `ac.regression_duplication_and_overstep_review.004`: The touched planning corpus, command docs, standards, trackers, contracts, evidence, schemas, and examples are aligned and contain no remaining placeholder or raw external-input path leakage in the reviewed boundary.
- `ac.regression_duplication_and_overstep_review.005`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation all complete without finding a new actionable issue under the same theme.

## Risks and Dependencies
- The review touches authoritative planning docs, task lifecycle behavior, derived indexes, acceptance contracts, evidence ledgers, and validation logic in one slice, so incomplete same-change updates could create broad but legitimate derived-surface churn.
- Task move repair must update governed companions before the old task path disappears or validation will still see broken references.
- Stale-path filtering must stay narrow enough to remove deleted references without dropping valid live relationships or adding unnecessary filesystem cost.
- The confirmation loop depends on continuing to review the same stable scope instead of wandering into unrelated cleanup.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): fix the real failure modes directly and reduce repeated work by tightening explicit seams rather than adding new side channels.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): authored planning, machine-readable authority, derived mirrors, and tests must move together in one governed slice.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): repository review work should continue through repeated validation and confirmation until no new actionable issues remain.

## References
- [regression_duplication_and_overstep_review_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/regression_duplication_and_overstep_review_direction.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/design/features/regression_duplication_and_overstep_review.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/regression_duplication_and_overstep_review.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md)
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md)
