---
trace_id: trace.validation_test_hotspot_rebalancing
id: prd.validation_test_hotspot_rebalancing
title: Validation Test Hotspot Rebalancing PRD
summary: Review and refactor the remaining governed validation test hotspots so artifact
  and document-semantics coverage become more modular without reducing live repository
  contract validation.
type: prd
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

# Validation Test Hotspot Rebalancing PRD

## Record Metadata
- `Trace ID`: `trace.validation_test_hotspot_rebalancing`
- `PRD ID`: `prd.validation_test_hotspot_rebalancing`
- `Status`: `active`
- `Linked Decisions`: `decision.validation_test_hotspot_rebalancing_direction`
- `Linked Designs`: `design.features.validation_test_hotspot_rebalancing`
- `Linked Implementation Plans`: `design.implementation.validation_test_hotspot_rebalancing`
- `Updated At`: `2026-03-13T18:46:53Z`

## Summary
Review and refactor the remaining governed validation test hotspots so artifact and document-semantics coverage become more modular without reducing live repository contract validation.

## Problem Statement
- The March 13, 2026 refactor audit still reproduces the remaining live portion of `RF-TST-001` after the earlier CLI-query hotspot split, concentrating broad repository-contract coverage into `core/python/tests/integration/test_control_plane_artifacts.py` and `core/python/tests/unit/test_document_semantics_validation.py`.
- `test_control_plane_artifacts.py` is still a 1171-line mixed-family integration surface spanning loader coverage, schema-backed artifact validation, foundations and entrypoint checks, standards and template contracts, workflow authoring checks, and front-matter assertions, which weakens failure locality and raises the cost of extending one family safely.
- `test_document_semantics_validation.py` is still a 1053-line mixed-family unit surface with multiple inline fixture writers and cross-family semantic rules for references, standards, workflows, and planning docs, making targeted maintenance noisy and obscuring the direct validator seams it exercises.
- Adjacent discoverability surfaces are also stale: the unit and integration README inventories do not list these hotspots, so the repository path index and `watchtower-core query paths` cannot resolve either file even though more than 400 planning references still point to them.

## Goals
- Split the remaining validation hotspots into smaller family-oriented suites with shared helper support while preserving the same repository-aware coverage and fail-closed validation posture.
- Keep the direct validator, loader, and aggregate-validation boundaries stable so `validate all`, document-semantics validation, artifact validation, and loader-backed repository checks behave exactly as they do today.
- Preserve historical path compatibility for the two hotspot filenames so planning traces, task docs, and repository references do not drift or disappear when the real tests move.
- Refresh adjacent README inventories, repository-path indexing, and trace-planning surfaces in the same change so the new layout stays discoverable and governed.

## Non-Goals
- Changing validation command names, flags, exit-code semantics, JSON payloads, or the current validation-family roster.
- Replacing live repository-aware assertions with shallow mocks, generated golden files, or opaque metaprogrammed test generation just to cut line count.
- Redesigning the full validation architecture, validator registry model, or schema-backed control-plane authority surfaces.
- Reopening the already-closed CLI query test split or unrelated command/query refactor themes.

## Requirements
- `req.validation_test_hotspot_rebalancing.001`: The trace must publish a coverage map and findings ledger across the remaining integration and unit validation hotspots, their direct validator or loader dependencies, README inventory surfaces, repository-path indexing, and traced governance artifacts before remediation begins.
- `req.validation_test_hotspot_rebalancing.002`: The mixed-family integration hotspot must split into focused suites plus small shared helpers without reducing loader, schema, example, front-matter, or authored-contract coverage.
- `req.validation_test_hotspot_rebalancing.003`: The mixed-family document-semantics hotspot must split into focused suites plus reusable fixture writers while preserving validator-selection coverage, fail-closed reference or standard or planning semantics rules, and canonical path checks.
- `req.validation_test_hotspot_rebalancing.004`: Historical path compatibility and repository discoverability must stay aligned through compatibility markers, updated unit or integration README inventories, refreshed repository-path indexing, and query-path confirmation.
- `req.validation_test_hotspot_rebalancing.005`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation must all pass on the final same-theme state before closeout.

## Acceptance Criteria
- `ac.validation_test_hotspot_rebalancing.001`: The planning corpus for `trace.validation_test_hotspot_rebalancing` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, bounded execution tasks, and the explicit coverage map plus findings ledger for the slice.
- `ac.validation_test_hotspot_rebalancing.002`: The old `test_control_plane_artifacts.py` hotspot is replaced by focused integration suites and shared helpers while current loader, schema, example, front-matter, and authored-contract coverage remains live.
- `ac.validation_test_hotspot_rebalancing.003`: The old `test_document_semantics_validation.py` hotspot is replaced by focused unit suites and shared fixture helpers while document-semantics validator coverage and fail-closed rule coverage remain intact.
- `ac.validation_test_hotspot_rebalancing.004`: Compatibility markers, README inventories, repository-path indexing, and `query paths` behavior stay aligned with the split suites so historical references and new discovery paths both work.
- `ac.validation_test_hotspot_rebalancing.005`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation complete with no new actionable issue under the validation-hotspot theme.

## Risks and Dependencies
- Historical planning and task references to the two hotspot filenames are widespread, so removing those paths outright would create unnecessary drift across governed planning artifacts.
- The aggregate validation suite depends on keeping repository-aware assertions live across schemas, docs, and authored control-plane artifacts; a simplistic split could accidentally drop coverage while appearing cleaner.
- Shared helper extraction must stay explicit and local-first so reviewers can still see which fixture shape or repository assertion each focused suite relies on.

## References
- March 13, 2026 refactor audit
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
