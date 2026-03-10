---
id: "task.core_export_hardening_followup.sync_output_dir.001"
trace_id: "trace.core_export_hardening_followup"
title: "Make output-directory sync snapshots dependency-correct"
summary: "Ensure sync output directories feed later dependent targets from the materialized snapshot instead of stale canonical derived artifacts."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:02:31Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/control_plane/workspace.py"
  - "core/python/src/watchtower_core/repo_ops/sync/"
  - "core/python/tests/unit/test_all_sync.py"
related_ids:
  - "prd.core_export_hardening_followup"
  - "design.features.core_export_hardening"
  - "design.implementation.core_export_hardening_execution"
---

# Make output-directory sync snapshots dependency-correct

## Summary
Ensure sync output directories feed later dependent targets from the materialized snapshot instead of stale canonical derived artifacts.

## Context
- The repo review found that `sync all --output-dir` can write internally inconsistent snapshots because later targets still read canonical derived artifacts from the repo.

## Scope
- Add the minimal overlay-loading behavior needed for generated artifact reads in output-directory mode.
- Add regression coverage for stale-canonical downstream indexes.

## Done When
- Output-directory sync runs produce dependency-correct coordination outputs and the regression is covered by tests.

## Links
- [core_export_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_hardening.md)
- [core_export_hardening_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_hardening_execution.md)

## Updated At
- `2026-03-10T16:02:31Z`
