---
id: task.internal_project_code_review_and_hardening.closeout_planning_catalog_sync.001
trace_id: trace.internal_project_code_review_and_hardening
title: Refresh planning catalog during initiative closeout
summary: Make initiative closeout rebuild planning-catalog outputs so planning queries
  reflect terminal initiative state immediately.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T16:17:09Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/closeout/initiative.py
- core/python/src/watchtower_core/cli/closeout_handlers.py
- docs/commands/core_python/watchtower_core_closeout_initiative.md
related_ids:
- prd.internal_project_code_review_and_hardening
- decision.internal_project_code_review_and_hardening_direction
- design.features.internal_project_code_review_and_hardening
- design.implementation.internal_project_code_review_and_hardening
---

# Refresh planning catalog during initiative closeout

## Summary
Make initiative closeout rebuild planning-catalog outputs so planning queries reflect terminal initiative state immediately.

## Scope
- Refresh planning-catalog outputs as part of initiative closeout write mode.
- Expose the additional output path and sync behavior through closeout runtime surfaces and docs.
- Add regression coverage proving query planning reflects completed initiative state after closeout.

## Done When
- closeout initiative --write rebuilds planning-catalog outputs in the same write path as initiative and coordination surfaces.
- query planning shows the terminal initiative status and closed phase immediately after closeout.
- Tests and docs cover the additional derived output.
