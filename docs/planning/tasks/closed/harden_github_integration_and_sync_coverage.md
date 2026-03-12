---
id: task.unit_test_hardening_and_rebalancing.github_coverage.001
trace_id: trace.unit_test_hardening_and_rebalancing
title: Harden GitHub integration and sync coverage
summary: Add direct deterministic unit coverage for GitHub client behavior and GitHub
  task-sync write or failure paths.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T02:46:38Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/integrations/github/
- core/python/src/watchtower_core/repo_ops/sync/github_tasks.py
- core/python/tests/unit/
related_ids:
- prd.unit_test_hardening_and_rebalancing
- design.features.unit_test_hardening_and_rebalancing
- design.implementation.unit_test_hardening_and_rebalancing
depends_on:
- task.unit_test_hardening_and_rebalancing.bootstrap.001
---

# Harden GitHub integration and sync coverage

## Summary
Add direct deterministic unit coverage for GitHub client behavior and GitHub task-sync write or failure paths.

## Scope
- Add mocked GitHubClient tests for REST, GraphQL, pagination, label, and error branches.
- Add GitHubTaskSyncService tests for create, update, project, binding validation, local writeback, and failure handling.

## Done When
- GitHub client and task-sync write or failure paths have direct deterministic unit coverage.
- No live network access is needed for GitHub coverage.
