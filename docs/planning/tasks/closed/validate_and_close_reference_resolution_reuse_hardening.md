---
id: task.reference_resolution_reuse_hardening.validation_closeout.002
trace_id: trace.reference_resolution_reuse_hardening
title: Validate and close reference-resolution reuse hardening
summary: Run targeted and full validation, update acceptance evidence, and close the
  trace once the reference-resolution reuse changes land cleanly.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T15:15:23Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
related_ids:
- prd.reference_resolution_reuse_hardening
- design.implementation.reference_resolution_reuse_hardening
- decision.reference_resolution_reuse_hardening_direction
- contract.acceptance.reference_resolution_reuse_hardening
depends_on:
- task.reference_resolution_reuse_hardening.shared_resolution_reuse.001
---

# Validate and close reference-resolution reuse hardening

## Summary
Run targeted and full validation, update acceptance evidence, and close the trace once the reference-resolution reuse changes land cleanly.

## Scope
- Run the bounded targeted regressions and the full repository validation baseline after the reuse changes land.
- Refresh acceptance evidence, close the execution tasks, close the initiative, and confirm a no-new-issues follow-up review pass.

## Done When
- Acceptance evidence and planning closeout surfaces reflect the delivered reuse hardening slice.
- watchtower-core validate all, pytest -q, mypy, and ruff pass after the change set lands.
- A final follow-up review pass of adjacent validation and sync surfaces finds no additional actionable issues.
