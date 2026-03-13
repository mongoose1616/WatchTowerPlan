---
trace_id: trace.regression_duplication_and_overstep_review
id: decision.regression_duplication_and_overstep_review_direction
title: Regression Duplication and Overstep Review Direction Decision
summary: Records the accepted direction to harden traceability, governed companion
  paths, validation, and planning-surface coherence in place without adding new
  pseudo-authority surfaces.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T03:21:56Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/standards/
---

# Regression Duplication and Overstep Review Direction Decision

## Record Metadata
- `Trace ID`: `trace.regression_duplication_and_overstep_review`
- `Decision ID`: `decision.regression_duplication_and_overstep_review_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.regression_duplication_and_overstep_review`
- `Linked Designs`: `design.features.regression_duplication_and_overstep_review`
- `Linked Implementation Plans`: `design.implementation.regression_duplication_and_overstep_review`
- `Updated At`: `2026-03-13T03:21:56Z`

## Summary
Records the accepted direction to harden traceability, governed companion paths, validation, and planning-surface coherence in place without adding new pseudo-authority surfaces.

## Decision Statement
Fix the confirmed regression and duplication issues inside the existing authoritative planning, sync, query, validation, contract, and evidence surfaces; normalize the intersecting cancelled trace as historical context; and do not create a repo-local pseudo-reference under `docs/references/**` for this review input.

## Trigger or Source Request
- User request to perform a comprehensive internal project review for regression, duplication of effort, repeated work, and overstep using the supplied March 2026 regression evidence set as external input.
- Discovery-pass confirmation that the live issues are systemic guardrail gaps, not isolated editorial mistakes.

## Current Context and Constraints
- Tasks that carry `trace.*` related IDs can currently disappear from trace joins if `trace_id` is omitted.
- Task moves can currently strand acceptance-contract and validation-evidence path references on the old task path.
- Acceptance reconciliation validates structure but did not validate repo-local path existence for the touched contract and evidence fields.
- Several sync builders reused `related_paths` from existing indexes, which allowed deleted paths to be reintroduced as stale derived state.
- `docs/references/**` is scoped to externally published authorities, so a repo-local regression-audit summary there would be category drift and duplicated authority rather than a clean fix.

## Applied References and Implications
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task records must remain authoritative and trace-linked state cannot silently fall out of derived planning views.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): acceptance contracts must keep their repo-local target paths aligned when governed planning artifacts move.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): evidence related paths and subject paths must remain valid, inspectable local references.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): repeated review and validation passes are part of the maintenance contract, not optional cleanup.
- [AGENTS.md](/home/j/WatchTowerPlan/docs/references/AGENTS.md): `docs/references/**` is reserved for externally published sources with canonical upstream links, which rules out a repo-native regression summary in that family.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle_support.py
- core/python/src/watchtower_core/repo_ops/sync/traceability_support.py
- core/python/src/watchtower_core/repo_ops/sync/prd_index.py
- core/python/src/watchtower_core/repo_ops/sync/decision_index.py
- core/python/src/watchtower_core/repo_ops/sync/design_document_index.py
- core/python/src/watchtower_core/repo_ops/sync/foundation_index.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/standard_index.py
- core/python/src/watchtower_core/validation/acceptance.py
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
- core/control_plane/schemas/interfaces/documentation/task_front_matter.v1.schema.json
- docs/planning/
- docs/commands/core_python/
- docs/standards/
- core/python/tests/

## Options Considered
### Option 1
- Patch only the currently broken source files and leave the write-path, validation-path, and planning-hygiene gaps otherwise unchanged.
- Strength: smallest local patch set.
- Tradeoff: repeated work and stale-state risks would remain live because the same invalid patterns could be reintroduced immediately.

### Option 2
- Harden the authoritative write, sync, validation, and planning surfaces in place; repair existing drift; and capture the review conclusions in the current trace without inventing a new local authority surface.
- Strength: closes the confirmed defects at the source while staying inside existing repository boundaries.
- Tradeoff: touches code, docs, contracts, ledgers, schemas, derived indexes, and tests in one broad but coherent maintenance slice.

### Option 3
- Create a dedicated repo-local regression reference under `docs/references/**` and continue the cancelled decision-supersession slice alongside the current review.
- Strength: would create one extra narrative artifact for future lookup.
- Tradeoff: duplicates repository-native authority, conflicts with the references-family boundary, and oversteps the confirmed live review scope.

## Chosen Outcome
Adopt option 2. The review hardens the existing task lifecycle, validation, sync, and planning surfaces directly, updates the relevant standards and command docs, records the cancellation rationale for the adjacent trace as historical context, and keeps the external-input conclusions inside the planning corpus rather than adding a pseudo-reference surface.

## Rationale and Tradeoffs
- The confirmed defects all live in authoritative repository surfaces that already exist and already own the behavior, so fixing those surfaces is the lowest-duplication path.
- A repo-local regression summary in `docs/references/**` would violate local family rules and create another place for review conclusions to drift from the planning corpus.
- Normalizing the cancelled adjacent trace prevents stale bootstrap scaffolding from competing with the active review trace without reopening unrelated governance work.
- The tradeoff is broader same-change coordination across code, docs, governed artifacts, and derived indexes, but that breadth is the real repository boundary of the defects.

## Consequences and Follow-Up Impacts
- Task creation and update flows now need explicit trace-linkage enforcement and governed-companion path repair coverage.
- Acceptance reconciliation and full validation will fail on missing repo-local contract or evidence paths that previously slipped through.
- Touched standards and command docs must explain the new trace-linkage and governed-companion repair behavior.
- The current trace should create bounded execution and validation tasks, then close only after repeated confirmation passes remain clean.

## Risks, Dependencies, and Assumptions
- Depends on same-change updates across authored docs, governed artifacts, tests, and derived mirrors so the hardening does not create new drift.
- Assumes the March 2026 regression evidence set is comparative input rather than a new standing authority family inside the repo.
- Risks accidental under-documentation if the planning-chain rewrite is treated as incidental instead of part of the reviewed defect boundary.

## References
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/design/features/regression_duplication_and_overstep_review.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/regression_duplication_and_overstep_review.md)
- [decision_supersession_and_regression_evidence_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/decision_supersession_and_regression_evidence_alignment.md)
- [AGENTS.md](/home/j/WatchTowerPlan/docs/references/AGENTS.md)
