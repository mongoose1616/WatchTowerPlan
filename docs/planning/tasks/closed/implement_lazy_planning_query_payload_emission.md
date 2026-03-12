---
id: task.lazy_planning_query_payload_emission.handler_lazy_payloads.002
trace_id: trace.lazy_planning_query_payload_emission
title: Implement lazy planning query payload emission
summary: Add bounded lazy JSON payload emission for the planning, initiatives, and
  coordination query handlers so human output paths stop invoking the heavy planning
  serializers.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T20:58:20Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/tests/
related_ids:
- prd.lazy_planning_query_payload_emission
- design.implementation.lazy_planning_query_payload_emission
- decision.lazy_planning_query_payload_emission_direction
- contract.acceptance.lazy_planning_query_payload_emission
---

# Implement lazy planning query payload emission

## Summary
Add bounded lazy JSON payload emission for the planning, initiatives, and coordination query handlers so human output paths stop invoking the heavy planning serializers.

## Scope
- Update the shared CLI handler helper and the targeted planning query handlers to defer payload construction until JSON output is requested.

## Done When
- Human query planning, initiatives, and non-empty coordination paths skip serializer work; JSON payloads remain unchanged; targeted regressions pass.
