---
id: "task.end_to_end_repo_review_and_rationalization.derived_metadata.001"
trace_id: "trace.end_to_end_repo_review_and_rationalization"
title: "Harden derived coordination metadata around closeout state"
summary: "Make traceability-derived initiative and coordination surfaces keep timestamps aligned with closeout-driven state changes so current-state trackers remain trustworthy."
type: "task"
status: "active"
task_status: "ready"
task_kind: "bug"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/closeout/"
  - "core/python/src/watchtower_core/repo_ops/sync/"
  - "core/python/tests/"
  - "docs/planning/"
related_ids:
  - "prd.end_to_end_repo_review_and_rationalization"
  - "design.features.end_to_end_repo_rationalization"
  - "design.implementation.end_to_end_repo_rationalization_execution"
depends_on:
  - "task.end_to_end_repo_review_and_rationalization.bootstrap.001"
---

# Harden derived coordination metadata around closeout state

## Summary
Make traceability-derived initiative and coordination surfaces keep timestamps aligned with closeout-driven state changes so current-state trackers remain trustworthy.

## Scope
- Fix closeout-aware timestamp projection in traceability-derived initiative and coordination surfaces.
- Add regression tests covering initiative closeout and the affected derived trackers.
- Update any affected standards or command docs if timestamp semantics change materially.

## Done When
- Closeout-driven current-state surfaces no longer show stale pre-closeout timestamps.
- Regression tests cover the closeout path.
- Docs explain the resulting timestamp behavior clearly enough for maintainers.

## Links
- [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
- [end_to_end_repo_rationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/end_to_end_repo_rationalization_execution.md)

## Updated At
- `2026-03-10T19:43:34Z`
