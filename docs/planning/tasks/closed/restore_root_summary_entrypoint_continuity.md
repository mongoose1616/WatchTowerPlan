---
id: task.foundations_summary_entrypoint_continuity.restore.001
trace_id: trace.foundations_summary_entrypoint_continuity
title: Restore root summary entrypoint continuity
summary: Recreate the missing root SUMMARY.md document and add fail-closed coverage
  for the foundations-adjacent summary entrypoint.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T00:04:27Z'
audience: shared
authority: authoritative
applies_to:
- SUMMARY.md
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- core/python/tests/integration/test_control_plane_artifacts.py
related_ids:
- prd.foundations_summary_entrypoint_continuity
- decision.foundations_summary_entrypoint_continuity_direction
- contract.acceptance.foundations_summary_entrypoint_continuity
---

# Restore root summary entrypoint continuity

## Summary
Recreate the missing root SUMMARY.md document and add fail-closed coverage for the foundations-adjacent summary entrypoint.

## Scope
- Restore a durable root SUMMARY.md surface that supports the current foundations and planning references without rewriting those historical documents.
- Add regression coverage that fails if the root summary entrypoint disappears again while root and foundations entrypoints still reference it.

## Done When
- SUMMARY.md exists again and the broken foundations-adjacent references resolve.
- Integration coverage fails closed on future root-summary entrypoint removal.
