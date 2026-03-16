---
id: task.post_rewrite_core_cleanup_and_surface_reduction.validation_closeout.005
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Validate and close post-rewrite core cleanup
summary: Run full validation, perform one more review loop, and close the trace when
  the added cleanup slices land and no new concrete issue remains in scope.
type: task
status: active
task_status: backlog
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T07:00:01Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
depends_on:
- task.post_rewrite_core_cleanup_and_surface_reduction.artifact_registry_retirement.008
---

# Validate and close post-rewrite core cleanup

## Summary
Run full validation, perform one more review loop, and close the trace when the added cleanup slices land and no new concrete issue remains in scope.

## Scope
- Rerun full repository validation after the added cleanup slices.
- Perform one confirmation-pass review loop focused on remaining rewrite leftovers.
- Close the initiative only if the current review scope surfaces no new actionable issue.

## Done When
- Full validation passes after the cleanup slices land.
- A final confirmation pass does not surface another concrete issue in the active review boundary.
