---
trace_id: trace.control_plane_example_validation_hardening
id: decision.control_plane_example_validation_hardening_direction
title: Control Plane Example Validation Hardening Direction Decision
summary: Records the initial direction decision for Control Plane Example Validation
  Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T14:40:00Z'
audience: shared
authority: supporting
applies_to:
- core/control_plane/examples/valid/indexes/
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/
- docs/commands/core_python/watchtower_core_validate_all.md
- docs/standards/validations/repository_validation_standard.md
---

# Control Plane Example Validation Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.control_plane_example_validation_hardening`
- `Decision ID`: `decision.control_plane_example_validation_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.control_plane_example_validation_hardening`
- `Linked Designs`: `design.features.control_plane_example_validation_hardening`
- `Linked Implementation Plans`: `design.implementation.control_plane_example_validation_hardening`
- `Updated At`: `2026-03-12T14:40:00Z`

## Summary
Records the initial direction decision for Control Plane Example Validation Hardening.

## Decision Statement
Repair the invalid valid examples, include the governed valid example corpus in aggregate artifact validation through explicit schema resolution, and add exhaustive example plus canonicality regressions.

## Trigger or Source Request
- A comprehensive project review found two canonical valid examples that fail their live schemas and a surrounding validation gap that let the drift persist.

## Current Context and Constraints
- Aggregate artifact validation currently focuses on live governed JSON artifacts and a narrow subset of example surfaces.
- Documentation front-matter examples do not carry `$schema`, so valid-example coverage needs an explicit deterministic schema-resolution rule.

## Applied References and Implications
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): broad repository validation should cover the governed artifact surfaces relied on during closeout.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): canonical valid and invalid examples are part of the schema contract and must remain aligned.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): fix the reproduced drift at the narrowest coherent boundary and keep the system fail closed.

## Affected Surfaces
- core/control_plane/examples/valid/indexes/
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/
- docs/commands/core_python/watchtower_core_validate_all.md
- docs/standards/validations/repository_validation_standard.md

## Options Considered
### Option 1
- Fix only the broken valid examples and leave aggregate validation and integration coverage unchanged.
- Strength: minimal diff.
- Tradeoff: leaves the baseline blind to future valid-example drift and does not fix the broken canonicality audit.

### Option 2
- Add explicit valid-example coverage to aggregate artifact validation, repair the broken examples, and add exhaustive valid/invalid example plus recursive canonicality tests.
- Strength: closes the live drift and the coverage gap together.
- Tradeoff: requires one explicit schema-resolution helper for documentation examples.

### Option 3
- Expand the validator registry with dedicated example validators for every schema-backed family.
- Strength: keeps everything registry-addressable.
- Tradeoff: creates noisy validator duplication and still needs separate negative-example handling.

## Chosen Outcome
Option 2 is accepted.

## Rationale and Tradeoffs
- The review found a live example drift defect, so fixing only the examples would leave the root validation gap in place.
- Explicit schema resolution for governed examples is smaller and more maintainable than creating duplicate validator-registry entries per example family.

## Consequences and Follow-Up Impacts
- Aggregate artifact validation and its command docs will expand to include canonical valid examples.
- Integration coverage will grow to validate the full example corpus and the corrected markdown canonicality audit.

## Risks, Dependencies, and Assumptions
- New documentation example families will need their schema mapping added intentionally.
- Invalid examples must remain expected failures in tests rather than being folded into the passing aggregate validator.

## References
- docs/planning/prds/control_plane_example_validation_hardening.md
- docs/planning/design/features/control_plane_example_validation_hardening.md
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/test_control_plane_artifacts.py
