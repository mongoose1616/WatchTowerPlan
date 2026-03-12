---
trace_id: trace.acceptance_reconciliation_snapshot_reuse
id: design.features.acceptance_reconciliation_snapshot_reuse
title: Acceptance Reconciliation Snapshot Reuse Feature Design
summary: Defines the technical design boundary for Acceptance Reconciliation Snapshot
  Reuse.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-12T17:02:50Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/tests/
---

# Acceptance Reconciliation Snapshot Reuse Feature Design

## Record Metadata
- `Trace ID`: `trace.acceptance_reconciliation_snapshot_reuse`
- `Design ID`: `design.features.acceptance_reconciliation_snapshot_reuse`
- `Design Status`: `active`
- `Linked PRDs`: `prd.acceptance_reconciliation_snapshot_reuse`
- `Linked Decisions`: `decision.acceptance_reconciliation_snapshot_reuse_direction`
- `Linked Implementation Plans`: `design.implementation.acceptance_reconciliation_snapshot_reuse`
- `Updated At`: `2026-03-12T17:02:50Z`

## Summary
Defines the technical design boundary for Acceptance Reconciliation Snapshot Reuse.

## Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope and Feature Boundary
- Covers command-scoped reuse of acceptance-validation inputs inside
  `AcceptanceReconciliationService`.
- Covers aggregate `validate all` acceptance execution and direct single-trace validation.
- Excludes broad loader caching, schema or contract shape changes, and unrelated refactors
  in the query or validation families.

## Current-State Context
- `ValidationAllService` reuses one `AcceptanceReconciliationService` instance across all
  acceptance targets, but the service itself currently rebuilds the same traceability, PRD,
  acceptance-contract, validation-evidence, and validator-registry views on every trace.
- The current query helpers are already thin filters over complete in-memory corpora, so the
  repeated rereads do not add semantic precision.
- Instrumentation on the live repo shows `34/34/34/34/33` loader calls for those shared
  surfaces during one aggregate acceptance pass.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the design should reuse shared command-scoped state at the orchestration boundary instead of pushing ad hoc caching into loaders or query handlers.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the optimization must stay reviewable and fail closed.

## Internal Standards and Canonical References Applied
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): validation behavior and coverage must remain intact after the optimization.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): acceptance reconciliation still has to read the same authoritative trace-linked planning surfaces.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): implementation belongs in the canonical Python workspace and should preserve thin command boundaries.

## Design Goals and Constraints
- Reuse already-validated acceptance inputs within one reconciliation-service lifetime.
- Keep the reuse boundary service-scoped rather than introducing cross-command state.
- Preserve the current per-trace reconciliation results and issue shapes exactly.

## Options Considered
### Option 1
- Add broad loader-level caching for all index and directory loads.
- Strength: could benefit more command families automatically.
- Tradeoff: risky because stale-state invalidation would spread across unrelated commands and
  obscure validation boundaries.

### Option 2
- Add explicit lazy snapshot reuse inside `AcceptanceReconciliationService`.
- Strength: bounded to one command-scoped service instance and aligned with current
  acceptance-validation inputs.
- Tradeoff: requires local grouping helpers and a small amount of state in the service.

## Recommended Design
### Architecture
- Extend `AcceptanceReconciliationService` with lazy snapshot helpers for:
  - traceability entries by trace
  - PRD entries by trace
  - acceptance contracts by trace
  - validation evidence by trace
  - validator IDs
- Keep `ValidationAllService` unchanged so it benefits automatically from the service-scoped
  snapshots it already reuses.
- Preserve the current direct command path for `watchtower-core validate acceptance`, which
  continues to instantiate one fresh service per command.

### Data and Interface Impacts
- No schema, contract, index, or CLI output shapes change.
- Runtime impacts stay limited to acceptance-validation internals and regression tests.
- Query services remain authoritative for query commands; acceptance validation can use local
  grouped snapshots because it only needs exact trace-scoped subsets.

### Execution Flow
1. The first `validate(trace_id)` call lazily loads the shared traceability, PRD,
   acceptance-contract, validation-evidence, and validator-registry inputs.
2. The service groups those inputs by `trace_id` or stable key and reuses them across later
   trace validations in the same command.
3. Each validation still performs the same acceptance, traceability, evidence, and validator
   comparisons against the trace-specific subsets.

### Invariants and Failure Cases
- Missing trace entries, PRDs, contracts, evidence, or validators must still produce the same
  fail-closed validation issues as today.
- Snapshot reuse must not leak across service instances or later commands.
- Aggregate validation should reduce repeated loader reads without changing the number of
  acceptance targets or their outcomes.

## Affected Surfaces
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/tests/

## Design Guardrails
- Do not add persistent cache state to `ControlPlaneLoader`.
- Do not let optimization concerns change acceptance reconciliation semantics or output order.

## Risks
- Local snapshot grouping could drift from query-service semantics if the acceptance service
  stops using the same filtering rules by trace.

## References
- [acceptance_reconciliation_snapshot_reuse.md](/home/j/WatchTowerPlan/docs/planning/prds/acceptance_reconciliation_snapshot_reuse.md)
- [acceptance_reconciliation_snapshot_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/acceptance_reconciliation_snapshot_reuse.md)
- [acceptance.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/acceptance.py)
- [all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/validation/all.py)
