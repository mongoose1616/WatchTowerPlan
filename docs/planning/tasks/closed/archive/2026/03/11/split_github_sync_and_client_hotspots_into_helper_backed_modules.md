---
id: task.repo_local_hotspot_modularity.github_integration.001
trace_id: trace.repo_local_hotspot_modularity
title: Split GitHub sync and client hotspots into helper-backed modules
summary: Reduce centralization in GitHub task sync and client request handling while
  preserving the current WatchTowerPlan GitHub contract.
type: task
status: active
task_status: done
task_kind: chore
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T06:19:10Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/sync/github_tasks.py
- core/python/src/watchtower_core/integrations/github/client.py
- core/python/tests/
related_ids:
- prd.repo_local_hotspot_modularity
- design.features.repo_local_hotspot_modularity
- design.implementation.repo_local_hotspot_modularity
depends_on:
- task.repo_local_hotspot_modularity.bootstrap.001
---

# Split GitHub sync and client hotspots into helper-backed modules

## Summary
Reduce centralization in GitHub task sync and client request handling while preserving the current WatchTowerPlan GitHub contract.

## Scope
- Split GitHub task sync payload building, issue reconciliation, and label/project handling into smaller helpers while keeping GitHubTaskSyncService stable.
- Split GitHub client request, mutation, and response helpers into smaller modules while keeping GitHubClient stable.

## Done When
- github_tasks.py and integrations/github/client.py are materially smaller or thin facades backed by helper modules.
- GitHub task sync and client regression tests stay green without changing current behavior.
