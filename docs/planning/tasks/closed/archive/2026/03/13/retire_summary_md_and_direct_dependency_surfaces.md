---
id: task.summary_surface_retirement.retire_summary.001
trace_id: trace.summary_surface_retirement
title: Retire SUMMARY.md and direct dependency surfaces
summary: Delete SUMMARY.md, remove the dedicated summary-continuity trace, and rewrite
  remaining repo-local references so no active surface depends on the retired summary
  entrypoint.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T01:46:46Z'
audience: shared
authority: authoritative
applies_to:
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- workflows/modules/foundations_context_review.md
- docs/planning/prds/
- docs/planning/decisions/
- docs/planning/design/
- docs/planning/tasks/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_traceability_index_sync.py
related_ids:
- trace.summary_surface_retirement
---

# Retire SUMMARY.md and direct dependency surfaces

## Summary
Delete SUMMARY.md, remove the dedicated summary-continuity trace, and rewrite remaining repo-local references so no active surface depends on the retired summary entrypoint.

## Scope
- Remove the root `SUMMARY.md` artifact and the dedicated summary-restoration
  trace, update active root/foundations/workflow/test surfaces, and rewrite the
  remaining direct historical dependencies that would otherwise break
  validation after the retirement.

## Done When
- The root summary and its dedicated continuity trace are removed, the
  surviving repo-local markdown links no longer target `SUMMARY.md`, the live
  entrypoint tests align with the retirement, and sync can rebuild without the
  retired path.
