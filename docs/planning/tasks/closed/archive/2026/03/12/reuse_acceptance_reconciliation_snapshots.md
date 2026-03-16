---
id: task.acceptance_reconciliation_snapshot_reuse.snapshot_reuse.002
trace_id: trace.acceptance_reconciliation_snapshot_reuse
title: Reuse acceptance reconciliation snapshots
summary: Eliminate repeated acceptance-validation rereads by reusing command-scoped
  traceability, PRD, contract, evidence, and validator snapshots.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T17:10:02Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/tests/
related_ids:
- prd.acceptance_reconciliation_snapshot_reuse
- design.features.acceptance_reconciliation_snapshot_reuse
- design.implementation.acceptance_reconciliation_snapshot_reuse
- decision.acceptance_reconciliation_snapshot_reuse_direction
- contract.acceptance.acceptance_reconciliation_snapshot_reuse
depends_on:
- task.acceptance_reconciliation_snapshot_reuse.bootstrap.001
---

# Reuse acceptance reconciliation snapshots

## Summary
Eliminate repeated acceptance-validation rereads by reusing command-scoped traceability,
PRD, contract, evidence, and validator snapshots.

## Scope
- Add lazy grouped snapshot helpers to `AcceptanceReconciliationService`.
- Preserve the same reconciliation findings and fail-closed behavior for direct and
  aggregate acceptance validation.
- Add targeted regressions proving reduced loader reads and preserved trace-level behavior.

## Done When
- Aggregate acceptance validation reuses shared reconciliation inputs instead of rereading
  them once per trace.
- Direct `AcceptanceReconciliationService.validate()` still passes for a live trace and
  preserves the same issue behavior for missing inputs.
- Targeted regression coverage proves the optimization boundary.
