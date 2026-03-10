---
id: "task.preimplementation_repo_review_and_hardening.core_modularity.001"
trace_id: "trace.preimplementation_repo_review_and_hardening"
title: "Split core monoliths and add supplemental schema loading"
summary: "Refactor the largest coordination-facing Python modules into smaller family modules and add supplemental schema registration for future external pack-owned artifacts."
type: "task"
status: "active"
task_status: "done"
task_kind: "feature"
priority: "high"
owner: "repository_maintainer"
updated_at: "2026-03-10T18:47:27Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/cli/"
  - "core/python/src/watchtower_core/control_plane/"
  - "core/python/tests/"
  - "docs/commands/core_python/"
  - "core/control_plane/"
related_ids:
  - "prd.preimplementation_repo_review_and_hardening"
  - "design.features.preimplementation_repo_readiness"
  - "design.implementation.preimplementation_repo_hardening_execution"
depends_on:
  - "task.preimplementation_repo_review_and_hardening.machine_coordination.001"
---

# Split core monoliths and add supplemental schema loading

## Summary
Refactor the largest coordination-facing Python modules into smaller family modules and add supplemental schema registration for future external pack-owned artifacts.

## Scope
- Split the CLI handler and control-plane model monoliths into smaller modules with compatibility-preserving imports.
- Add a supplemental schema registration seam to the schema store.
- Update tests, docs, and command surfaces affected by the refactor.

## Done When
- The largest targeted modules are split into clearer family modules.
- Supplemental schemas can be registered without modifying the local schema catalog.
- The repository stays green after the refactor.

## Outcome
- CLI runtime behavior now lives in family-specific handler modules with a thin compatibility facade at `watchtower_core.cli.handlers`.
- The control-plane typed artifact layer now lives under `watchtower_core.control_plane.models/` with compatibility-preserving re-exports.
- `SchemaStore` and `ControlPlaneLoader` now accept supplemental schema documents for future external artifact packs without mutating the canonical schema catalog.
- Targeted and full-repo validation passed after the refactor.

## Links
- [preimplementation_repo_readiness.md](/home/j/WatchTowerPlan/docs/planning/design/features/preimplementation_repo_readiness.md)
- [preimplementation_repo_hardening_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/preimplementation_repo_hardening_execution.md)

## Updated At
- `2026-03-10T18:47:27Z`
