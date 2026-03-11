---
id: task.route_preview_natural_request_matching.hardening.001
trace_id: trace.route_preview_natural_request_matching
title: Harden route preview for natural maintenance requests
summary: Make advisory route preview match task-lifecycle and commit-closeout surfaces
  for natural report-review maintenance requests.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T14:16:05Z'
audience: shared
authority: authoritative
applies_to:
- workflows/ROUTING_TABLE.md
- core/control_plane/indexes/routes/route_index.v1.json
- core/python/src/watchtower_core/repo_ops/query/routes.py
- docs/commands/core_python/watchtower_core_route_preview.md
related_ids:
- prd.route_preview_natural_request_matching
- design.features.route_preview_natural_request_matching
- design.implementation.route_preview_natural_request_matching
---

# Harden route preview for natural maintenance requests

## Summary
Make advisory route preview match task-lifecycle and commit-closeout surfaces for natural report-review maintenance requests.

## Scope
- Fix deterministic route preview so requests phrased as review/fix/planning/tasks/validation/commits select the expected bounded workflow set.
- Keep the solution governed and lexical rather than introducing semantic routing.

## Done When
- The live request used in the final report review selects Repository Review, Task Lifecycle Management, Code Validation, and Commit Closeout.
- Route preview docs, route-index data, tests, and validation stay aligned in the same change set.
