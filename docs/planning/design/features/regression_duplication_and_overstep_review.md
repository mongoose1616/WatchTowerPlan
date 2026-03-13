---
trace_id: trace.regression_duplication_and_overstep_review
id: design.features.regression_duplication_and_overstep_review
title: Regression Duplication and Overstep Review Feature Design
summary: Defines the review and remediation design for traceability joins, governed
  companion paths, stale-path filtering, and planning-surface coherence under the
  regression-and-duplication theme.
type: feature_design
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

# Regression Duplication and Overstep Review Feature Design

## Record Metadata
- `Trace ID`: `trace.regression_duplication_and_overstep_review`
- `Design ID`: `design.features.regression_duplication_and_overstep_review`
- `Design Status`: `active`
- `Linked PRDs`: `prd.regression_duplication_and_overstep_review`
- `Linked Decisions`: `decision.regression_duplication_and_overstep_review_direction`
- `Linked Implementation Plans`: `design.implementation.regression_duplication_and_overstep_review`
- `Updated At`: `2026-03-13T03:21:56Z`

## Summary
Defines the review and remediation design for traceability joins, governed companion paths, stale-path filtering, and planning-surface coherence under the regression-and-duplication theme.

## Source Request
- User request to run a comprehensive internal project review for regression, duplication of effort, repeated work, and overstep using the supplied March 2026 regression evidence set as comparative input.
- Discovery-pass confirmation that the same themed defect boundary spans planning docs, task documents, derived indexes, acceptance/evidence artifacts, validation services, and their adjacent command and standards docs.

## Scope and Feature Boundary
- Covers the current review trace, the intersecting cancelled trace, and the authoritative repository surfaces that create, derive, validate, or explain trace-linked planning state.
- Covers planning documents, task records, derived trackers and indexes, acceptance contracts, validation evidence ledgers, schemas, examples, loaders, sync builders, query consumers, command docs, standards, and regression tests directly tied to the confirmed issues.
- Covers repeated post-fix review, second-angle confirmation, and adversarial confirmation under the same stable theme.
- Excludes new product-facing functionality, a broader decision-supersession feature program, and repo-local pseudo-reference creation under `docs/references/**`.

## Current-State Context
- Tasks with `trace.*` related IDs but no `trace_id` currently disappear from initiative, planning-catalog, and traceability joins.
- `task update --write` can move a task document without repairing the old task path in acceptance contracts and validation evidence.
- Acceptance reconciliation validates structure but did not previously validate whether repo-local `validation_targets`, `related_paths`, or evidence `subject_paths` still exist on disk.
- Several sync builders preserve `related_paths` from current derived indexes, which can reintroduce deleted references as repeated stale state.
- The current review trace and an adjacent cancelled trace still contain placeholder bootstrap content or stale task state, which creates planning noise and hides the actual reviewed state.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): close the real failure paths in the canonical surfaces instead of layering on more manual repair steps.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): docs, code, contracts, ledgers, indexes, and tests must stay aligned in one deterministic change set.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): the work remains bounded to repository-maintenance infrastructure and should not expand into product feature design.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task records and task status transitions must remain authoritative and trace-linked.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the planning corpus must remain joinable across human- and machine-readable surfaces.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): acceptance contracts must keep valid repo-local path targets and move with governed planning artifacts.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): evidence subject paths and related paths must stay inspectable and current.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): the maintenance workflow requires repeated validation and no-new-issues confirmation, not just first-pass fixes.

## Design Goals and Constraints
- Remove repeated-work and stale-state paths at the authoritative source rather than documenting around them.
- Preserve current capability, determinism, correctness, and performance while adding the missing guardrails.
- Keep the review under one stable thematic scope until repeated confirmation passes stop finding actionable issues.
- Preserve the repository family boundaries: no new local pseudo-reference family and no broad redesign beyond the confirmed defect boundary.

## Options Considered
### Option 1
- Apply narrow file-local fixes to the currently broken docs and artifacts only.
- Strength: smallest immediate churn.
- Tradeoff: the same stale or missing linkage patterns can recur because the source write and validation paths stay permissive.

### Option 2
- Harden the source write, sync, validation, and planning surfaces together, then repair existing drift and validate with repeated themed review passes.
- Strength: closes the confirmed defect class without introducing a parallel authority surface.
- Tradeoff: broad same-change-set coordination across code, docs, contracts, ledgers, indexes, schemas, and tests.

### Option 3
- Create a new repo-local review-reference artifact and defer some of the guardrail fixes to later work.
- Strength: adds more narrative context quickly.
- Tradeoff: duplicates authority, conflicts with the references-family boundary, and leaves the real drift paths live.

## Recommended Design
### Architecture
- Enforce trace linkage at task-authoring time through schema and lifecycle validation so traced tasks cannot silently disappear from joins.
- Repair governed acceptance and evidence companions automatically when task moves change the canonical task document path.
- Validate repo-local contract and evidence paths directly during acceptance reconciliation and aggregate validation.
- Filter existing derived `related_paths` through repo-local existence checks before preserving them in rebuilt indexes.
- Rewrite the current and adjacent cancelled planning chains so they accurately reflect active versus historical work and no longer carry placeholder or raw external-path leakage.

### Data and Interface Impacts
- `core/control_plane/schemas/interfaces/documentation/task_front_matter.v1.schema.json` gains explicit trace-linkage requirements for trace-related task records.
- Acceptance contracts and validation evidence now fail validation when repo-local path references are stale or missing.
- Derived PRD, decision, design, foundation, reference, and standard indexes stop rehydrating deleted `related_paths`.
- Command docs and standards docs expand to describe the stricter task and governed-companion behavior.
- Planning trackers and query surfaces reflect cleaned active and cancelled trace state after sync.

### Execution Flow
1. Build the coverage map and complete a discovery pass across planning docs, tasks, control-plane artifacts, runtime services, tests, and the supplied external review input.
2. Harden the authoritative write and validation paths: task trace linkage, task-move companion repair, acceptance/evidence path existence checks, and stale-related-path filtering.
3. Repair source artifacts: traced tasks missing `trace_id`, placeholder planning docs, cancelled-trace historical records, and adjacent standards/command docs.
4. Refresh derived trackers and indexes, then run targeted validation followed by full-repository validation.
5. Re-review the touched area from a fresh angle, then run an adversarial confirmation pass whose goal is to disprove the claim that the themed area is clean.
6. If a new actionable issue appears, add it to the findings ledger and repeat the same bounded loop until consecutive confirmation passes stay clean.

### Invariants and Failure Cases
- Traced tasks must not disappear from joins because of omitted linkage metadata.
- Acceptance and evidence artifacts must not look valid when they reference deleted local files.
- Derived indexes must not resurrect deleted relationships from previous output state.
- Cancelled traces must remain queryable as historical context without competing with active execution state.

## Affected Surfaces
- docs/planning/
- docs/commands/core_python/
- docs/standards/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
- core/control_plane/indexes/
- core/control_plane/schemas/interfaces/documentation/
- core/control_plane/examples/
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/validation/
- core/python/tests/

## Design Guardrails
- Do not reduce validator strictness to hide drift.
- Do not add a new repo-local pseudo-reference under `docs/references/**` for repository-native review conclusions.
- Do not repair only derived indexes while leaving the source write paths able to reproduce the defect immediately.
- Keep every fix accompanied by the minimum required companion docs, governed artifacts, and regression coverage.

## Risks
- Broad derived-surface churn can obscure whether the real source fixes are complete unless post-fix review stays focused on the touched dependency chain.
- Task-path repair logic must update the full companion set consistently or acceptance/evidence drift will survive under a new file name.
- Confirmation passes can become redundant if they reuse the same viewpoint, so the review must deliberately vary the angle of inspection.

## References
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md)
- [regression_duplication_and_overstep_review_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/regression_duplication_and_overstep_review_direction.md)
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md)
