---
id: "task.core_export_readiness_and_optimization.command_registry.001"
trace_id: "trace.core_export_readiness_and_optimization"
title: "Establish registry-backed CLI authority"
summary: "Introduce registry-backed CLI command authority so parser wiring, command lookup, and command-surface maintenance no longer depend on one monolithic CLI file and doc-derived machine metadata."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T05:14:33Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/cli/"
  - "core/python/src/watchtower_core/sync/command_index.py"
  - "docs/commands/core_python/"
  - "core/control_plane/indexes/commands/command_index.v1.json"
related_ids:
  - "prd.core_export_readiness_and_optimization"
  - "design.features.core_export_ready_architecture"
  - "design.implementation.core_export_readiness_execution"
---

# Establish registry-backed CLI authority

## Summary
Introduce registry-backed CLI command authority so parser wiring, command lookup, and command-surface maintenance no longer depend on one monolithic CLI file and doc-derived machine metadata.

## Context
- The current CLI entrypoint is the largest coupling point in the package.
- Command behavior, machine lookup metadata, and help-surface maintenance need one explicit authority model before the broader export-ready refactor can progress cleanly.

## Scope
- Split the CLI into family modules and add registry-backed command specifications.
- Derive parser wiring and machine-readable command metadata from the registry while keeping human command docs aligned.
- Preserve the current command surface during the refactor.

## Done When
- The root CLI entrypoint is thin and registry-backed.
- Command-index generation and CLI surface tests no longer depend on one monolithic parser file as the main authority.

## Links
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_export_readiness_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_readiness_execution.md)
- [command_documentation_and_lookup.md](/home/j/WatchTowerPlan/docs/planning/design/features/command_documentation_and_lookup.md)

## Updated At
- `2026-03-10T05:14:33Z`
