---
id: task.summary_surface_retirement.validation.002
title: Validate and close summary surface retirement
summary: Run targeted and full validation, refresh evidence, rerun confirmation passes,
  and close the summary-retirement slice.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T01:47:55Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/contracts/acceptance/summary_surface_retirement_acceptance.v1.json
- core/control_plane/ledgers/validation_evidence/summary_surface_retirement_planning_baseline.v1.json
- docs/planning/prds/summary_surface_retirement.md
related_ids:
- trace.summary_surface_retirement
---

# Validate and close summary surface retirement

## Summary
Run targeted and full validation, refresh evidence, rerun confirmation passes, and close the summary-retirement slice.

## Scope
- Validate the summary retirement changes, refresh acceptance evidence, run post-fix confirmation passes, and close the initiative with updated planning trackers and indexes.

## Done When
- Targeted and full validation are green, no surviving repo-local markdown link
  targets `SUMMARY.md`, and the initiative is closed cleanly.
