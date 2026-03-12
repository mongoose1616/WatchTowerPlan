---
trace_id: trace.acceptance_reconciliation_snapshot_reuse
id: decision.acceptance_reconciliation_snapshot_reuse_direction
title: Acceptance Reconciliation Snapshot Reuse Direction Decision
summary: Accept service-scoped acceptance snapshot reuse and reject broader loader caching
  for Acceptance Reconciliation Snapshot Reuse.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T17:02:50Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/tests/
---

# Acceptance Reconciliation Snapshot Reuse Direction Decision

## Record Metadata
- `Trace ID`: `trace.acceptance_reconciliation_snapshot_reuse`
- `Decision ID`: `decision.acceptance_reconciliation_snapshot_reuse_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.acceptance_reconciliation_snapshot_reuse`
- `Linked Designs`: `design.features.acceptance_reconciliation_snapshot_reuse`
- `Linked Implementation Plans`: `design.implementation.acceptance_reconciliation_snapshot_reuse`
- `Updated At`: `2026-03-12T17:02:50Z`

## Summary
Accept service-scoped acceptance snapshot reuse and reject broader loader caching for
Acceptance Reconciliation Snapshot Reuse.

## Decision Statement
Use lazy service-scoped snapshots inside `AcceptanceReconciliationService` to reuse shared
traceability, PRD, contract, evidence, and validator inputs across aggregate acceptance
validation.

## Trigger or Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Current Context and Constraints
- Aggregate acceptance validation currently rereads the same traceability, PRD,
  acceptance-contract, validation-evidence, and validator-registry surfaces once per trace,
  even though one `AcceptanceReconciliationService` instance already spans the full command.
- The optimization must preserve the existing reconciliation findings and fail-closed
  behavior, especially for missing traceability entries, missing contracts, and validator
  coverage mismatches.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): optimize by reusing explicit command-scoped state at the service boundary instead of introducing hidden ambient caches.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep validation logic reviewable and fail closed while reducing repeated work.
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): the optimization must preserve the repository validation contract rather than trading correctness for speed.

## Affected Surfaces
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/tests/

## Options Considered
### Option 1
- Add loader-level caching for all governed loads involved in acceptance validation.
- Strength: could reduce repeated reads across more commands automatically.
- Tradeoff: spreads invalidation concerns across unrelated commands and weakens the explicit
  validation boundary.

### Option 2
- Add lazy service-scoped snapshots only to `AcceptanceReconciliationService`.
- Strength: bounded to one command-scoped service instance and aligned with the actual
  repeated-read hotspot.
- Tradeoff: introduces small local grouping helpers inside the service.

## Chosen Outcome
Accept Option 2. The implementation will add lazy service-scoped grouped snapshots inside
`AcceptanceReconciliationService` and keep loader behavior unchanged.

## Rationale and Tradeoffs
- The repeated-read defect is local to acceptance reconciliation, so a local service-scoped
  fix is easier to reason about and less risky than a broader loader cache.
- `ValidationAllService` already reuses one acceptance service instance for the full command,
  so the optimization composes with the current orchestration without new command wiring.
- The tradeoff is a small amount of local state in the acceptance service, but that state is
  bounded to the current command and can be covered directly with regression tests.

## Consequences and Follow-Up Impacts
- `AcceptanceReconciliationService` will own grouped snapshot helpers for the shared
  acceptance-validation inputs.
- Aggregate acceptance validation should reduce repeated loader reads materially while
  preserving current reconciliation results.
- The trace will need targeted read-count regressions, full validation evidence, and a
  follow-up review pass before closeout.

## Risks, Dependencies, and Assumptions
- The grouped snapshot helpers must continue to mirror the trace-specific query semantics for
  PRDs, contracts, and evidence.
- The implementation assumes one service instance continues to span aggregate acceptance
  validation in `ValidationAllService`.

## References
- [acceptance_reconciliation_snapshot_reuse.md](/home/j/WatchTowerPlan/docs/planning/prds/acceptance_reconciliation_snapshot_reuse.md)
- [acceptance_reconciliation_snapshot_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/features/acceptance_reconciliation_snapshot_reuse.md)
- [acceptance_reconciliation_snapshot_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/acceptance_reconciliation_snapshot_reuse.md)
