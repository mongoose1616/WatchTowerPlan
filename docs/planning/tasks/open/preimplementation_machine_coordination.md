---
id: "task.preimplementation_repo_review_and_hardening.machine_coordination.001"
trace_id: "trace.preimplementation_repo_review_and_hardening"
title: "Strengthen the machine coordination start-here surface"
summary: "Elevate the initiative index into the explicit machine coordination start-here path for traced work and expose it through clearer query and documentation surfaces."
type: "task"
status: "active"
task_status: "ready"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T17:55:24Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/schemas/artifacts/initiative_index.v1.schema.json"
  - "core/control_plane/indexes/initiatives/initiative_index.v1.json"
  - "core/python/src/watchtower_core/repo_ops/query/initiatives.py"
  - "core/python/src/watchtower_core/repo_ops/sync/initiative_index.py"
  - "core/python/src/watchtower_core/cli/"
  - "docs/planning/"
  - "docs/commands/core_python/"
related_ids:
  - "decision.preimplementation_machine_coordination_entrypoint"
  - "prd.preimplementation_repo_review_and_hardening"
  - "design.features.preimplementation_repo_readiness"
  - "design.implementation.preimplementation_repo_hardening_execution"
---

# Strengthen the machine coordination start-here surface

## Summary
Elevate the initiative index into the explicit machine coordination start-here path for traced work and expose it through clearer query and documentation surfaces.

## Scope
- Enrich the initiative index with small active-task summaries.
- Add an explicit coordination query path and align command and planning docs with it.
- Keep authored planning families and traceability authority unchanged.

## Done When
- One clear machine coordination start-here path is documented and implemented.
- Agents can answer the first coordination question for traced work without manually reopening several planning indexes.

## Links
- [preimplementation_machine_coordination_entrypoint.md](/home/j/WatchTowerPlan/docs/planning/decisions/preimplementation_machine_coordination_entrypoint.md)
- [preimplementation_repo_readiness.md](/home/j/WatchTowerPlan/docs/planning/design/features/preimplementation_repo_readiness.md)

## Updated At
- `2026-03-10T17:55:24Z`
