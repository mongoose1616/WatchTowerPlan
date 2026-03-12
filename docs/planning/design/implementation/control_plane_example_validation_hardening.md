---
trace_id: trace.control_plane_example_validation_hardening
id: design.implementation.control_plane_example_validation_hardening
title: Control Plane Example Validation Hardening Implementation Plan
summary: Breaks Control Plane Example Validation Hardening into a bounded implementation
  slice.
type: implementation_plan
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

# Control Plane Example Validation Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.control_plane_example_validation_hardening`
- `Plan ID`: `design.implementation.control_plane_example_validation_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.control_plane_example_validation_hardening`
- `Linked Decisions`: `decision.control_plane_example_validation_hardening_direction`
- `Source Designs`: `design.features.control_plane_example_validation_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.control_plane_example_validation_hardening`
- `Updated At`: `2026-03-12T14:40:00Z`

## Summary
Breaks Control Plane Example Validation Hardening into a bounded implementation slice.

## Source Request or Design
- design.features.control_plane_example_validation_hardening

## Scope Summary
- Repair the canonical valid foundation-index and traceability-index examples and harden validation coverage over governed examples and markdown `applies_to` audits.
- Leave schema redesign, new artifact families, and pack-external validation behavior out of scope.

## Assumptions and Constraints
- The repository baseline should stay deterministic and fail closed even as artifact-family coverage grows.
- Invalid examples should remain intentionally failing surfaces proven through tests rather than aggregate passing targets.

## Internal Standards and Canonical References Applied
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): the broad validation tier should catch governed valid-example drift.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): canonical valid and invalid examples remain part of the schema-backed contract boundary.
- [watchtower_core_validate_all.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_all.md): command docs must stay aligned with the aggregate validator's real coverage.

## Proposed Technical Approach
- Add a repo-local helper for enumerating control-plane examples and resolving their schema IDs, then wire it into the aggregate artifact validation flow for valid examples only.
- Update the two invalid valid examples, add exhaustive example and canonicality regressions, and refresh the command and validation-standard docs to match the new baseline.

## Work Breakdown
1. Author the planning documents, accepted decision, and bounded execution tasks for the validation-hardening slice.
2. Repair the valid foundation-index and traceability-index examples and add example-schema resolution support to aggregate validation.
3. Add exhaustive valid/invalid example regressions, repair the recursive markdown `applies_to` audit, and align command and validation-standard docs.
4. Run sync, acceptance validation, full repository validation, Python workspace checks, and a follow-up review pass before closeout.

## Risks
- Example-schema inference for documentation front-matter examples must remain explicit and easily extensible.
- The aggregate validator should not duplicate invalid-example failure checks that are better expressed as negative tests.

## Validation Plan
- Run targeted validation and regression tests for aggregate validation, control-plane artifact integration coverage, and schema-store example handling.
- Run `watchtower-core sync all --write --format json`, `watchtower-core validate acceptance --trace-id trace.control_plane_example_validation_hardening --format json`, final `watchtower-core validate all --format json`, `pytest -q`, `python -m mypy src/watchtower_core`, and `ruff check .`.

## References
- docs/planning/design/features/control_plane_example_validation_hardening.md
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_validate_all.md
