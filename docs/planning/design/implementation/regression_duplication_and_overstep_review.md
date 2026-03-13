---
trace_id: trace.regression_duplication_and_overstep_review
id: design.implementation.regression_duplication_and_overstep_review
title: Regression Duplication and Overstep Review Implementation Plan
summary: Breaks the regression-and-duplication review into a coverage-led remediation,
  validation, and confirmation loop across planning, control-plane, and runtime
  surfaces.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T03:54:02Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/standards/
- workflows/
---

# Regression Duplication and Overstep Review Implementation Plan

## Record Metadata
- `Trace ID`: `trace.regression_duplication_and_overstep_review`
- `Plan ID`: `design.implementation.regression_duplication_and_overstep_review`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.regression_duplication_and_overstep_review`
- `Linked Decisions`: `decision.regression_duplication_and_overstep_review_direction`
- `Source Designs`: `design.features.regression_duplication_and_overstep_review`
- `Linked Acceptance Contracts`: `contract.acceptance.regression_duplication_and_overstep_review`
- `Updated At`: `2026-03-13T03:54:02Z`

## Summary
Breaks the regression-and-duplication review into a coverage-led remediation, validation, and confirmation loop across planning, control-plane, and runtime surfaces.

## Source Request or Design
- Feature design: [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/design/features/regression_duplication_and_overstep_review.md)
- PRD: [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md)
- Decision: [regression_duplication_and_overstep_review_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/regression_duplication_and_overstep_review_direction.md)

## Scope Summary
- Complete the themed review loop for traceability drift, governed companion-path drift, stale derived relationships, and planning-surface coherence.
- Fix confirmed code, data-contract, tracker, and documentation defects in the same change sets as their companion validation and test updates.
- Refresh derived trackers and indexes, then run repeated validation and confirmation passes until no new actionable issue appears in the same boundary.
- Exclude unrelated product work, broad planning-model redesign, and repo-local pseudo-reference creation in `docs/references/**`.

## Assumptions and Constraints
- Existing validation should remain strict; the implementation must improve source behavior rather than weakening repository rules.
- Derived trackers and indexes must be rebuilt after source fixes so post-fix review evaluates the real live state instead of stale output.
- The review should stay inside one stable theme and reopen the loop if any post-fix pass finds a new actionable issue in that boundary.
- Performance-sensitive sync and validation paths should not absorb unnecessary filesystem churn beyond the targeted existence checks needed for correctness.

## Current-State Context
- The discovery pass already confirmed five actionable issue clusters under the same theme: missing trace linkage on traced tasks, task-move governed-companion drift, missing repo-local path validation in acceptance reconciliation, stale `related_paths` preserved by sync builders, and placeholder or stale planning/task state in the current plus adjacent cancelled traces.
- The current trace still contains only its bootstrap task, so the implementation cycle must add bounded execution and validation tasks before closeout.
- The adjacent cancelled trace is already closed as cancelled, but its authored planning docs still look like unfinished active work unless they are rewritten as historical records.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task creation, movement, and closure must remain authoritative and same-change aligned with derived planning views.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): contract path references must remain valid and should move with the governed artifacts they point at.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): evidence must remain durable, inspectable, and tied to concrete validated subject paths.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): repaired source state must stay joined across human-readable planning and machine-readable planning indexes.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): repository review requires targeted validation, full validation, and repeated no-new-issues confirmation before closeout.

## Proposed Technical Approach
- Add strict trace-linkage validation to task authoring and task updates, then cover that behavior with unit and integration tests.
- Extend task lifecycle move handling so acceptance contracts and validation evidence automatically rewrite old task document paths to the new canonical path.
- Add repo-local path existence validation for acceptance and evidence artifacts and propagate that behavior through aggregate validation.
- Replace stale derived `related_paths` reuse with filtered existing-path reuse in the affected sync builders.
- Repair existing planning docs, tasks, contracts, and ledgers so the live repo state reflects the new rules immediately.
- Rebuild derived mirrors, then validate and re-review from multiple angles until the same thematic slice stays clean.

## Work Breakdown
1. Build the coverage map and complete the discovery pass across planning docs, tasks, governed artifacts, runtime implementations, tests, and the supplied external review evidence.
2. Implement code and schema hardening for task trace linkage, task-move governed-companion repair, acceptance/evidence path validation, and stale-related-path filtering, with targeted regression tests.
3. Repair source artifacts by adding missing task `trace_id` values, rewriting placeholder planning docs, cancelling stale open tasks on the cancelled trace, cleaning adjacent raw external-path leakage, and updating command and standards docs.
4. Create bounded execution and validation tasks for the current trace, close the bootstrap task, rebuild derived planning surfaces, and update the acceptance contract plus validation-evidence ledger to reflect the real remediation scope.
5. Run targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation; if any new actionable issue appears, add it to the findings ledger and repeat the same loop.

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.regression_duplication_and_overstep_review.001` | `high` | `resolved` | task front matter schema; task lifecycle support; initiative/planning/traceability joins; traced task docs | targeted task-lifecycle tests and post-sync planning queries |
| `finding.regression_duplication_and_overstep_review.002` | `high` | `resolved` | task lifecycle move handling; acceptance contracts; validation evidence ledgers | task-lifecycle integration coverage plus acceptance-only validation |
| `finding.regression_duplication_and_overstep_review.003` | `medium` | `resolved` | acceptance reconciliation; aggregate validation | acceptance-reconciliation unit coverage and validate-all regression coverage |
| `finding.regression_duplication_and_overstep_review.004` | `medium` | `resolved` | PRD, decision, design, foundation, reference, and standard index sync builders | targeted sync unit coverage and post-sync stale-path scans |
| `finding.regression_duplication_and_overstep_review.005` | `medium` | `resolved` | current trace planning docs; cancelled trace planning docs and tasks; adjacent standards and command docs; trackers and derived indexes | placeholder and external-path scans found no matches; lifecycle normalization closed the bounded tasks; coordination query reported zero actionable tasks after initiative closeout; acceptance/evidence/task/index path audits reported zero missing paths |
| `finding.regression_duplication_and_overstep_review.006` | `medium` | `resolved` | cancelled-trace acceptance contract and validation evidence | aggregate validate-all output plus same-change contract/evidence normalization |
| `finding.regression_duplication_and_overstep_review.007` | `low` | `resolved` | route-preview and CLI-query regression tests | adversarial whole-repo raw-path scan exposed three non-authoritative external-input literals; fixtures were normalized to `/external/repository/report`, the 40-test targeted route-preview suite passed, the fresh full pytest baseline passed, and the final whole-repo raw-path scan returned no matches |

## Risks
- Validation and sync output will change broadly once the cleaned source state is rebuilt, so post-fix review must distinguish expected derived churn from new defects.
- Cancelling the stale open tasks on the cancelled trace could leave hidden companion-path drift if any overlooked governed artifact still references their old open-path locations.
- Repeated confirmation passes can miss the same class of problem if they only replay the same queries and scans.

## Validation Plan
- Run targeted Python tests for task lifecycle, acceptance reconciliation, aggregate validation, schema coverage, and affected sync builders while the code and schema fixes land.
- Run `uv run watchtower-core sync all --write --format json` from `core/python/` after the authored planning and governed artifacts are coherent.
- Run `uv run watchtower-core validate all --format json`, `uv run pytest`, `uv run mypy src`, and `uv run ruff check .` as the full repository baseline.
- Re-run focused scans for placeholder text, raw external-input paths, stale repo-local path references, and trace-linked task coherence after the sync and validation pass.
- Refresh the acceptance contract and validation-evidence ledger with the actual remediation and confirmation results before closeout.

## References
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/prds/regression_duplication_and_overstep_review.md)
- [regression_duplication_and_overstep_review_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/regression_duplication_and_overstep_review_direction.md)
- [regression_duplication_and_overstep_review.md](/home/j/WatchTowerPlan/docs/planning/design/features/regression_duplication_and_overstep_review.md)
