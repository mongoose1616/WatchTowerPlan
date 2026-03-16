---
id: task.refactor_review_and_hardening.workflow_route_discrimination.002
trace_id: trace.refactor_review_and_hardening
title: Clarify workflow route discrimination and documentation review routing
summary: Distinguish adjacent workflow routes in authored workflow surfaces, route-preview
  metadata, and regression coverage so bounded documentation audits stop falling through
  to broader review routes.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T14:38:36Z'
audience: shared
authority: authoritative
applies_to:
- workflows/ROUTING_TABLE.md
- workflows/modules/
- core/control_plane/indexes/routes/
- core/control_plane/indexes/workflows/
- core/control_plane/registries/workflows/
- docs/commands/core_python/watchtower_core_route_preview.md
- core/python/tests/unit/
related_ids:
- trace.refactor_review_and_hardening
- prd.refactor_review_and_hardening
- design.features.refactor_review_and_hardening
- design.implementation.refactor_review_and_hardening
- decision.refactor_review_and_hardening_direction
- contract.acceptance.refactor_review_and_hardening
---

# Clarify workflow route discrimination and documentation review routing

## Summary
Distinguish adjacent workflow routes in authored workflow surfaces, route-preview metadata, and regression coverage so bounded documentation audits stop falling through to broader review routes.

## Scope
- Publish a dedicated documentation-review route and workflow metadata entry.
- Sharpen adjacent routing-table and workflow-module wording so documentation review, documentation refresh, repository review, and reconciliation routes remain distinct.
- Keep command docs, route/workflow indexes, registry metadata, and route-preview regressions aligned with the refined route boundary.

## Done When
- Bounded documentation review prompts select the dedicated documentation-review route instead of broad repository review or no match.
- Routing-table prose, workflow metadata, command docs, and targeted regressions agree on the adjacent route distinctions.
