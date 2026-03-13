---
trace_id: trace.validation_test_hotspot_rebalancing
id: design.features.validation_test_hotspot_rebalancing
title: Validation Test Hotspot Rebalancing Feature Design
summary: Defines the technical design boundary for Validation Test Hotspot Rebalancing.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T18:46:53Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/cli/validation_handlers.py
- docs/commands/core_python/
- docs/planning/
---

# Validation Test Hotspot Rebalancing Feature Design

## Record Metadata
- `Trace ID`: `trace.validation_test_hotspot_rebalancing`
- `Design ID`: `design.features.validation_test_hotspot_rebalancing`
- `Design Status`: `active`
- `Linked PRDs`: `prd.validation_test_hotspot_rebalancing`
- `Linked Decisions`: `decision.validation_test_hotspot_rebalancing_direction`
- `Linked Implementation Plans`: `design.implementation.validation_test_hotspot_rebalancing`
- `Updated At`: `2026-03-13T18:46:53Z`

## Summary
Defines the technical design boundary for Validation Test Hotspot Rebalancing.

## Source Request
- Another comprehensive internal refactor review was requested against the March 13, 2026 refactor audit, with instructions to keep reviewing under one stable theme until repeated confirmation passes found no new actionable issue.
- The discovery pass confirmed that the remaining live portion of `RF-TST-001` is now concentrated in `test_control_plane_artifacts.py`, `test_document_semantics_validation.py`, and their adjacent README-backed repository-path discoverability surfaces.

## Scope and Feature Boundary
- Covers the two remaining oversized governed validation suites, their direct helper seams, the artifact and document-semantics validation services they exercise, the aggregate validation orchestration path, unit or integration README inventories, repository-path indexing, and adjacent traced governance surfaces required to close the slice coherently.
- Covers compatibility handling for the historical hotspot file paths so planning traces and query-path discovery stay stable while the real tests move into focused suites.
- Excludes changes to validation runtime behavior, validator registry contracts, schema shapes, control-plane artifact families, or the broad command-surface design outside documentation and indexing updates required by the test split.

## Current-State Context
- `core/python/tests/integration/test_control_plane_artifacts.py` is still 1171 lines long and mixes loader, schema, example, foundations, standards, template, front-matter, and workflow checks in one file with only two small local helpers.
- `core/python/tests/unit/test_document_semantics_validation.py` is still 1053 lines long, contains six large inline fixture-writing helpers, and mixes validator selection, reference semantics, standard semantics, planning semantics, and canonical path rules in one file.
- `core/python/tests/unit/README.md` does not list `test_document_semantics_validation.py`, `core/python/tests/integration/README.md` does not list `test_control_plane_artifacts.py`, and `watchtower-core query paths --query test_control_plane_artifacts --format json` plus the same probe for `test_document_semantics_validation` both return `result_count: 0`.
- More than 300 planning references still mention `test_control_plane_artifacts.py`, and more than 100 still mention `test_document_semantics_validation.py`, so the design must preserve historical path compatibility instead of simply deleting the old filenames.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keeps the test surface explicit, inspectable, and local-first rather than collapsing coverage into opaque generators or helper magic.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): requires deterministic repository-aware validation instead of reducing the live contract checks to shallow mocks.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires companion human and machine surfaces to stay synchronized when layout or discoverability changes.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): constrains package-local test layout, workspace command execution, and same-change documentation alignment.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): README inventories are governed entrypoint surfaces and must stay current when test-family structure changes.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): README inventory changes must continue to drive a coherent repository-path index and query-path surface.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): traced execution work needs durable tasks and aligned planning closeout surfaces.

## Design Goals and Constraints
- Improve failure locality and maintainability for the remaining governed validation hotspots without reducing contract breadth.
- Preserve the current validation runtime behavior, loader behavior, and command-layer output semantics.
- Keep the historical hotspot file paths present as thin compatibility markers so planning references and query surfaces do not drift.

## Options Considered
### Option 1
- Keep the two large files in place and extract only a few helper functions inside them.
- Lowest immediate churn and no file movement.
- Leaves the mixed-family hotspot boundaries largely intact and does not solve README or repository-path discoverability drift.

### Option 2
- Split the real tests into family-oriented suites backed by small explicit helper modules, keep the historical hotspot filenames as compatibility markers, and refresh README inventories so repository-path indexing stays coherent.
- Improves failure locality, preserves repository-aware assertions, and avoids widespread historical-path drift.
- Requires careful curation of suite boundaries and same-change inventory updates so the split remains discoverable.

### Option 3
- Replace much of the explicit test structure with generated parameter tables or more generic fixture factories.
- Cuts repetition the most aggressively.
- Rejected because it would make governed validation expectations less inspectable and harder to debug when a single family regresses.

## Recommended Design
### Architecture
- Replace `test_control_plane_artifacts.py` with focused integration files grouped by validation family, backed by one small helper module for repeated JSON or front-matter loading and repository-aware assertions.
- Replace `test_document_semantics_validation.py` with focused unit files grouped by validator-selection, reference semantics, standard semantics, and planning semantics rules, backed by one small fixture-writer helper module.
- Keep `test_control_plane_artifacts.py` and `test_document_semantics_validation.py` as compatibility-marker files that explain the new suite layout and preserve historical repository paths.
- Refresh the unit and integration READMEs so the repository-path index and `query paths` surface expose both the compatibility markers and the new focused suite families.

### Data and Interface Impacts
- No schema, validator-registry, or runtime command-interface changes are expected.
- Repository-path index entries will change because README inventories will start listing the compatibility markers and the new focused suites.
- The validation-evidence and acceptance surfaces must capture the final focused-suite layout and the discoverability confirmation probes.

### Execution Flow
1. Publish the bounded planning chain, coverage map, findings ledger, decision, and execution tasks for the validation-hotspot slice.
2. Split the integration hotspot into focused suites plus helper-backed compatibility handling and align adjacent README inventory surfaces.
3. Split the document-semantics hotspot into focused suites plus reusable fixture writers, then refresh README or repository-path discoverability and rerun targeted validation before full closeout.

### Invariants and Failure Cases
- Live repository-aware assertions must remain in place for schemas, examples, authored docs, and validator-selection behavior; the split must not replace them with mocks.
- Compatibility-marker files must not accidentally shadow or duplicate the real test collection in ways that change pytest behavior.
- README inventory drift is a fail-closed concern because it changes repository-path indexing and query-path discovery for the touched test surfaces.

## Affected Surfaces
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/integration/README.md
- core/python/tests/unit/README.md
- core/control_plane/indexes/repository_paths/repository_path_index.v1.json
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/src/watchtower_core/cli/validation_handlers.py
- docs/commands/core_python/watchtower_core_validate.md
- docs/planning/

## Design Guardrails
- Prefer small explicit helper modules and focused test files over reflection-heavy test generation or hidden fixture magic.
- Do not change validation command behavior, loader outputs, or schema contracts unless a confirmation pass finds a same-theme correctness issue that must be fixed.

## Risks
- A split that groups tests along the wrong boundary could preserve file count growth without materially improving failure locality.
- Shared fixture helpers could become opaque if they grow beyond the minimum needed to keep the focused suites readable.
- Compatibility markers and README inventories must stay synchronized or the repository-path discoverability fix will regress.

## References
- March 13, 2026 refactor audit
- [validation_test_hotspot_rebalancing.md](/home/j/WatchTowerPlan/docs/planning/prds/validation_test_hotspot_rebalancing.md)
