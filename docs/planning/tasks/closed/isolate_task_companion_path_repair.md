---
id: task.planning_authoring_hotspot_regression_hardening.task_companion_repair.003
trace_id: trace.planning_authoring_hotspot_regression_hardening
title: Isolate governed task companion path repair
summary: Extract acceptance-contract and validation-evidence task-path repair from
  TaskLifecycleService while preserving task mutation behavior and governed companion
  alignment.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T17:36:16Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/task_companion_path_repair.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle_support.py
- core/python/src/watchtower_core/repo_ops/README.md
- core/python/tests/unit/test_task_companion_path_repair.py
- core/python/tests/
- docs/commands/core_python/
related_ids:
- prd.planning_authoring_hotspot_regression_hardening
- design.features.planning_authoring_hotspot_regression_hardening
- design.implementation.planning_authoring_hotspot_regression_hardening
- decision.planning_authoring_hotspot_regression_hardening_direction
- contract.acceptance.planning_authoring_hotspot_regression_hardening
---

# Isolate governed task companion path repair

## Summary
Extract acceptance-contract and validation-evidence task-path repair from TaskLifecycleService while preserving task mutation behavior and governed companion alignment.

## Scope
- Move governed acceptance-contract and validation-evidence task-path repair into a dedicated helper-backed collaborator.
- Preserve canonical applies_to handling, coordination refresh, and task move semantics.
- Keep task docs, runtime-boundary docs, and lifecycle regressions aligned with the split.

## Done When
- TaskLifecycleService no longer owns governed companion traversal details directly.
- Task-path repair still updates acceptance and evidence artifacts before old task paths disappear.
- Targeted lifecycle and handler tests remain green.
