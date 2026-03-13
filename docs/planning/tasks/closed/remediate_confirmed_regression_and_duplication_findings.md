---
id: task.regression_duplication_and_overstep_review.remediation.002
trace_id: trace.regression_duplication_and_overstep_review
title: Remediate confirmed regression and duplication findings
summary: Fix the confirmed traceability, governed-companion, validation, sync, and
  planning-surface defects from the regression-and-duplication review.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T03:45:03Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/validation/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
- docs/planning/
- docs/commands/core_python/
- docs/standards/
related_ids:
- trace.regression_duplication_and_overstep_review
- prd.regression_duplication_and_overstep_review
- design.features.regression_duplication_and_overstep_review
- design.implementation.regression_duplication_and_overstep_review
- decision.regression_duplication_and_overstep_review_direction
- contract.acceptance.regression_duplication_and_overstep_review
---

# Remediate confirmed regression and duplication findings

## Summary
Fix the confirmed traceability, governed-companion, validation, sync, and planning-surface defects from the regression-and-duplication review.

## Scope
- Fix trace-linked task omission by enforcing trace_id when trace.* related IDs are present.
- Repair acceptance-contract and validation-evidence task-path references when task moves change canonical task document paths.
- Add repo-local path validation and stale-related-path filtering across the affected validation and sync surfaces.
- Normalize the current review trace and the intersecting cancelled trace so planning docs, tasks, and trackers reflect the real repository state.

## Done When
- Targeted regression tests cover the confirmed defect classes and pass.
- Touched docs, governed artifacts, trackers, and indexes are aligned with the repaired behavior.
- The current review trace is ready for final validation and confirmation passes.
