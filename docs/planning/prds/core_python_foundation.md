---
trace_id: "trace.core_python_foundation"
id: "prd.core_python_foundation"
title: "Core Python Foundation PRD"
summary: "Defines the planning intent for the core Python workspace, control-plane loaders, validation, and query foundations."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T03:57:14Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/"
  - "core/control_plane/"
  - "docs/planning/design/"
aliases:
  - "core python prd"
  - "core runtime foundation"
---

# Core Python Foundation PRD

## Record Metadata
- `Trace ID`: `trace.core_python_foundation`
- `PRD ID`: `prd.core_python_foundation`
- `Status`: `active`
- `Linked Decisions`: `decision.core_python_workspace_root`
- `Linked Designs`: `design.features.core_python_workspace_and_harness`; `design.features.python_validator_execution`; `design.features.schema_resolution_and_index_search`
- `Linked Implementation Plans`: `design.implementation.control_plane_loaders_and_schema_store`
- `Linked Acceptance Contracts`: `contract.acceptance.core_python_foundation`
- `Linked Validation Evidence`: `evidence.core_python_foundation.traceability_baseline`
- `Updated At`: `2026-03-10T03:57:14Z`

## Summary
This PRD defines the product and planning intent for the core Python helper and harness foundation that operates over the versioned control plane.

## Problem Statement
The repository now has a growing control-plane surface, but the executable Python layer that should load schemas, query indexes, run validators, and later emit evidence is still only partially defined. Without a stable PRD, the core runtime and its planning artifacts risk drifting from one another.

## Goals
- Establish one governed Python workspace under `core/python/`.
- Make schema loading, control-plane lookup, validation, and query first-class core capabilities.
- Make deterministic index refresh and structured payload validation available to workflow-driven data entry.
- Keep the control plane authoritative and the Python layer deterministic and local-first.
- Make future traceability and validation evidence possible without redesigning the planning surfaces again.

## Non-Goals
- Building domain-pack-specific logic in core.
- Adding vector search, network services, or heavy infrastructure in the first core runtime slices.
- Treating mutable runtime state as versioned control-plane authority.

## Target Users or Actors
- Repository maintainers shaping core architecture and governance.
- Engineers implementing the Python helper and harness layer.
- LLM or agent execution flows that need deterministic local loading, validation, and query behavior.

## Key Scenarios
- An engineer needs to resolve a governed schema by `$id` and validate an artifact without ad hoc file scanning.
- An agent needs a compact machine-readable path to find commands, design docs, PRDs, and decisions.
- A workflow needs Python to validate a structured payload and materialize a reviewed index or contract update consistently.
- A validator needs to map from a stable validator ID to a schema-backed validation step and produce durable evidence.

## Requirements
- `req.core_python_foundation.001`: Core must keep `core/control_plane/` as the canonical versioned machine-readable authority surface.
- `req.core_python_foundation.002`: Core must keep all Python-specific code, tooling, and onboarding surfaces under `core/python/`.
- `req.core_python_foundation.003`: Core must provide deterministic schema resolution through the governed schema catalog rather than broad filesystem search.
- `req.core_python_foundation.004`: Core must provide index-backed query surfaces for high-signal repository lookup.
- `req.core_python_foundation.005`: Core must support validator execution through stable validator IDs defined in the validator registry.
- `req.core_python_foundation.006`: Core must preserve end-to-end traceability across PRD, decision, design, implementation plan, and validation evidence surfaces.

## Acceptance Criteria
- `ac.core_python_foundation.001`: The repository contains one canonical Python workspace under `core/python/` and one canonical authored control-plane root under `core/control_plane/`.
- `ac.core_python_foundation.002`: Published schema, validator, command, PRD, decision, design, acceptance, evidence, and traceability artifacts exist and validate against their governed schemas.
- `ac.core_python_foundation.003`: At least one real `PRD -> decision -> design -> implementation plan -> validation evidence` chain exists for the core Python foundation initiative.
- `ac.core_python_foundation.004`: The first Python implementation slice can load and validate the schema catalog, validator registry, command index, repository path index, PRD index, decision index, and traceability index through governed control-plane artifacts.

## Success Metrics
- Core planning artifacts can be joined by one shared `trace_id` without parsing prose heuristically.
- A future Python query service can answer traceability and lookup questions from governed indexes alone.
- Engineers can identify the active PRD, decision, designs, implementation plan, and validation evidence for the core Python foundation in one review pass.

## Risks and Dependencies
- The current core runtime is implemented and validated, but future extraction into `WatchTower` still needs an explicit modularization and export slice.
- If new planning docs are added without updating indexes and trackers, traceability will drift again.
- Validation evidence standards and traceability indexes must stay aligned with the validator registry and planning indexes.

## Open Questions
- Should future Python tooling regenerate acceptance contracts and traceability indexes automatically, or keep them as reviewed artifacts refreshed through explicit commands?
- Should the next bounded follow-up split reusable runtime layers from `WatchTowerPlan` repo-operations so the core can be consumed directly by `WatchTower`?

## Foundations References Applied
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): core should provide routing, validation, evidence capture, and reusable closeout behavior.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): core should remain deterministic, schema-first, and traceable.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): important planning and validation surfaces should exist in both human-readable and machine-usable forms.

## References
- [core_python_workspace_and_harness.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_python_workspace_and_harness.md)
- [python_validator_execution.md](/home/j/WatchTowerPlan/docs/planning/design/features/python_validator_execution.md)
- [schema_resolution_and_index_search.md](/home/j/WatchTowerPlan/docs/planning/design/features/schema_resolution_and_index_search.md)
- [control_plane_loaders_and_schema_store.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/control_plane_loaders_and_schema_store.md)
- [core_python_foundation_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json)
- [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json)
