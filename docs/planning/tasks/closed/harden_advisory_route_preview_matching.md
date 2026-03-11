---
id: task.standard_runtime_and_route_explicitness.route_preview_hardening.001
trace_id: trace.standard_runtime_and_route_explicitness
title: Harden advisory route preview matching
summary: Make route preview resilient to realistic free-form maintenance requests
  without changing its advisory authority model.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T04:46:44Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/query/routes.py
- docs/commands/core_python/watchtower_core_route_preview.md
- core/python/tests/unit/test_route_index_sync.py
related_ids:
- prd.standard_runtime_and_route_explicitness
- design.features.standard_runtime_and_route_explicitness
- design.implementation.standard_runtime_and_route_explicitness
- decision.standard_runtime_and_route_explicitness_direction
---

# Harden advisory route preview matching

## Summary
Make route preview resilient to realistic free-form maintenance requests without changing its advisory authority model.

## Scope
- Improve deterministic route-preview scoring beyond exact trigger-phrase matches.
- Add regression coverage for realistic broad maintenance requests and no-match behavior.
- Update the route-preview command docs to describe the stronger advisory matching.

## Done When
- A realistic report-driven maintenance request returns the expected routed workflow set.
- Route-preview tests cover the new scoring behavior and no-match guardrails.
- The command docs describe the updated advisory matching model.
