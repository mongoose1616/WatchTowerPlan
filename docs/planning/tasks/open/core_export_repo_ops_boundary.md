---
id: "task.core_export_readiness_and_optimization.repo_ops_boundary.001"
trace_id: "trace.core_export_readiness_and_optimization"
title: "Isolate repo-ops from reusable core"
summary: "Move repository-specific query, sync, validation, and planning-document semantics into explicit repo-ops surfaces so reusable layers stop depending on WatchTowerPlan-only behavior."
type: "task"
status: "active"
task_status: "ready"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T04:28:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/query/"
  - "core/python/src/watchtower_core/sync/"
  - "core/python/src/watchtower_core/validation/"
  - "core/python/src/watchtower_core/adapters/"
related_ids:
  - "prd.core_export_readiness_and_optimization"
  - "design.features.core_export_ready_architecture"
  - "design.implementation.core_export_readiness_execution"
---

# Isolate repo-ops from reusable core

## Summary
Move repository-specific query, sync, validation, and planning-document semantics into explicit repo-ops surfaces so reusable layers stop depending on WatchTowerPlan-only behavior.

## Context
- The current package mixes reusable coordination logic with repo-specific planning and Markdown-governance behavior.
- The export-ready boundary will not be credible until repo-specific behavior is isolated structurally and by import flow.

## Scope
- Create or formalize repo-ops package surfaces for planning-doc and Markdown-governance behavior.
- Separate reusable coordination families from repo-specific planning maintenance.
- Keep compatibility shims only where needed during migration.

## Done When
- Repo-specific planning behavior is grouped under explicit repo-ops surfaces.
- Reusable layers no longer depend on planning-doc semantics through accidental imports.

## Links
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_export_readiness_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_readiness_execution.md)
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)

## Updated At
- `2026-03-10T04:28:34Z`
