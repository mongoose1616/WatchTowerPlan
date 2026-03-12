---
trace_id: trace.control_plane_example_validation_hardening
id: design.features.control_plane_example_validation_hardening
title: Control Plane Example Validation Hardening Feature Design
summary: Defines the technical design boundary for Control Plane Example Validation
  Hardening.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-12T14:40:00Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/examples/valid/indexes/
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/
- docs/commands/core_python/watchtower_core_validate_all.md
- docs/standards/validations/repository_validation_standard.md
---

# Control Plane Example Validation Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.control_plane_example_validation_hardening`
- `Design ID`: `design.features.control_plane_example_validation_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.control_plane_example_validation_hardening`
- `Linked Decisions`: `decision.control_plane_example_validation_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.control_plane_example_validation_hardening`
- `Updated At`: `2026-03-12T14:40:00Z`

## Summary
Defines the technical design boundary for Control Plane Example Validation Hardening.

## Source Request
- A comprehensive project review found that the canonical valid foundation-index and traceability-index examples fail their schemas.
- The same review confirmed that aggregate validation omits the valid example corpus and that the governed markdown `applies_to` canonicality audit is partially dead and non-recursive.

## Scope and Feature Boundary
- Cover the governed control-plane valid example corpus, the aggregate validation path that should catch valid-example drift, and the integration audits that prove canonicality and invalid-example behavior.
- Do not redesign artifact schemas or broaden validation to pack-owned artifacts outside `core/control_plane/examples/`.

## Current-State Context
- `watchtower-core validate all` currently passes even while two canonical valid examples are schema-invalid because the artifact family only walks live governed artifact targets and a small subset of interface examples.
- The integration audit intended to enforce governed markdown `applies_to` canonicality has unreachable loop logic and uses non-recursive `glob("*.md")`, so most nested standards docs are not actually checked there.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): validation should keep the machine-readable substrate trustworthy and fail closed at the narrowest coherent boundary.

## Internal Standards and Canonical References Applied
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): broad repository validation should cover governed artifacts through the baseline validation flow.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): canonical valid and invalid examples are part of the governed schema boundary and must stay aligned.
- [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md): the foundation-index family operationalizes valid and invalid examples as companion surfaces.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): the traceability-index family likewise depends on valid and invalid examples remaining authoritative.

## Design Goals and Constraints
- Catch canonical valid-example drift in the aggregate validation baseline rather than relying only on sparse hand-authored example tests.
- Preserve fail-closed behavior by resolving each example against an explicit schema ID; do not introduce permissive validation fallback for arbitrary repo-local JSON.
- Keep invalid examples intentionally failing and prove that behavior in automated tests.

## Options Considered
### Option 1
- Fix only the two invalid valid examples and leave aggregate validation behavior unchanged.
- Strength: smallest implementation change.
- Tradeoff: baseline validation remains blind to future valid-example drift, and the current review finding could recur quietly.

### Option 2
- Repair the invalid examples, teach aggregate artifact validation to include the valid example corpus through explicit schema resolution, and add exhaustive example plus canonicality regressions.
- Strength: fixes the live drift and the coverage gap in one coherent slice.
- Tradeoff: requires a small amount of explicit schema-resolution logic for documentation front-matter examples that do not carry `$schema`.

### Option 3
- Add one validator-registry entry per example family and rely entirely on registry auto-selection.
- Strength: keeps aggregate validation purely registry-driven.
- Tradeoff: adds noisy per-example-family validator management and still needs a separate solution for invalid-example expectations.

## Recommended Design
### Architecture
- Add one repo-local example-artifact helper that enumerates the governed example corpus and resolves the correct schema ID for each valid example.
- Extend the aggregate artifact validation family to run those valid examples alongside the live governed JSON artifacts.

### Data and Interface Impacts
- The valid foundation-index and traceability-index examples change to satisfy their live schemas.
- `watchtower-core validate all` changes behavior by adding valid example artifacts to its artifact-family target set.
- Integration tests add exhaustive valid-example success, invalid-example failure, and recursive markdown canonicality coverage.

### Execution Flow
1. Enumerate the governed valid example corpus and resolve explicit schema IDs, including documentation front-matter examples that need deterministic path-based mapping.
2. Run aggregate artifact validation against those valid examples in the same artifact family as the live governed JSON surfaces.
3. Prove the corpus with exhaustive integration tests and repair the currently invalid valid examples.

### Invariants and Failure Cases
- Invalid examples must remain expected failures in tests rather than being added to aggregate validation as passing targets.
- If a governed example cannot resolve to one explicit schema ID, the validation flow must fail rather than silently skipping or guessing.

## Affected Surfaces
- core/control_plane/examples/valid/indexes/
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/
- docs/commands/core_python/watchtower_core_validate_all.md
- docs/standards/validations/repository_validation_standard.md

## Design Guardrails
- Keep example-schema resolution bounded to the governed control-plane example corpus.
- Do not weaken schema requirements to make the broken examples pass; fix the examples instead.

## Risks
- Example-schema mapping could drift if new documentation example families are added without extending the helper and tests.
- Aggregate validation target growth increases output volume, so the follow-up review should confirm the added coverage remains bounded and useful.

## References
- docs/planning/prds/control_plane_example_validation_hardening.md
- core/control_plane/examples/valid/indexes/foundation_index.v1.example.json
- core/control_plane/examples/valid/indexes/traceability_index.v1.example.json
- core/python/src/watchtower_core/repo_ops/validation/all.py
- docs/standards/data_contracts/schema_standard.md
