---
trace_id: "trace.core_python_foundation"
id: "decision.core_python_workspace_root"
title: "Core Python Workspace Root Decision"
summary: "Records the decision to use core/python as the single Python workspace root alongside the versioned control plane."
type: "decision_record"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T04:55:49Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/python/"
  - "core/control_plane/"
  - "docs/planning/design/features/core_python_workspace_and_harness.md"
aliases:
  - "python workspace root decision"
  - "core python root decision"
---

# Core Python Workspace Root Decision

## Record Metadata
- `Trace ID`: `trace.core_python_foundation`
- `Decision ID`: `decision.core_python_workspace_root`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.core_python_foundation`
- `Linked Designs`: `design.features.core_python_workspace_and_harness`; `design.implementation.control_plane_loaders_and_schema_store`
- `Linked Implementation Plans`: `design.implementation.control_plane_loaders_and_schema_store`
- `Updated At`: `2026-03-09T04:55:49Z`

## Summary
This decision records the choice to make `core/python/` the single Python workspace root and keep `core/control_plane/` as its versioned authored sibling.

## Decision Statement
Use `core/python/` as the only Python workspace root for package code, tooling, tests, and onboarding, while keeping `core/control_plane/` as the separate authored authority tree.

## Trigger or Source Request
The repository needed one clear home for all Python-specific surfaces and a stable boundary between authored machine-readable artifacts and executable runtime code.

## Current Context and Constraints
- `core/control_plane/` already existed as the versioned control-plane authority.
- The previous flat Python scaffold under `core/` did not fully satisfy the requirement to consolidate Python-specific surfaces.
- Future schema loading, validation, query, and evidence services should compose over the same workspace root.

## Affected Surfaces
- `core/python/`
- `core/control_plane/`
- `docs/planning/prds/core_python_foundation.md`
- `docs/planning/design/features/core_python_workspace_and_harness.md`
- `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md`

## Options Considered
### Option 1
- Keep a flat `core/src/`, `core/tests/`, and top-level `core/pyproject.toml` layout.
- Strength: conventional small-package layout.
- Tradeoff: Python-specific surfaces remain scattered directly under `core/` and blur the intended workspace boundary.

### Option 2
- Use `core/python/` as the only Python workspace root and keep `core/control_plane/` as a sibling authority tree.
- Strength: explicit boundary between authored control-plane artifacts and executable Python surfaces.
- Tradeoff: requires path churn and synchronized updates across docs, indexes, and onboarding surfaces.

### Option 3
- Fold Python code directly into `core/control_plane/`.
- Strength: fewer top-level directories under `core/`.
- Tradeoff: collapses the authored/runtime boundary and makes review, validation, and indexing less clear.

## Chosen Outcome
Adopt `core/python/` as the single Python workspace root and keep authored control-plane state in `core/control_plane/`.

## Rationale and Tradeoffs
- This layout is the clearest expression of the repository’s authority model.
- It keeps Python onboarding and tooling discoverable in one place.
- It makes future loaders, validators, and query services easier to reason about because they are consumers of the control plane, not the control plane itself.

## Consequences and Follow-Up Impacts
- All Python code, tests, tool configuration, and local environment documentation should stay under `core/python/`.
- Future control-plane loaders, validation code, query code, and evidence code should be implemented against this boundary.
- Supporting docs, indexes, and onboarding surfaces must stay aligned whenever Python entrypoints change.

## Risks, Dependencies, and Assumptions
- Engineers must use the workspace contract consistently or the boundary will erode.
- The Python implementation still needs control-plane loaders and evidence support to realize the value of the chosen layout.
- The repository path index and planning docs must remain synchronized with the chosen root.

## References
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)
- [core_python_workspace_and_harness.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_python_workspace_and_harness.md)
- [control_plane_loaders_and_schema_store.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/control_plane_loaders_and_schema_store.md)
