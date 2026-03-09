---
trace_id: "trace.core_python_foundation"
id: "design.features.schema_resolution_and_index_search"
title: "Schema Resolution and Index Search Design"
summary: "Defines the feature-level technical design for deterministic local schema resolution and index-backed repository search in the Python helper layer."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T07:05:24Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/design/features/schema_resolution_and_index_search.md"
  - "core/control_plane/registries/schema_catalog/schema_catalog.v1.json"
  - "core/control_plane/indexes/repository_paths/repository_path_index.v1.json"
  - "core/python/src/watchtower_core/query/"
aliases:
  - "schema resolution design"
  - "index search design"
---

# Schema Resolution and Index Search Design

## Record Metadata
- `Trace ID`: `trace.core_python_foundation`
- `Design ID`: `design.features.schema_resolution_and_index_search`
- `Design Status`: `active`
- `Linked PRDs`: `prd.core_python_foundation`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `design.implementation.control_plane_loaders_and_schema_store`
- `Updated At`: `2026-03-09T07:05:24Z`

## Summary
This document defines the feature-level technical design for deterministic local schema resolution and index-backed repository search in the future Python helper layer.

## Source Request
- User request to define the best method for loading schemas and searching indexes as the repository file count grows.
- Downstream planning authority is captured in [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md).

## Scope and Feature Boundary
- Covers a schema catalog-driven resolution path for published schema `$id` values.
- Covers an index-backed repository search path for narrowing candidate files and directories before content loading.
- Covers how these two capabilities compose without collapsing into one undifferentiated search feature.
- Does not implement the Python code in this document.
- Does not add vector search, embeddings, or a database-backed full-text layer.
- Does not define validation policy or intake contract selection.

## Current-State Context
- `core/control_plane/indexes/repository_paths/repository_path_index.v1.json` already defines a generated repository path index for entrypoint retrieval.
- `core/control_plane/registries/validators/validator_registry.v1.json` already declares validation capabilities by stable validator ID.
- `core/control_plane/registries/schema_catalog/` exists as a directory boundary but does not yet publish a governed schema catalog artifact.
- Current ad hoc schema validation requires manual local schema-store wiring because published schema `$id` values are URNs rather than file paths.
- `core/python/src/watchtower_core/` is the consolidated package root and currently contains scaffold-only modules.

## Foundations References Applied
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md): keep core deterministic, local-first, and fail-closed rather than inference-heavy.
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md): keep core as the shared machine substrate rather than a UI-first search product.
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md): favor simple local Python and structured machine-readable contracts before adding heavier infrastructure.
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md): keep one canonical machine-readable authority per concept and avoid parallel truth in code.

## Internal Standards and Canonical References Applied
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [python_validator_execution.md](/home/j/WatchTowerPlan/docs/planning/design/features/python_validator_execution.md)
- [repository_path_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/repository_paths/repository_path_index.v1.json)

## Design Goals and Constraints
- Resolve published schemas deterministically by stable schema `$id`, not by filesystem scanning or text search.
- Use generated indexes to narrow repository search before any content read path expands.
- Keep schema authority separate from path retrieval so each surface stays small and understandable.
- Fail closed when a requested schema ID, index artifact, or filter is invalid.
- Keep the first implementation local, lightweight, and reviewable.

## Options Considered
### Option 1
- Search the repository tree directly whenever schema or path lookup is needed.
- Strengths: smallest initial code change and no additional control-plane artifact.
- Tradeoffs or reasons not chosen: repeated tree walks, hidden heuristics, poor determinism, and unnecessary coupling between lookup behavior and current filesystem layout.

### Option 2
- Use a schema catalog registry for schema resolution and the repository path index for structured search.
- Strengths: deterministic schema resolution, clear control-plane authority, and small composable services in Python.
- Tradeoffs or reasons not chosen: requires one new registry artifact family and a modest amount of loader code.

### Option 3
- Add a local SQLite or FTS-backed search layer immediately and use it for both schema and path lookup.
- Strengths: broader future query surface and stronger text search if the corpus grows substantially.
- Tradeoffs or reasons not chosen: heavier than current needs, less transparent for review, and premature before deterministic registry- and index-backed lookup is in place.

## Recommended Design
### Architecture
- Add a schema catalog loader that reads and validates the authored schema catalog registry.
- Add a `SchemaStore` service that resolves a requested schema `$id` to its canonical local file and loads the schema document.
- Add a `RepositoryIndexSearch` service that reads the repository path index and filters entries by path prefix, surface kind, tags, aliases, or free-text query over the indexed fields.
- Keep these as separate services composed by higher-level workflows rather than one blended search abstraction.
- Keep `rg` or direct filesystem scans as explicit fallback behavior, not as the default lookup path.

### Data and Interface Impacts
- Add the schema catalog registry artifact family under `core/control_plane/registries/schema_catalog/`.
- Reuse the existing repository path index artifact family under `core/control_plane/indexes/repository_paths/`.
- Future Python code in `core/python/src/watchtower_core/control_plane/` should expose schema-catalog and path-index loaders.
- Future Python code in `core/python/src/watchtower_core/validation/` should depend on `SchemaStore` for schema-backed validation rather than manual resolver wiring.

### Execution Flow
1. A caller requests a published schema by `$id` or requests repository candidates by query and structured filters.
2. Python loads and validates the schema catalog or repository path index artifact.
3. For schema resolution, `SchemaStore` resolves the requested `$id` to one active catalog record and loads the schema from `canonical_path`.
4. For path search, `RepositoryIndexSearch` filters and ranks the indexed entries without scanning the whole repository tree.
5. Higher-level services load only the small candidate set returned by the search layer or the single schema resolved by the schema store.
6. If a requested target is outside the indexed or cataloged surfaces, the caller must opt into explicit fallback behavior rather than silently broadening the search boundary.

### Invariants and Failure Cases
- Unknown schema `$id` values are hard failures.
- A schema catalog record whose `canonical_path` does not exist or whose schema file publishes a mismatched `$id` is a hard failure.
- Repository path indexes are retrieval aids, not authority surfaces. They must not redefine path authority.
- Search services must not silently scan the full tree when the path index is missing or stale.
- Fallback scanning should be explicit and visible in the caller contract if it is supported later.

## Affected Surfaces
- `docs/standards/data_contracts/schema_catalog_standard.md`
- `docs/planning/design/features/schema_resolution_and_index_search.md`
- `core/control_plane/schemas/artifacts/` for the schema catalog artifact schema
- `core/control_plane/registries/schema_catalog/` for the live schema catalog artifact
- `core/control_plane/examples/valid/registries/` and `core/control_plane/examples/invalid/registries/`
- Future `core/python/src/watchtower_core/control_plane/` resolver and loader modules
- Future `core/python/tests/unit/` and `core/python/tests/integration/` coverage for schema resolution and index search

## Design Guardrails
- Keep schema resolution authoritative and deterministic through the schema catalog registry.
- Keep repository search index-backed and retrieval-oriented rather than turning it into a second source of truth.
- Do not add a database or vector search layer until structured control-plane lookup is clearly insufficient.
- Keep fallback full-tree scans explicit so the default behavior remains cheap and reviewable.

## Implementation-Planning Handoff Notes
- First implementation planning should separate schema-catalog loading, schema-store resolution, and repository-path-index search into distinct tasks.
- Implementation planning should include tests for schema-ID mismatch, missing canonical paths, and filtered path-index queries.
- The first implementation should use the existing repository path index as-is rather than expanding directly into a full-tree catalog.

## Dependencies
- The published schema catalog artifact family.
- The existing repository path index artifact family.
- Local JSON Schema validation support in Python.

## Risks
- If the repository path index remains too narrow, callers may overuse fallback scans and undermine the design boundary.
- If schema aliases become too loose, schema resolution may become ambiguous instead of deterministic.
- Overgeneralizing the path-search API too early could add complexity before more than one concrete caller exists.

## Open Questions
- Should the first path-search API support simple score-based ranking, or should it return deterministic filtered results in catalog order until a stronger use case appears?
- Should alias matching be exact-only in the first version, or should it allow normalized token matching across aliases and summaries?

## References
- [python_validator_execution.md](/home/j/WatchTowerPlan/docs/planning/design/features/python_validator_execution.md)
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [repository_path_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/repository_paths/repository_path_index.v1.json)

## Updated At
- `2026-03-09T07:05:24Z`
