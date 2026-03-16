---
id: task.planning_artifact_retention_and_purge.validation_closeout.005
trace_id: trace.planning_artifact_retention_and_purge
title: Validate and close planning artifact retention and purge
summary: Run targeted and full validation, confirm the pilot purge behavior, refresh
  evidence, and close the retention-model trace once the cleanup path lands cleanly.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T03:43:18Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
related_ids:
- prd.planning_artifact_retention_and_purge
- design.features.planning_artifact_retention_and_purge
- design.implementation.planning_artifact_retention_and_purge
- decision.planning_artifact_retention_and_purge_direction
- contract.acceptance.planning_artifact_retention_and_purge
depends_on:
- task.planning_artifact_retention_and_purge.pilot_cleanup.004
---

# Validate and close planning artifact retention and purge

## Summary
Run targeted and full validation, confirm the pilot purge behavior, refresh evidence, and close the retention-model trace once the cleanup path lands cleanly.

## Scope
- Run targeted workflow, sync, and validation checks for the new purge path plus the affected planning families.
- Refresh acceptance evidence and derived planning surfaces after the pilot purge succeeds.
- Close the remaining tasks and initiative only after the retention policy and purge path are both clean.

## Done When
- Targeted and full validation passes without a new planning-retention regression.
- Acceptance evidence covers the final workflow and pilot-purge acceptance IDs.
- The initiative closes with coherent coordination, initiative, task, and traceability state.
