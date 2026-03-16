---
id: task.coordination_projection_source_reuse.validation_closeout.003
trace_id: trace.coordination_projection_source_reuse
title: Validate and close coordination projection source reuse
summary: Run targeted and full validation, refresh acceptance evidence, and close
  the trace once the coordination projection reuse changes land cleanly.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T16:22:53Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
related_ids:
- prd.coordination_projection_source_reuse
- design.implementation.coordination_projection_source_reuse
- decision.coordination_projection_source_reuse_direction
- contract.acceptance.coordination_projection_source_reuse
depends_on:
- task.coordination_projection_source_reuse.loader_override_reuse.002
---

# Validate and close coordination projection source reuse

## Summary
Run targeted and full validation, refresh acceptance evidence, and close the trace once the
coordination projection reuse changes land cleanly.

## Scope
- Run the bounded targeted regressions and the full repository validation baseline after the
  reuse changes land.
- Refresh acceptance evidence, close the execution tasks, close the initiative, and confirm a
  no-new-issues follow-up review pass.
- Confirm the override reuse path preserves schema-validation boundaries for generated
  current-run artifacts.

## Done When
- Acceptance evidence and planning closeout surfaces reflect the delivered coordination
  projection reuse slice.
- `watchtower-core validate all`, `pytest -q`, `mypy`, and `ruff` pass after the change set
  lands.
- Generated current-run overrides remain schema-validated before downstream sync consumers
  reuse them.
- A final follow-up review pass of adjacent loader and sync surfaces finds no additional
  actionable issues.
