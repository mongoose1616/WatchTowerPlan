---
id: task.planning_artifact_retention_and_purge.workflow_and_ledger.003
trace_id: trace.planning_artifact_retention_and_purge
title: Implement guarded trace purge workflow and minimal purge ledger
summary: Add the purge ledger, safety checks, and repo-local implementation path that
  removes a closed trace package only when retention criteria are satisfied.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T03:35:24Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/src/watchtower_core/
- docs/planning/
related_ids:
- prd.planning_artifact_retention_and_purge
- design.features.planning_artifact_retention_and_purge
- design.implementation.planning_artifact_retention_and_purge
- decision.planning_artifact_retention_and_purge_direction
- contract.acceptance.planning_artifact_retention_and_purge
depends_on:
- task.planning_artifact_retention_and_purge.standard_alignment.002
---

# Implement guarded trace purge workflow and minimal purge ledger

## Summary
Add the purge ledger, safety checks, and repo-local implementation path that removes a closed trace package only when retention criteria are satisfied.

## Scope
- Add one minimal machine-readable purge ledger for traces removed from the planning corpus.
- Implement a guarded repo-local workflow or command path that deletes a whole closed trace package and records the purge atomically.
- Fail closed when a surviving canonical surface still depends on the trace being purged.

## Done When
- A bounded implementation surface can purge one eligible trace end to end.
- The purge writes the minimal surviving ledger entry and refreshes derived surfaces.
- The workflow refuses partial or unsafe purges.
