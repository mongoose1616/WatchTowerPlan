---
id: "task.core_export_hardening_followup.command_metadata.001"
trace_id: "trace.core_export_hardening_followup"
title: "Repair command implementation metadata"
summary: "Publish command-family implementation paths in command metadata instead of pointing every command at the thin root CLI entrypoint."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "medium"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:18:44Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/cli/"
  - "core/python/src/watchtower_core/repo_ops/sync/command_index.py"
  - "core/control_plane/indexes/commands/command_index.v1.json"
related_ids:
  - "prd.core_export_hardening_followup"
  - "design.features.core_export_hardening"
  - "design.implementation.core_export_hardening_execution"
depends_on:
  - "task.core_export_hardening_followup.sync_output_dir.001"
---

# Repair command implementation metadata

## Summary
Publish command-family implementation paths in command metadata instead of pointing every command at the thin root CLI entrypoint.

## Context
- The CLI split succeeded, but command metadata still reports `cli/main.py` for every command even though command families now live in separate modules.

## Scope
- Add explicit command-family implementation metadata to parser-derived command specs.
- Resync the command index and the related tests.

## Done When
- Command index entries point at useful command-family implementation surfaces.

## Links
- [core_export_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_hardening.md)
- [core_export_hardening_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_hardening_execution.md)

## Updated At
- `2026-03-10T16:18:44Z`
