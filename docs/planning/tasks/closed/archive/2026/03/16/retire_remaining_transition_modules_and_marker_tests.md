---
id: task.transition_surface_retirement.implementation.002
trace_id: trace.transition_surface_retirement
title: Retire remaining transition modules and marker tests
summary: Removes the remaining compatibility facades, re-export bridges, and marker-only
  test files and repairs direct consumers.
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
- core/python/src/
- core/python/tests/
- docs/planning/
related_ids:
- prd.transition_surface_retirement
- design.features.transition_surface_retirement
- design.implementation.transition_surface_retirement
- decision.transition_surface_retirement_direction
- contract.acceptance.transition_surface_retirement
---

# Retire remaining transition modules and marker tests

## Summary
Removes the remaining compatibility facades, re-export bridges, and marker-only test files and repairs direct consumers.

## Scope
- Delete the live facade and re-export modules.
- Delete the marker-only test files and move direct imports and docs to the focused suites.
- Repair active planning or lookup surfaces so canonical links and derived indexes no longer point at retired paths.

## Done When
- The retired modules and marker files no longer exist in the live tree.
- Runtime, tests, docs, and derived planning surfaces resolve only the direct owners and focused suites.
