---
id: task.unit_test_hardening_and_rebalancing.cli_lifecycle_coverage.001
trace_id: trace.unit_test_hardening_and_rebalancing
title: Harden command and lifecycle coverage
summary: Add direct handler and service coverage for closeout, route, plan, task,
  query, and lifecycle behavior that current CLI smoke tests do not cover deeply enough.
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
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/closeout/
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/tests/unit/
related_ids:
- prd.unit_test_hardening_and_rebalancing
- design.features.unit_test_hardening_and_rebalancing
- design.implementation.unit_test_hardening_and_rebalancing
depends_on:
- task.unit_test_hardening_and_rebalancing.bootstrap.001
---

# Harden command and lifecycle coverage

## Summary
Add direct handler and service coverage for closeout, route, plan, task, query, and lifecycle behavior that current CLI smoke tests do not cover deeply enough.

## Scope
- Add direct handler tests for closeout, route, plan, task, and representative query families in both JSON and human-output modes.
- Add branch-focused service tests for lifecycle and planning helper behavior that remain under-covered.

## Done When
- Low-coverage command and lifecycle modules have direct unit coverage for meaningful success and failure branches.
- CLI smoke tests no longer carry most behavior assertions for these surfaces.
