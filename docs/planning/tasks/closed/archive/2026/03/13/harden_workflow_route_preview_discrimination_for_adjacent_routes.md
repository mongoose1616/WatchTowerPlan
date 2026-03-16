---
id: task.workflow_route_boundary_discoverability_hardening.route_preview_discrimination.002
trace_id: trace.workflow_route_boundary_discoverability_hardening
title: Harden workflow route preview discrimination for adjacent routes
summary: Improve route-preview matching and selection so realistic reconciliation
  prompts resolve correctly and low-signal route leakage is filtered without hiding
  intentional multi-route requests.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T21:37:07Z'
audience: shared
authority: authoritative
applies_to:
- workflows/ROUTING_TABLE.md
- core/python/src/watchtower_core/repo_ops/query/routes.py
- core/control_plane/indexes/routes/route_index.v1.json
related_ids:
- prd.workflow_route_boundary_discoverability_hardening
- design.features.workflow_route_boundary_discoverability_hardening
- design.implementation.workflow_route_boundary_discoverability_hardening
- decision.workflow_route_boundary_discoverability_hardening_direction
- contract.acceptance.workflow_route_boundary_discoverability_hardening
depends_on:
- task.workflow_route_boundary_discoverability_hardening.bootstrap.001
---

# Harden workflow route preview discrimination for adjacent routes

## Summary
Improve route-preview matching and selection so realistic reconciliation prompts resolve correctly and low-signal route leakage is filtered without hiding intentional multi-route requests.

## Scope
- Review the current route-preview scorer, trigger-keyword set, and route-index sync path for the adjacent reconciliation and task routes.
- Implement deterministic matching and selection changes that fix the reproduced no-match and low-signal leakage cases without collapsing intentional multi-route unions.
- Keep the authored routing table and derived route index aligned with the final behavior.

## Done When
- Realistic documentation-implementation and governed-artifact reconciliation prompts resolve to the intended routes in route preview.
- The reproduced phase-transition prompt no longer leaks Code Validation solely because of a low-signal validation token.
- Focused route-preview regressions cover the fixed prompts and pass.
