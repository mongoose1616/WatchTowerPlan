---
id: task.acceptance_reconciliation_snapshot_reuse.validation_closeout.003
trace_id: trace.acceptance_reconciliation_snapshot_reuse
title: Validate and close acceptance reconciliation snapshot reuse
summary: Run targeted and full validation, refresh acceptance evidence, and close
  the trace once the acceptance snapshot-reuse change lands cleanly.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T17:17:13Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
related_ids:
- prd.acceptance_reconciliation_snapshot_reuse
- design.implementation.acceptance_reconciliation_snapshot_reuse
- decision.acceptance_reconciliation_snapshot_reuse_direction
- contract.acceptance.acceptance_reconciliation_snapshot_reuse
depends_on:
- task.acceptance_reconciliation_snapshot_reuse.snapshot_reuse.002
---

# Validate and close acceptance reconciliation snapshot reuse

## Summary
Run targeted and full validation, refresh acceptance evidence, and close the trace once the
acceptance snapshot-reuse change lands cleanly.

## Scope
- Run the bounded targeted regressions and the full repository validation baseline after the
  reuse change lands.
- Refresh acceptance evidence, close the execution tasks, close the initiative, and confirm
  a no-new-issues follow-up review pass.

## Done When
- Acceptance evidence and planning closeout surfaces reflect the delivered acceptance
  snapshot-reuse slice.
- `watchtower-core validate all`, `pytest -q`, `mypy`, and `ruff` pass after the change set
  lands.
- A final follow-up review pass of adjacent acceptance-validation and aggregate-validation
  surfaces finds no additional actionable issues.
