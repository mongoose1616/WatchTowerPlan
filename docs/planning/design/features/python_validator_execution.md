---
trace_id: "trace.core_python_foundation"
id: "design.features.python_validator_execution"
title: "Python Validator Execution Design"
summary: "Defines the feature-level technical design for a Python validation layer that reads the authored validator registry from core/control_plane and executes validators deterministically against governed artifacts."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T07:05:24Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/design/features/python_validator_execution.md"
  - "core/python/src/watchtower_core/validation/"
  - "core/control_plane/registries/validators/validator_registry.v1.json"
  - "core/control_plane/ledgers/validation_evidence/"
aliases:
  - "validator execution design"
  - "python validation design"
---

# Python Validator Execution Design

## Record Metadata
- `Trace ID`: `trace.core_python_foundation`
- `Design ID`: `design.features.python_validator_execution`
- `Design Status`: `active`
- `Linked PRDs`: `prd.core_python_foundation`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `design.implementation.control_plane_loaders_and_schema_store`
- `Updated At`: `2026-03-09T07:05:24Z`

## Summary
This document defines the feature-level technical design for a Python validation layer that reads the authored validator registry from `core/control_plane/` and executes validators deterministically against governed artifacts.

## Source Request
- User request to make the validator work a `docs/planning/design/features` artifact after establishing the first control-plane validator registry.
- Downstream planning authority is captured in [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md).

## Scope and Feature Boundary
- Covers the Python-side execution model for registry-driven validation.
- Covers how validator definitions in `core/control_plane/registries/validators/validator_registry.v1.json` map to Python runners and structured results.
- Covers the first wave of schema-backed validation for governed documentation front matter and JSON control-plane artifacts.
- Covers the first durable evidence-write path that records governed validation outcomes back into the governed control plane.
- Does not define the full intake-contract family.
- Does not define validation policy documents.
- Does not implement the code in this document.

## Current-State Context
- `core/control_plane/registries/validators/validator_registry.v1.json` now defines validator identities, engines, target artifact kinds, and schema dependencies.
- `core/control_plane/schemas/interfaces/documentation/` already publishes governed front matter validation interfaces for reference, standard, workflow, PRD, and decision-record documents.
- `core/control_plane/contracts/acceptance/`, `core/control_plane/ledgers/validation_evidence/`, and `core/control_plane/indexes/traceability/` now provide the downstream contract, evidence, and join surfaces the validator layer now writes to in its first durable evidence path.
- `core/python/src/watchtower_core/validation/` is the package boundary for validator execution and now provides registry-backed front-matter and JSON artifact validation services.
- The repository has standards for schemas, naming and IDs, lifecycle status, format selection, and front matter, but it does not yet have a Python execution path that turns those artifacts into actual validation behavior.

## Foundations References Applied
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md): keep core local-first, deterministic, schema-first, and fail-closed.
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md): keep core as the shared runtime and governance substrate rather than the user-facing product.
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md): favor Python for helper and harness layers and JSON Schema for machine-validated contracts.
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md): keep one canonical source for machine-facing facts and avoid parallel truth in code.

## Internal Standards and Canonical References Applied
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md)
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md)
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md)
- [validator_registry.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/validators/validator_registry.v1.json)
- [validator_registry.v1.schema.json](/home/j/WatchTowerPlan/core/control_plane/schemas/artifacts/validator_registry.v1.schema.json)

## Design Goals and Constraints
- Keep validator identity and selection declarative in the control plane rather than hardcoded in Python.
- Make validation fail closed when the registry, the schema references, or the requested validator selection is invalid.
- Keep the first implementation small and deterministic.
- Separate lifecycle status from validation results. The result model must not overload artifact lifecycle `status`.
- Allow future intake contracts and validation policies to select validator IDs without changing the execution core.

## Options Considered
### Option 1
- Hardcode validator definitions directly in Python modules.
- Strengths: smallest first code change and minimal loader logic.
- Tradeoffs or reasons not chosen: duplicates the control-plane registry, weakens declarative selection, and makes policies and contracts refer to code structure instead of stable validator IDs.

### Option 2
- Use the validator registry only for discovery but select validators primarily by artifact kind in Python.
- Strengths: simple path from artifact parsing to runner dispatch.
- Tradeoffs or reasons not chosen: artifact-kind-only selection becomes too implicit once multiple validators can apply to the same artifact family.

### Option 3
- Resolve and execute validators by registry ID, with future contracts naming required validator IDs declaratively.
- Strengths: keeps control-plane identity stable, composes cleanly with future contracts and policy, and keeps Python focused on execution rather than authority.
- Tradeoffs or reasons not chosen: requires a little more plumbing up front around registry loading and explicit selection.

## Recommended Design
### Architecture
- Add a control-plane loader that reads and validates the authored validator registry artifact.
- Add a validator service in `core/python/src/watchtower_core/validation/` that resolves validator IDs to registry records.
- Add runner modules keyed by `engine`, starting with a JSON Schema runner.
- Add a parsing adapter layer for artifact families that are not validated directly as raw files, such as Markdown front matter.
- Add a structured result model that records validator ID, target, engine, pass or fail outcome, and issue details without using lifecycle status terminology.

### Data and Interface Impacts
- The validator registry remains the canonical source of validator identity, applicability, and schema dependencies.
- Python code consumes registry records and published schemas but does not redefine their identifiers.
- Documentation front matter validation becomes the first implemented artifact family because its schemas and examples already exist.
- Future intake contracts should name validator IDs explicitly rather than embedding runner logic or path heuristics.

### Execution Flow
1. A caller requests validation by validator ID directly or by a future intake contract that resolves to validator IDs.
2. Python loads and validates the authored validator registry artifact.
3. Python resolves each requested validator ID to an active registry record.
4. Python dispatches to the appropriate runner based on `engine`.
5. For documentation front matter, Python extracts and parses the YAML front matter block before schema validation.
6. The runner validates the target payload against the referenced schema IDs and returns structured issues.
7. The service aggregates the validator results and returns a deterministic validation report.

### Invariants and Failure Cases
- Unknown validator IDs are hard failures.
- Unknown or unsupported `engine` values are hard failures.
- Schema-backed validators must not run without declared `schema_ids`.
- Registry records marked `deprecated` should not be selected by default once that behavior is implemented.
- Parsing failures for front matter are validation failures for the target artifact, not silent skips.
- The validation report should distinguish execution errors from contract failures, but neither should reuse lifecycle `status`.

## Affected Surfaces
- `core/python/src/watchtower_core/control_plane/` for registry and schema loading helpers.
- `core/python/src/watchtower_core/validation/` for the validator service, runners, and result models.
- `core/python/src/watchtower_core/models/` if typed models are introduced for registry entries and result objects.
- `core/python/tests/unit/` for loader, dispatch, and runner tests.
- `core/python/tests/integration/` for validation runs against authored control-plane artifacts and example documents.
- Future `core/control_plane/contracts/intake/` artifacts that choose validator IDs declaratively.

## Design Guardrails
- Control-plane artifacts remain the canonical source of validator identity and applicability.
- Python modules may implement runners, but they must not become the hidden source of truth for validator definitions.
- Keep the first wave limited to JSON Schema-backed validators and documentation front matter.
- Avoid introducing SQLite, NDJSON, or policy engines until the validation flow has a concrete need for them.

## Implementation-Planning Handoff Notes
- First implementation planning should break the work into registry loading, runner dispatch, front matter extraction, JSON Schema execution, and result modeling.
- Implementation planning should also account for test fixtures that exercise both valid and invalid front matter examples.
- Intake contracts and validation policy should be planned as later features that consume validator IDs rather than prerequisites for the first execution path.

## Dependencies
- `jsonschema` for Draft 2020-12 validation.
- A YAML parser for front matter extraction and parsing.
- The authored validator registry and documentation interface schemas already present under `core/control_plane/`.

## Risks
- Overgeneralizing the runner architecture too early could create unnecessary abstraction before there is more than one practical engine.
- Coupling parsing and validation too tightly could make future artifact families harder to add cleanly.
- Path matching in `applies_to` will stay ambiguous unless future contracts or a narrower selection rule become authoritative.

## Open Questions
- Should the first public Python API accept only validator IDs, or also support a convenience path that resolves validators from artifact kind and target path?
- Should the result model expose warnings separately from failures in the first version, or stay pass or fail only until policies are introduced?
- Where should parsed front matter extraction live: inside the validation package or as a reusable control-plane adapter?

## References
- [feature_design_planning.md](/home/j/WatchTowerPlan/workflows/modules/feature_design_planning.md)
- [validator_registry.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/validators/validator_registry.v1.json)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)

## Updated At
- `2026-03-09T07:05:24Z`
