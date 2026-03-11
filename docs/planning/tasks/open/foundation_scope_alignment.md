---
id: task.foundation_scope_and_entrypoint_realignment.repository_scope_alignment.001
trace_id: trace.foundation_scope_and_entrypoint_realignment
title: Align foundation scope with current repository boundary
summary: Add an explicit repository-scope foundation and realign the existing foundation
  layer so current repo truth and future WatchTower product narrative stop competing.
type: task
status: active
task_status: backlog
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T01:26:55Z'
audience: shared
authority: authoritative
applies_to:
- docs/foundations/
related_ids:
- prd.foundation_scope_and_entrypoint_realignment
- design.features.foundation_scope_and_entrypoint_realignment
- design.implementation.foundation_scope_and_entrypoint_realignment
- decision.foundation_scope_boundary
---

# Align foundation scope with current repository boundary

## Summary
Add an explicit repository-scope foundation and realign the existing foundation layer so current repo truth and future WatchTower product narrative stop competing.

## Scope
- Add an authoritative repository-scope foundation document and align the foundations README around it.
- Clarify product_direction.md and customer_story.md so future product narrative is visibly secondary to current repository scope.
- Clarify engineering_design_principles.md, engineering_stack_direction.md, and repository_standards_posture.md around the export boundary, compactness, and current runtime baseline.

## Done When
- The foundation layer distinguishes current repository-operating truth from future product narrative.
- The foundations README and linked foundation references are aligned with the new scope model.
