---
id: "task.core_export_hardening_followup.public_api_boundary.001"
trace_id: "trace.core_export_hardening_followup"
title: "Harden the public export-safe API boundary"
summary: "Move repo-specific consumers onto repo_ops surfaces and stop advertising repo-specific query, sync, and aggregate validation APIs from top-level export-safe namespaces."
type: "task"
status: "active"
task_status: "ready"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T15:24:07Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/query/"
  - "core/python/src/watchtower_core/sync/"
  - "core/python/src/watchtower_core/validation/"
  - "core/python/src/watchtower_core/cli/"
  - "core/python/tests/"
related_ids:
  - "prd.core_export_hardening_followup"
  - "design.features.core_export_hardening"
  - "design.implementation.core_export_hardening_execution"
depends_on:
  - "task.core_export_hardening_followup.command_metadata.001"
---

# Harden the public export-safe API boundary

## Summary
Move repo-specific consumers onto repo_ops surfaces and stop advertising repo-specific query, sync, and aggregate validation APIs from top-level export-safe namespaces.

## Context
- The repo review found that top-level `watchtower_core.query`, `watchtower_core.sync`, and `ValidationAllService` still expose repo-specific behavior as if it were reusable core API.

## Scope
- Update internal repo-specific consumers to import `watchtower_core.repo_ops.*` directly.
- Narrow the top-level public exports so repo-specific services are not advertised as reusable surfaces.
- Add regression coverage for the tightened boundary.

## Done When
- Repo-specific consumers no longer depend on top-level export-safe convenience re-exports and the public boundary matches the intended architecture.

## Links
- [core_export_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_hardening.md)
- [core_export_hardening_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_hardening_execution.md)

## Updated At
- `2026-03-10T15:24:07Z`
