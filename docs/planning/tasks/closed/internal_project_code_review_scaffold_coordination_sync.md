---
id: task.internal_project_code_review_and_hardening.scaffold_coordination_sync.001
trace_id: trace.internal_project_code_review_and_hardening
title: Refresh traced coordination surfaces after plan scaffold writes
summary: Make plan scaffold write mode rebuild traceability, initiative, planning,
  and coordination surfaces for traced planning docs.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T16:17:08Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/src/watchtower_core/cli/plan_handlers.py
- docs/commands/core_python/watchtower_core_plan_scaffold.md
related_ids:
- prd.internal_project_code_review_and_hardening
- decision.internal_project_code_review_and_hardening_direction
- design.features.internal_project_code_review_and_hardening
- design.implementation.internal_project_code_review_and_hardening
---

# Refresh traced coordination surfaces after plan scaffold writes

## Summary
Make plan scaffold write mode rebuild traceability, initiative, planning, and coordination surfaces for traced planning docs.

## Scope
- Refresh the coordination sync group after traced plan scaffold writes.
- Keep family-specific planning indexes and trackers aligned in the same write path.
- Add regression coverage proving traced scaffold writes appear in traceability and initiative queries immediately.

## Done When
- Writing a traced PRD, design, implementation plan, or decision scaffold refreshes traceability, initiative, planning, and coordination surfaces.
- Command payloads and docs accurately describe the refreshed surfaces.
- Regression tests fail before the fix and pass after it.
