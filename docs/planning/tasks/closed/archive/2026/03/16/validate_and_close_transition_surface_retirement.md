---
id: task.transition_surface_retirement.validation_closeout.003
trace_id: trace.transition_surface_retirement
title: Validate and close transition surface retirement
summary: Refreshes derived surfaces, runs the full validation stack, and closes the
  trace once no transition leftovers remain in scope.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T19:38:33Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
related_ids:
- prd.transition_surface_retirement
- design.features.transition_surface_retirement
- design.implementation.transition_surface_retirement
- decision.transition_surface_retirement_direction
- contract.acceptance.transition_surface_retirement
depends_on:
- task.transition_surface_retirement.implementation.002
---

# Validate and close transition surface retirement

## Summary
Refreshes derived surfaces, runs the full validation stack, and closes the trace once no transition leftovers remain in scope.

## Scope
- Refresh planning, repository-path, and coordination surfaces after the retirement slice lands.
- Run acceptance, validate-all, pytest, mypy, ruff, and targeted leftover-path audits.
- Close the initiative only when the scoped transition surfaces are gone and the repo is green.

## Done When
- Validation passes and the trace is ready for terminal closeout.
- No scoped compatibility facade, re-export bridge, or marker-only test path remains live.
