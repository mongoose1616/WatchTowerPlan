---
trace_id: trace.control_plane_example_validation_hardening
id: prd.control_plane_example_validation_hardening
title: Control Plane Example Validation Hardening PRD
summary: Fix invalid canonical example artifacts and harden repository validation
  coverage over the governed control-plane example corpus and applies_to canonicality
  audits.
type: prd
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

# Control Plane Example Validation Hardening PRD

## Record Metadata
- `Trace ID`: `trace.control_plane_example_validation_hardening`
- `PRD ID`: `prd.control_plane_example_validation_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.control_plane_example_validation_hardening_direction`
- `Linked Designs`: `design.features.control_plane_example_validation_hardening`
- `Linked Implementation Plans`: `design.implementation.control_plane_example_validation_hardening`
- `Updated At`: `2026-03-12T14:40:00Z`

## Summary
Fix invalid canonical example artifacts and harden repository validation coverage over the governed control-plane example corpus and applies_to canonicality audits.

## Problem Statement
The comprehensive project review found two live control-plane drift defects that the baseline validation flow was not surfacing clearly enough. The canonical valid foundation-index example and canonical valid traceability-index example no longer satisfy their schemas, and the surrounding validation coverage is too weak: aggregate artifact validation does not currently exercise the valid example corpus, while the integration audit for governed markdown `applies_to` canonicality contains unreachable logic and scans only top-level files. As a result, canonical examples and path-canonicality regressions can drift farther than intended before the repository baseline catches them.

## Goals
- Repair the invalid canonical valid examples so they again prove their schemas correctly.
- Extend the aggregate validation baseline to cover the governed valid example corpus under `core/control_plane/examples/valid/`.
- Add exhaustive regression coverage for valid and invalid examples and restore the markdown `applies_to` canonicality audit to real recursive coverage.

## Non-Goals
- Redesign the foundation-index or traceability-index schemas.
- Convert intentionally invalid examples into passing artifacts.
- Expand the validation baseline to external pack-owned artifacts outside the governed control-plane example corpus.

## Requirements
- `req.control_plane_example_validation_hardening.001`: The canonical valid foundation-index and traceability-index examples must satisfy their current schemas without weakening the schemas themselves.
- `req.control_plane_example_validation_hardening.002`: `watchtower-core validate all` must include the governed valid control-plane example corpus in its artifact family so broad repository validation catches valid-example drift.
- `req.control_plane_example_validation_hardening.003`: Repository regression coverage must validate every governed valid example as passing, every governed invalid example as failing, and the markdown `applies_to` canonicality audit must scan nested governed markdown surfaces without dead code.

## Acceptance Criteria
- `ac.control_plane_example_validation_hardening.001`: The trace carries a fully authored planning chain, accepted direction decision, acceptance contract, evidence artifact, and bounded closed task set for this validation-hardening slice.
- `ac.control_plane_example_validation_hardening.002`: The canonical valid foundation-index and traceability-index examples pass schema validation, and `watchtower-core validate all` covers the valid control-plane example corpus in its artifact family.
- `ac.control_plane_example_validation_hardening.003`: Exhaustive integration and unit regressions prove all valid examples pass, all invalid examples fail, and governed markdown `applies_to` canonicality is checked recursively.
- `ac.control_plane_example_validation_hardening.004`: Final sync, validation, Python workspace checks, and a follow-up review pass complete without additional issues in the reviewed control-plane validation area.

## Risks and Dependencies
- Example-schema resolution for documentation front-matter examples must stay explicit and fail closed rather than inventing permissive fallback behavior.
- Broadening aggregate validation increases target count, so the implementation should stay deterministic and avoid duplicating artifact coverage unnecessarily.
- The follow-up review pass must confirm the fix closes the example-validation gap rather than only patching the two currently broken examples.

## References
- core/control_plane/examples/valid/indexes/foundation_index.v1.example.json
- core/control_plane/examples/valid/indexes/traceability_index.v1.example.json
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/standards/validations/repository_validation_standard.md
- docs/standards/data_contracts/schema_standard.md
