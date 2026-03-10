---
trace_id: "trace.core_python_foundation"
id: "design.implementation.control_plane_loaders_and_schema_store"
title: "Control-Plane Loaders and SchemaStore Implementation Plan"
summary: "Breaks the first executable core/python slice into concrete work for loading governed control-plane artifacts and resolving schemas locally through a reusable SchemaStore."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T02:30:31Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/design/implementation/control_plane_loaders_and_schema_store.md"
  - "core/python/src/watchtower_core/control_plane/"
  - "core/control_plane/registries/schema_catalog/schema_catalog.v1.json"
  - "core/control_plane/registries/validators/validator_registry.v1.json"
aliases:
  - "control plane loader plan"
  - "schemastore plan"
---

# Control-Plane Loaders and SchemaStore Implementation Plan

## Record Metadata
- `Trace ID`: `trace.core_python_foundation`
- `Plan ID`: `design.implementation.control_plane_loaders_and_schema_store`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.core_python_foundation`
- `Linked Decisions`: `decision.core_python_workspace_root`
- `Source Designs`: `design.features.core_python_workspace_and_harness`; `design.features.python_validator_execution`; `design.features.schema_resolution_and_index_search`
- `Linked Acceptance Contracts`: `contract.acceptance.core_python_foundation`
- `Updated At`: `2026-03-10T02:30:31Z`

## Summary
This plan breaks the first executable `core/python` slice into concrete work for loading governed control-plane artifacts and resolving schemas locally through a reusable `SchemaStore`.

## Source Request or Design
- PRD: [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)
- Decision: [core_python_workspace_root.md](/home/j/WatchTowerPlan/docs/planning/decisions/core_python_workspace_root.md)
- This plan is driven by the approved feature designs for the core Python workspace, schema resolution and index search, and validator execution.

## Scope Summary
- Implement reusable control-plane loaders in `core/python/src/watchtower_core/control_plane/`.
- Implement a `SchemaStore` that resolves schema `$id` values through the published schema catalog.
- Load and validate the current schema catalog, validator registry, repository path index, and command index.
- Add tests against the live control-plane artifacts and governed examples.
- Do not implement validator dispatch, repository search, or richer CLI behavior in this slice.

## Assumptions and Constraints
- `core/control_plane/` remains the canonical source of machine-readable authority.
- `core/python/` remains the only Python workspace root.
- Local schema resolution must stay deterministic and fail closed.
- The first implementation should avoid premature abstractions for engines, policies, or storage backends.

## Current-State Context
- `core/control_plane/registries/schema_catalog/schema_catalog.v1.json` now catalogs published schema IDs and canonical local schema paths.
- `core/control_plane/registries/validators/validator_registry.v1.json` declares validation capabilities that later code will need to load.
- `core/control_plane/indexes/repository_paths/repository_path_index.v1.json` and `core/control_plane/indexes/commands/command_index.v1.json` now provide governed lookup surfaces.
- `core/control_plane/contracts/acceptance/`, `core/control_plane/indexes/traceability/`, and `core/control_plane/ledgers/validation_evidence/` now publish the first downstream traceability surfaces the loader layer will eventually need to expose.
- `core/python/src/watchtower_core/control_plane/` now publishes live loaders, typed models, and schema-resolution helpers that later query, sync, and validation slices reuse.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): loaders and query services should stay in modular package code under `core/python/`.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): schema resolution must come from the governed catalog rather than hardcoded filenames.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): loaded artifact schemas should be validated and reused consistently.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): query services should consume the generated repository path index instead of raw repository scans.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): command lookup loaders should consume the governed command index.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): acceptance loading should resolve the governed contract family directly.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): trace queries must consume the unified traceability joins rather than ad hoc link logic.
- [python_validator_execution.md](/home/j/WatchTowerPlan/docs/planning/design/features/python_validator_execution.md): the loader slice should support the validator execution path without duplicating resolution logic.
- [schema_resolution_and_index_search.md](/home/j/WatchTowerPlan/docs/planning/design/features/schema_resolution_and_index_search.md): implementation should follow the approved split between schema resolution and index-backed search.

## Proposed Technical Approach
- Add a small `control_plane` module split into:
  - `paths.py` for repo-root and control-plane path discovery
  - `errors.py` for fail-closed loader and schema-resolution exceptions
  - `models.py` for typed artifact records and indexes
  - `schemas.py` for `SchemaStore`
  - `loader.py` for higher-level artifact loading helpers
- Bootstrap `SchemaStore` from the schema catalog schema and schema catalog artifact directly, then build a local schema registry from all cataloged schemas.
- Validate governed artifacts through their published `$schema` values rather than hidden hardcoded validators.
- Parse loaded artifacts into lightweight dataclasses so later validators and query code can reuse stable typed objects.

## Work Breakdown
1. Add the implementation-plan doc family and this plan.
2. Implement `control_plane/paths.py` and `control_plane/errors.py`.
3. Implement typed models for schema-catalog, validator-registry, repository-path-index, and command-index artifacts.
4. Implement `SchemaStore` bootstrapping, schema resolution, and local schema validation helpers.
5. Implement `ControlPlaneLoader` helpers for the current governed artifacts.
6. Add unit tests for schema resolution, artifact loading, and live example validation.
7. Run the standard Python workspace checks and keep docs or inventories aligned if the surface changes.

## Dependencies
- `jsonschema` and its local referencing support.
- The published schema catalog and artifact schemas already stored under `core/control_plane/`.
- The current `core/python` workspace tooling contract via `uv`.

## Risks
- Bootstrapping schema resolution through the schema catalog can become circular if the initial bootstrap boundary is not kept explicit.
- Overloading the first loader layer with query or validator behavior would make the slice harder to reason about.
- If typed models drift from the artifact schemas, later services will inherit hidden contract mismatches.

## Validation Plan
- Load and validate the live schema catalog.
- Assert that each cataloged schema path exists and its `$id` matches the catalog record.
- Load and validate the live validator registry, repository path index, and command index.
- Validate the published valid and invalid documentation-front-matter examples through `SchemaStore`.
- Run `uv run pytest`, `uv run ruff check .`, and `uv run mypy src`.

## Rollout or Migration Plan
- No migration is needed. This slice adds new Python capabilities without changing the authored control-plane artifact formats.
- Later slices for validator execution and query should depend on this loader layer rather than re-reading JSON directly.

## Open Questions
- Whether the first public API should expose generic `load_artifact` entrypoints only, or also convenience methods for common artifact families.
- Whether future artifact models should remain dataclass-based or move to a stricter runtime model layer once more executable surfaces exist.

## References
- [core_python_workspace_and_harness.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_python_workspace_and_harness.md)
- [python_validator_execution.md](/home/j/WatchTowerPlan/docs/planning/design/features/python_validator_execution.md)
- [schema_resolution_and_index_search.md](/home/j/WatchTowerPlan/docs/planning/design/features/schema_resolution_and_index_search.md)
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)

## Updated At
- `2026-03-10T02:30:31Z`
