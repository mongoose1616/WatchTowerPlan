---
trace_id: trace.typed_query_surface_modularity_hardening
id: prd.typed_query_surface_modularity_hardening
title: Typed Query Surface Modularity Hardening PRD
summary: Review and refactor the typed planning and documentation retrieval surface
  so index models, loader consumers, and query test coverage become more modular without
  changing query behavior, validation fidelity, or governed authority boundaries.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T17:56:36Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/models/
- core/python/src/watchtower_core/control_plane/loader.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/unit/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
- docs/planning/
---

# Typed Query Surface Modularity Hardening PRD

## Record Metadata
- `Trace ID`: `trace.typed_query_surface_modularity_hardening`
- `PRD ID`: `prd.typed_query_surface_modularity_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.typed_query_surface_modularity_hardening_direction`
- `Linked Designs`: `design.features.typed_query_surface_modularity_hardening`
- `Linked Implementation Plans`: `design.implementation.typed_query_surface_modularity_hardening`
- `Updated At`: `2026-03-13T17:56:36Z`

## Summary
Review and refactor the typed planning and documentation retrieval surface so index models, loader consumers, and query test coverage become more modular without changing query behavior, validation fidelity, or governed authority boundaries.

## Problem Statement
- The March 13, 2026 refactor audit still reproduces `RF-PY-003` and `RF-TST-001` under the typed retrieval surface even after the earlier coordination, reference-signaling, and planning-authoring refactor traces were closed.
- `core/python/src/watchtower_core/control_plane/models/planning.py` remains a 548-line mixed-domain hotspot that defines seven index entry or index pairs with repeated `from_document()` and `get()` patterns, making low-level index-shape maintenance noisier than it needs to be.
- `core/python/tests/unit/test_cli_query_commands.py` remains a 912-line mixed-family suite with 35 tests spanning route previews, dry-run authoring commands, knowledge queries, planning queries, and coordination queries, which weakens failure locality and makes same-theme query changes harder to review.
- Direct consumers remain stable today, but they span `ControlPlaneLoader`, repo-local query services, planning-sync consumers, acceptance validation, and CLI handlers, so a sloppy refactor would risk import drift or behavior drift across a wide retrieval boundary.

## Goals
- Split the typed planning and documentation retrieval models into smaller domain-focused modules with explicit helper-backed materialization patterns while preserving inspectable dataclasses and stable public imports.
- Split the broad CLI query regression hotspot into narrower suites with shared helper assertions so query, route-preview, and dry-run planning checks keep their real command coverage but gain better locality.
- Review loader consumers, query consumers, runtime boundary docs, and adjacent governed planning surfaces under the same theme until repeated confirmation passes find no new actionable issue.
- Preserve deterministic query behavior, governed artifact shapes, schema-backed validation, and the stable `watchtower_core.control_plane.models` import boundary.

## Non-Goals
- Changing command names, flags, JSON payload shapes, or the underlying control-plane index schemas.
- Redesigning the whole query command family or reopening the separate command-surface breadth and workflow-lattice audit slices.
- Replacing explicit typed dataclasses with opaque metaprogramming or generated model registries just to reduce line count.
- Reducing live governed-artifact coverage, swapping real loader or CLI calls for shallow mocks, or weakening full-repo validation.

## Requirements
- `req.typed_query_surface_modularity_hardening.001`: The trace must publish and follow an explicit coverage map plus findings ledger across typed models, loader consumers, query consumers, runtime docs, tests, planning trackers, acceptance surfaces, and evidence surfaces before remediation begins.
- `req.typed_query_surface_modularity_hardening.002`: The typed planning and documentation retrieval models must move into smaller domain-focused modules with explicit shared helper-backed materialization or lookup seams while preserving current exported type names, loader return types, and query or sync consumer behavior.
- `req.typed_query_surface_modularity_hardening.003`: Direct loader and query consumers plus adjacent runtime-boundary docs must stay aligned with the refactor in the same change set, with no CLI behavior drift and no human-versus-machine authority drift.
- `req.typed_query_surface_modularity_hardening.004`: The oversized CLI query regression hotspot must split into narrower suites and shared helpers without reducing real command coverage, fixture fidelity, or current assertions over query, route-preview, and planning dry-run behavior.
- `req.typed_query_surface_modularity_hardening.005`: The initiative must run targeted validation, full repository validation, a post-fix review pass, a second-angle no-new-issues review, and an adversarial confirmation pass; if any new same-theme issue appears, the loop must reopen until consecutive confirmation passes are clean.

## Acceptance Criteria
- `ac.typed_query_surface_modularity_hardening.001`: The planning corpus for `trace.typed_query_surface_modularity_hardening` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, bounded execution tasks, and the explicit coverage map plus findings ledger for the slice.
- `ac.typed_query_surface_modularity_hardening.002`: Typed planning and documentation retrieval models live in smaller domain-focused modules with explicit helper-backed materialization or lookup seams, and `watchtower_core.control_plane.models` plus `ControlPlaneLoader.load_*` continue to expose the same stable public behavior.
- `ac.typed_query_surface_modularity_hardening.003`: Direct loader, query, sync, and validation consumers of the typed retrieval models stay aligned with the refactor, and runtime boundary docs continue to describe the control-plane model boundary accurately.
- `ac.typed_query_surface_modularity_hardening.004`: CLI query, route-preview, and dry-run planning regressions run from narrower suites with shared helpers while preserving the covered command families and current JSON-payload expectations.
- `ac.typed_query_surface_modularity_hardening.005`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation all complete without finding a new actionable issue in the typed retrieval modularity theme.

## Risks and Dependencies
- Over-abstracting the typed models could hide field-level authority expectations instead of clarifying them.
- Splitting the CLI-query hotspot could accidentally drop coverage if the new helpers start asserting only helper behavior instead of full command behavior.
- The refactor depends on preserving the re-export boundary in `watchtower_core.control_plane.models`; missing one consumer update could break query, sync, or validation code outside the immediate hotspot.

## References
- March 13, 2026 refactor audit
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
