---
trace_id: trace.acceptance_reconciliation_snapshot_reuse
id: prd.acceptance_reconciliation_snapshot_reuse
title: Acceptance Reconciliation Snapshot Reuse PRD
summary: Eliminate repeated trace-level rereads inside acceptance reconciliation by
  reusing command-scoped validated planning and evidence snapshots without weakening
  validation fidelity.
type: prd
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

# Acceptance Reconciliation Snapshot Reuse PRD

## Record Metadata
- `Trace ID`: `trace.acceptance_reconciliation_snapshot_reuse`
- `PRD ID`: `prd.acceptance_reconciliation_snapshot_reuse`
- `Status`: `active`
- `Linked Decisions`: `decision.acceptance_reconciliation_snapshot_reuse_direction`
- `Linked Designs`: `design.features.acceptance_reconciliation_snapshot_reuse`
- `Linked Implementation Plans`: `design.implementation.acceptance_reconciliation_snapshot_reuse`
- `Updated At`: `2026-03-12T17:02:50Z`

## Summary
Eliminate repeated trace-level rereads inside acceptance reconciliation by reusing command-scoped validated planning and evidence snapshots without weakening validation fidelity.

## Problem Statement
The comprehensive optimization review found a real scaling defect in the acceptance
validation slice. `ValidationAllService._validate_acceptance()` currently validates `33`
trace targets, but `AcceptanceReconciliationService.validate()` rereads the same
traceability, PRD, acceptance-contract, validation-evidence, and validator-registry
surfaces once per trace. Direct instrumentation on the live repository shows one
acceptance-family pass performs `34` traceability loads, `34` PRD index loads, `34`
acceptance-contract directory scans, `34` validation-evidence directory scans, and `33`
validator-registry loads. As the traced planning and evidence corpus grows, that
repeated loading increases validation cost without adding fidelity.

## Goals
- Reuse command-scoped validated acceptance-validation inputs across all per-trace
  reconciliation checks in one command run.
- Preserve the current reconciliation behavior, error reporting, and fail-closed
  validation semantics for both single-trace and aggregate acceptance validation.
- Close the optimization finding with direct instrumentation, regression coverage, full
  repository validation, and a clean follow-up review pass.

## Non-Goals
- Adding process-global or cross-command caches for planning, contract, or evidence data.
- Changing PRD, acceptance-contract, validation-evidence, or traceability schema shapes.
- Weakening validation by skipping schema-backed loading or returning stale snapshot data
  across separate commands.

## Requirements
- `req.acceptance_reconciliation_snapshot_reuse.001`: Acceptance reconciliation must reuse
  command-scoped validated snapshots of traceability, PRD, acceptance-contract,
  validation-evidence, and validator-registry data instead of rereading those sources once
  per trace.
- `req.acceptance_reconciliation_snapshot_reuse.002`: The snapshot-reuse path must preserve
  the same reconciliation outcomes, validator coverage checks, and fail-closed behavior as
  the current per-trace implementation.
- `req.acceptance_reconciliation_snapshot_reuse.003`: The implementation must remain scoped
  to the current service or command so later commands never inherit stale planning or
  evidence state.
- `req.acceptance_reconciliation_snapshot_reuse.004`: The initiative must prove the reuse
  improvement with direct instrumentation and keep the repository green on the normal
  validation baseline.

## Acceptance Criteria
- `ac.acceptance_reconciliation_snapshot_reuse.001`: The trace publishes a fully-authored
  PRD, accepted direction decision, active feature design, active implementation plan,
  refreshed acceptance contract, refreshed validation evidence, and bounded closed task set
  for `trace.acceptance_reconciliation_snapshot_reuse`.
- `ac.acceptance_reconciliation_snapshot_reuse.002`: Direct instrumentation shows aggregate
  acceptance validation reuses stable planning and evidence snapshots instead of rereading
  traceability, PRD, acceptance-contract, validation-evidence, and validator-registry data
  once per trace.
- `ac.acceptance_reconciliation_snapshot_reuse.003`: Single-trace and aggregate acceptance
  validation preserve the same reconciliation behavior and fail closed when required data is
  missing or invalid.
- `ac.acceptance_reconciliation_snapshot_reuse.004`: Targeted regressions plus the full
  repository validation baseline pass after the acceptance snapshot-reuse change lands.
- `ac.acceptance_reconciliation_snapshot_reuse.005`: A follow-up review of adjacent
  acceptance-validation, query, and aggregate-validation surfaces finds no additional
  actionable issues.

## Risks and Dependencies
- Snapshot reuse must stay service-scoped so later validation commands never observe stale
  inputs.
- The grouped snapshot helpers must remain faithful to the current query semantics for PRDs,
  contracts, and evidence by trace.
- The change depends on the current acceptance-validation contract continuing to treat
  traceability, PRD, acceptance contract, validation evidence, and validator registry as
  the authoritative reconciliation inputs.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the optimization should remove repeated work through explicit command-scoped composition rather than hidden ambient state.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): optimization must preserve fail-closed validation behavior and same-change alignment across human and machine surfaces.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): as the governed core grows, internal validation paths need to scale without eroding operator trust or fidelity.

## References
- [acceptance_reconciliation_snapshot_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/features/acceptance_reconciliation_snapshot_reuse.md)
- [acceptance_reconciliation_snapshot_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/acceptance_reconciliation_snapshot_reuse.md)
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
