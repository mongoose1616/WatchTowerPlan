---
id: task.foundation_scope_and_entrypoint_realignment.root_entrypoint_contract.001
trace_id: trace.foundation_scope_and_entrypoint_realignment
title: Tighten root and planning entrypoint contract
summary: Keep the root as a thin router, point humans and agents at the updated scope
  guidance, and align top-level entrypoint docs with the clarified foundation boundary.
type: task
status: active
task_status: done
task_kind: documentation
priority: medium
owner: repository_maintainer
updated_at: '2026-03-11T01:39:27Z'
audience: shared
authority: authoritative
applies_to:
- README.md
- docs/planning/README.md
- docs/foundations/README.md
related_ids:
- prd.foundation_scope_and_entrypoint_realignment
- design.features.foundation_scope_and_entrypoint_realignment
- design.implementation.foundation_scope_and_entrypoint_realignment
- decision.foundation_scope_boundary
depends_on:
- task.foundation_scope_and_entrypoint_realignment.repository_scope_alignment.001
---

# Tighten root and planning entrypoint contract

## Summary
Keep the root as a thin router, point humans and agents at the updated scope guidance, and align top-level entrypoint docs with the clarified foundation boundary.

## Scope
- Update the root README and nearby entrypoint docs so they route to repository scope and coordination rather than carrying broad narrative context.
- Keep top-level entrypoints thin and avoid duplicating deeper family documentation in root surfaces.
- Align any affected entrypoint notes with the whole-repo summary and clarified scope model.

## Done When
- Root and planning entrypoints reflect the clarified repository scope model.
- Top-level entrypoint docs stay thin and route readers to the right deeper surfaces.
