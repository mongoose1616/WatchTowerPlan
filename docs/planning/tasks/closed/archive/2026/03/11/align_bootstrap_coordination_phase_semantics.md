---
id: task.internal_project_code_review_followup.bootstrap_phase_semantics_alignment.001
trace_id: trace.internal_project_code_review_followup
title: Align bootstrap coordination phase semantics
summary: Keep bootstrap-only planning traces in implementation_planning until real
  execution work exists.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T17:13:25Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/integration/test_planning_scaffolds_service.py
related_ids:
- prd.internal_project_code_review_followup
- decision.internal_project_code_review_followup_direction
- design.features.internal_project_code_review_followup
- design.implementation.internal_project_code_review_followup
---

# Align bootstrap coordination phase semantics

## Summary
Keep bootstrap-only planning traces in implementation_planning until real execution work exists.

## Scope
- Keep bootstrap-only traces from projecting execution before bounded execution tasks exist.
- Add regression coverage for initiative and planning projections after bootstrap writes.

## Done When
- Bootstrap-only traces project implementation_planning instead of execution.
- Initiative and planning query surfaces stay aligned on the corrected phase semantics.
