---
trace_id: "trace.core_python_foundation"
id: "design.features.core_python_workspace_and_harness"
title: "Core Python Workspace and Harness Design"
summary: "Defines the feature-level technical design for the consolidated Python workspace under core/python and the first functional boundaries of the core helper and harness package."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T18:25:06Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/design/features/core_python_workspace_and_harness.md"
  - "core/python/"
  - "core/control_plane/"
  - "docs/planning/design/implementation/control_plane_loaders_and_schema_store.md"
aliases:
  - "core python workspace design"
  - "harness workspace design"
---

# Core Python Workspace and Harness Design

## Record Metadata
- `Trace ID`: `trace.core_python_foundation`
- `Design ID`: `design.features.core_python_workspace_and_harness`
- `Design Status`: `active`
- `Linked PRDs`: `prd.core_python_foundation`
- `Linked Decisions`: `decision.core_python_workspace_root`
- `Linked Implementation Plans`: `design.implementation.control_plane_loaders_and_schema_store`
- `Updated At`: `2026-03-09T18:25:06Z`

## Summary
This document defines the feature-level technical design for the consolidated Python workspace under `core/python/` and the first functional boundaries of the core helper and harness package.

## Source Request
- User request to plan the core layout, consolidate all Python-related surfaces in one Python folder, and define the onboarding surfaces needed for a standard local Python environment.
- Planning authority captured in [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md).
- Durable workspace-root choice captured in [core_python_workspace_root.md](/home/j/WatchTowerPlan/docs/planning/decisions/core_python_workspace_root.md).

## Scope and Feature Boundary
- Covers the workspace split between `core/control_plane/` and `core/python/`.
- Covers Python onboarding surfaces, package layout, and the first functional package boundaries for the helper and harness layer.
- Covers the initial feature categories that should exist in the Python core package.
- Does not implement validator, query, or sync behavior beyond scaffolding.
- Does not define domain-pack behavior or domain-pack-owned state.

## Current-State Context
- `core/control_plane/` already exists as the versioned machine-readable authority tree.
- `core/python/` is now the consolidated Python workspace root for package code, tests, tool configuration, and local environment surfaces.
- The earlier flat placeholder Python layout under `core/` has been retired in favor of the consolidated workspace root.
- Generated Python artifacts have already appeared directly under `core/`, which is a boundary leak the workspace design should prevent.
- Existing feature designs for validator execution and schema resolution assume a Python package surface but do not yet define the final workspace root.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keep the runtime deterministic, local-first, and separated from canonical machine-readable authority.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): keep core as the governed substrate and execution helper layer rather than a product-specific UI surface.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): favor Python for helper and harness logic and JSON Schema for machine-validated contracts.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): avoid parallel truth by keeping control-plane authority in artifacts and execution logic in Python.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): `core/python/` must remain the single Python workspace root with one onboarding contract.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): schema resolution should come from governed catalog records instead of hardcoded Python paths.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): new Python workspace surfaces need to remain discoverable through the derived path index.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): governed machine artifacts should stay schema-backed and fail closed.
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md): human guidance stays in Markdown while machine-readable control-plane artifacts stay in JSON.
- [python_validator_execution.md](/home/j/WatchTowerPlan/docs/planning/design/features/python_validator_execution.md): validator execution belongs in dedicated modular package surfaces rather than mixed workspace scripts.
- [schema_resolution_and_index_search.md](/home/j/WatchTowerPlan/docs/planning/design/features/schema_resolution_and_index_search.md): schema loading and index-backed lookup should be shared package capabilities from the start.

## Design Goals and Constraints
- Keep all Python-specific surfaces under one subtree.
- Keep authored control-plane artifacts outside the Python workspace.
- Make engineer onboarding predictable with one pinned interpreter, one lockfile, one local virtual environment, and one standard command set.
- Keep the initial package small and shaped around actual core capabilities rather than speculative domain abstractions.
- Avoid duplicate CLI trees, duplicate package roots, and committed cache or build artifacts.

## Options Considered
### Option 1
- Keep the flat `core/src/`, `core/tests/`, and `core/pyproject.toml` layout.
- Strengths: smallest immediate change and conventional enough for a simple package.
- Tradeoffs or reasons not chosen: Python onboarding files stay scattered directly under `core/`, and the layout does not satisfy the goal of consolidating Python-specific surfaces in one subtree.

### Option 2
- Create `core/python/` as the single Python workspace root alongside `core/control_plane/`.
- Strengths: clean separation between machine-readable authority and Python execution surfaces, simple onboarding, and one obvious home for tooling, envs, source, and tests.
- Tradeoffs or reasons not chosen: requires updating references, inventories, and the repository path index.

### Option 3
- Fold Python code into `core/control_plane/` or make the control plane a Python package resource tree.
- Strengths: fewer top-level directories under `core/`.
- Tradeoffs or reasons not chosen: blurs the authority boundary, couples authored artifacts to runtime tooling, and makes review and generation less clear.

## Recommended Design
### Architecture
- Keep `core/control_plane/` as the canonical authored authority tree.
- Add `core/python/` as the only Python workspace root.
- Keep one package root at `core/python/src/watchtower_core/`.
- Organize the package around actual core capabilities:
  - `control_plane/` for artifact loading and resolution
  - `validation/` for validator execution
  - `query/` for index-backed lookup
  - `adapters/` for front matter and artifact parsing
  - `evidence/` for structured outputs and issues
  - `sync/` for deterministic refresh and materialization of derived indexes and contracts
  - `cli/` for thin operator-facing commands
  - `utils/` for narrow shared helpers

### Data and Interface Impacts
- The Python workspace becomes the canonical home for `.python-version`, `pyproject.toml`, `uv.lock`, `.venv`, `src/`, `tests/`, and small helper tools.
- Existing feature designs that referenced `core/src/` and `core/tests/` should point to `core/python/src/` and `core/python/tests/` instead.
- The repository path index should advertise `core/python/` as the Python entrypoint rather than the old flat layout.
- The initial CLI should stay thin and package-local rather than growing a second source tree.
- Future workflow-assisted data entry should validate structured payloads and materialize derived JSON artifacts through package code rather than hand-editing indexes ad hoc.

### Execution Flow
1. An engineer enters `core/python/`.
2. `uv` resolves the pinned Python version from `.python-version` and syncs the workspace from `pyproject.toml` and `uv.lock`.
3. The local `.venv/` becomes the standard execution environment for tests, linting, typing, and CLI commands.
4. The Python package loads governed artifacts from `core/control_plane/` rather than redefining them.
5. Feature modules such as validation and query compose on top of the same loaders and structured result surfaces.

### Invariants and Failure Cases
- `core/control_plane/` remains authoritative for governed machine-readable state.
- `core/python/` remains the only home for Python-specific tooling and package code.
- Unknown or missing lockfile and interpreter metadata are onboarding failures, not silent fallbacks.
- Generated caches, build outputs, and virtual environments must stay ignored and must not leak into governed repository surfaces.

## Affected Surfaces
- `docs/standards/engineering/python_workspace_standard.md`
- `docs/planning/design/features/core_python_workspace_and_harness.md`
- `docs/planning/design/features/python_validator_execution.md`
- `docs/planning/design/features/schema_resolution_and_index_search.md`
- `core/README.md`
- `core/python/`
- `core/control_plane/indexes/repository_paths/repository_path_index.v1.json`

## Design Guardrails
- Keep the package boundaries aligned with actual core behavior, not domain-specific concepts.
- Prefer one package root and one CLI tree.
- Keep onboarding documented in the workspace README and reproducible from the lockfile.
- Keep the first functional scope centered on control-plane loading, validation, query, adapters, evidence, and operator-facing commands.
- Use the future `sync/` surface for deterministic index refresh and contract materialization rather than mixing that behavior into query or validation modules.

## Implementation-Planning Handoff Notes
- First implementation planning should break the work into workspace bootstrap, control-plane loaders, validation service, query service, adapters, and evidence models.
- Implementation planning should include update steps for the repository path index whenever the Python workspace entrypoints change.
- The first code slices should implement deterministic schema resolution and validator execution before adding heavier search or operational layers.

## Dependencies
- `uv` for local environment and lockfile management.
- A pinned Python 3.12 interpreter.
- The authored control-plane artifacts already present under `core/control_plane/`.

## Risks
- Letting ad hoc scripts grow outside the package would recreate the scattered workspace shape this design is trying to avoid.
- Adding too many package modules before their behaviors exist would create empty taxonomy instead of useful code boundaries.
- If the workspace README and lockfile drift apart, onboarding will stop being deterministic.

## Open Questions
- Should the first CLI expose only a `doctor`-style workspace check, or also a thin validation entrypoint once the validator service lands?
- When the query layer matures, should it stay entirely in-process over JSON artifacts, or should a later local SQLite layer become a separate optional backend?

## References
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [python_validator_execution.md](/home/j/WatchTowerPlan/docs/planning/design/features/python_validator_execution.md)
- [schema_resolution_and_index_search.md](/home/j/WatchTowerPlan/docs/planning/design/features/schema_resolution_and_index_search.md)
- [repository_path_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/repository_paths/repository_path_index.v1.json)

## Updated At
- `2026-03-09T18:25:06Z`
