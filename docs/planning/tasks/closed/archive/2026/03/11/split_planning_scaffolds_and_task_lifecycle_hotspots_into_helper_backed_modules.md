---
id: task.repo_local_hotspot_modularity.scaffolds_lifecycle.001
trace_id: trace.repo_local_hotspot_modularity
title: Split planning scaffolds and task lifecycle hotspots into helper-backed modules
summary: Reduce centralization in planning scaffold generation and task lifecycle
  mutation services without changing their current contracts.
type: task
status: active
task_status: done
task_kind: chore
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T06:19:00Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/tests/
related_ids:
- prd.repo_local_hotspot_modularity
- design.features.repo_local_hotspot_modularity
- design.implementation.repo_local_hotspot_modularity
depends_on:
- task.repo_local_hotspot_modularity.bootstrap.001
---

# Split planning scaffolds and task lifecycle hotspots into helper-backed modules

## Summary
Reduce centralization in planning scaffold generation and task lifecycle mutation services without changing their current contracts.

## Scope
- Split planning scaffold metadata normalization, section rendering, and bootstrap orchestration into helper modules while keeping PlanningScaffoldService stable.
- Split task lifecycle normalization, validation, and mutation helpers out of task_lifecycle.py while keeping TaskLifecycleService and current task documents stable.

## Done When
- planning_scaffolds.py and task_lifecycle.py are materially smaller or reduced to thin facades backed by helper modules.
- Planning scaffold and task lifecycle tests stay green without contract changes.
