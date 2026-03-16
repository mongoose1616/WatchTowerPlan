---
id: task.planning_artifact_retention_and_purge.standard_alignment.002
trace_id: trace.planning_artifact_retention_and_purge
title: Align retention policy with canonical standards and purgeability rules
summary: Define the promote-then-purge standard, update directly affected guidance,
  and remove canonical assumptions that closed trace artifacts must be kept forever.
type: task
status: active
task_status: ready
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-15T10:42:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/governance/
- docs/planning/
related_ids:
- prd.planning_artifact_retention_and_purge
- design.features.planning_artifact_retention_and_purge
- design.implementation.planning_artifact_retention_and_purge
- decision.planning_artifact_retention_and_purge_direction
- contract.acceptance.planning_artifact_retention_and_purge
---

# Align retention policy with canonical standards and purgeability rules

## Summary
Define the promote-then-purge standard, update directly affected guidance, and remove canonical assumptions that closed trace artifacts must be kept forever.

## Scope
- Publish the canonical retention standard for closed traced planning artifacts and the same-change purge contract.
- Update directly affected governance and planning guidance that currently assumes archive permanence or historical task-path dependencies.
- Keep the surviving post-purge authority surfaces explicit so the policy does not live only in deleted artifacts.

## Done When
- The retention rule lives in an authoritative standard instead of only in planning docs.
- Directly affected guidance no longer assumes closed trace artifacts remain in the repo forever when a purge is recorded.
- The standard names what survives purge and what is removed.
