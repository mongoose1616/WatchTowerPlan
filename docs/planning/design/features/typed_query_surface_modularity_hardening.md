---
trace_id: trace.typed_query_surface_modularity_hardening
id: design.features.typed_query_surface_modularity_hardening
title: Typed Query Surface Modularity Hardening Feature Design
summary: Defines the technical design boundary for Typed Query Surface Modularity
  Hardening.
type: feature_design
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
- core/python/src/watchtower_core/control_plane/README.md
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
---

# Typed Query Surface Modularity Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.typed_query_surface_modularity_hardening`
- `Design ID`: `design.features.typed_query_surface_modularity_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.typed_query_surface_modularity_hardening`
- `Linked Decisions`: `decision.typed_query_surface_modularity_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.typed_query_surface_modularity_hardening`
- `Updated At`: `2026-03-13T17:56:36Z`

## Summary
Defines the technical design boundary for Typed Query Surface Modularity Hardening.

## Source Request
- The user requested another comprehensive internal refactor review using the March 13, 2026 external audit at `/home/j/WatchTower/REFACTOR.md`, with a stable same-theme review loop that continues until no new actionable issue remains.
- The discovery pass confirmed two still-actionable audit clusters under one bounded retrieval theme: `RF-PY-003` for `core/python/src/watchtower_core/control_plane/models/planning.py` and `RF-TST-001` for `core/python/tests/unit/test_cli_query_commands.py`.

## Scope and Feature Boundary
- Covers typed index-entry and index models for PRDs, decisions, design docs, references, foundations, standards, and workflows; their direct loader or query consumers; runtime-boundary docs; and the broad CLI query regression suite that exercises the same retrieval surface.
- Covers same-change planning, task, acceptance-contract, and evidence updates needed to trace, validate, and close the refactor slice correctly.
- Excludes command or schema redesign, broader workflow-routing refactors, and the separate giant artifact-validation or document-semantics hotspot families unless the confirmation loop finds a direct same-theme dependency.

## Current-State Context
- `core/python/src/watchtower_core/control_plane/models/planning.py` currently holds seven near-parallel typed index entry or index pairs inside one 548-line file with repeated tuple-coercion, artifact materialization, and linear `get()` lookup logic.
- `core/python/tests/unit/test_cli_query_commands.py` currently groups 35 tests across paths, route preview, task create, plan scaffold, knowledge queries, planning queries, coordination queries, and authority or trace queries into one 912-line file with repeated `main([...])`, `capsys`, and JSON-assertion patterns.
- Direct consumer pressure is real: `ControlPlaneLoader`, multiple `repo_ops/query/*.py` services, planning-sync code, acceptance validation, and CLI handlers all depend on the typed model export surface staying stable.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): requires explicit, inspectable typed surfaces and rejects opaque abstractions that blur authority boundaries.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): favors local-first deterministic code and reviewable repository-native helpers over clever indirection.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): keeps the Python workspace layout explicit and requires runtime-boundary docs to stay aligned when package boundaries change materially.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): traced execution work needs durable task records and aligned derived planning surfaces.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): constrains the bounded task set shape used to execute and close the slice.

## Design Goals and Constraints
- Reduce hotspot size and repeated boilerplate while keeping the typed model contracts explicit at the field level.
- Improve test failure locality without reducing full-command coverage or replacing governed-surface checks with shallow helper-only assertions.
- Preserve the stable `watchtower_core.control_plane.models` re-export surface, `ControlPlaneLoader.load_*` behavior, index schemas, query payloads, and deterministic validation posture.

## Options Considered
### Option 1
- Keep the large model and test files in place, adding only local helper functions inside each file.
- Lower immediate churn and fewer import changes.
- Leaves the mixed-domain hotspots mostly intact and does not materially improve failure locality or boundary clarity.

### Option 2
- Split the typed models into domain-focused modules backed by small explicit helper functions, and split the CLI-query regression hotspot into narrower family-specific suites with one shared JSON-command helper.
- Cuts the two confirmed hotspots down at their real fault lines while preserving explicit dataclasses, stable public imports, and end-to-end command coverage.
- Requires careful consumer and re-export alignment so internal module moves do not leak into stable import or behavior surfaces.

### Option 3
- Introduce generic model registries or metaprogrammed base classes to generate most entry or index pairs automatically.
- Minimizes handwritten repetition the most.
- Conflicts with the audit guardrails because it would make typed authority contracts less inspectable and harder to debug.

## Recommended Design
### Architecture
- Move the typed planning-document index models into one domain-focused module and the reference or foundation or standard or workflow index models into a second domain-focused module, with one small shared helper module for explicit tuple coercion, artifact materialization, and `get()` lookups.
- Preserve `watchtower_core.control_plane.models.__init__` as the stable public import surface so loaders, query services, sync code, validators, and tests continue to import the same names.
- Replace the monolithic `test_cli_query_commands.py` suite with narrower files grouped by command family, backed by one small helper that runs commands and returns parsed JSON payloads without hiding the real CLI invocation path.

### Data and Interface Impacts
- No control-plane JSON schema or index-shape changes are expected.
- Public Python type names and loader methods must remain stable even though their implementation modules change.
- Runtime-boundary docs under `core/python/src/watchtower_core/control_plane/` and any touched planning surfaces must describe the split accurately.

### Execution Flow
1. Establish the traced planning, acceptance, evidence, and task surfaces for the bounded retrieval-modularity slice.
2. Split the typed model hotspot into focused modules plus explicit shared helpers, then update `__init__`, `ControlPlaneLoader`, and all direct consumers so imports and behavior remain stable.
3. Split the CLI query regression hotspot into focused suites plus shared command or JSON helpers, then rerun targeted and full validation until repeated confirmation passes find no new same-theme issue.

### Invariants and Failure Cases
- Typed dataclasses must stay explicit and inspectable; the refactor must not hide required fields or defaulting rules behind dynamic registration.
- `ControlPlaneLoader.load_*` methods must keep returning the same typed artifacts, and `get()` methods must keep their current `KeyError` behavior on missing identifiers.
- The shared test helper must still execute the real CLI entrypoint and parse the real JSON output so command behavior drift cannot hide behind helper-only assertions.

## Affected Surfaces
- `core/python/src/watchtower_core/control_plane/models/`
- `core/python/src/watchtower_core/control_plane/loader.py`
- `core/python/src/watchtower_core/repo_ops/query/`
- `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
- `core/python/src/watchtower_core/validation/acceptance.py`
- `core/python/tests/unit/`
- `core/python/src/watchtower_core/control_plane/README.md`
- `docs/planning/`
- `core/control_plane/contracts/acceptance/typed_query_surface_modularity_hardening_acceptance.v1.json`
- `core/control_plane/ledgers/validation_evidence/typed_query_surface_modularity_hardening_planning_baseline.v1.json`

## Design Guardrails
- Prefer small explicit helpers over generic registries or reflection-heavy abstractions.
- Keep query, sync, validation, and loader behavior unchanged unless the confirmation loop finds a same-theme correctness issue that must be fixed.
- Do not widen this slice into a broader command-surface or workflow-lattice redesign just because adjacent files are large.

## Risks
- Consumer drift is the main implementation risk because the typed model names are imported across loader, query, sync, validation, and tests.
- Test-file splits can accidentally overfit helpers or miss a family if the new suite boundaries are chosen poorly.
- A confirmation pass may still expose an adjacent hotspot in loader or query serialization that has to be fixed before this theme can close.

## References
- March 13, 2026 refactor audit
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/typed_query_surface_modularity_hardening.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
