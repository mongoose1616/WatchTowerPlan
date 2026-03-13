---
trace_id: trace.planning_authoring_hotspot_regression_hardening
id: design.features.planning_authoring_hotspot_regression_hardening
title: Planning Authoring Hotspot Regression Hardening Feature Design
summary: Defines the technical design boundary for Planning Authoring Hotspot Regression
  Hardening.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T17:26:00Z'
audience: shared
authority: authoritative
---

# Planning Authoring Hotspot Regression Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.planning_authoring_hotspot_regression_hardening`
- `Design ID`: `design.features.planning_authoring_hotspot_regression_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.planning_authoring_hotspot_regression_hardening`
- `Linked Decisions`: `decision.planning_authoring_hotspot_regression_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.planning_authoring_hotspot_regression_hardening`
- `Updated At`: `2026-03-13T17:26:00Z`

## Summary
Defines the technical design boundary for Planning Authoring Hotspot Regression Hardening.

## Source Request
- Perform another comprehensive internal refactor review, follow the traced task cycle, and keep reviewing under the same theme until repeated confirmation passes find no new actionable issue.

## Scope and Feature Boundary
- Covers `planning_scaffolds.py`, `planning_scaffold_support.py`, task lifecycle mutation, governed companion-path repair, adjacent plan or task command docs, targeted runtime-boundary docs, and the planning trackers or indexes affected by those writes.
- Covers declarative scaffold-kind contracts, helper-backed rendering seams, helper-backed bootstrap acceptance or evidence generation, helper-backed planning-surface refresh, and isolated task companion repair.
- Does not reopen sync CLI or traceability or GitHub hotspot modularity surfaces from the earlier trace.
- Does not change user-facing `plan` or `task` command behavior, artifact shapes, or control-plane schema contracts.

## Current-State Context
- The earlier `trace.repo_local_hotspot_modularity` closed correctly for the March 11, 2026 codebase, but later fixes added 538 net lines back across planning scaffold and task lifecycle hotspot files.
- `planning_scaffolds.py` now directly coordinates scaffold rendering, bootstrap acceptance-contract generation, bootstrap validation-evidence generation, per-kind tracker or index refresh, and coordination refresh decisions.
- `task_lifecycle.py` now directly rewrites acceptance-contract and validation-evidence internals when a task path changes, so the mutation service once again understands governed companion artifact structure.
- `planning_scaffold_support.py` still carries several parallel per-kind maps and one large `render_sections()` branch, so scaffold-contract updates still require synchronized edits across multiple structures.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keep repo-local orchestration explicit, readable, and bounded without leaking repository semantics into reusable core.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): same-change updates must keep code, docs, trackers, and machine-readable surfaces aligned through the refactor.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task path moves must keep governed acceptance and validation-evidence references aligned in the same change set.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): task-document placement and section contracts remain unchanged while internals move into helpers.
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md): PRD scaffolds must retain the current section and metadata contract under the new helper structure.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): feature-design scaffolds must retain the explained applied-reference sections under the split renderers.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): implementation-plan scaffolds must retain the current required-source and validation-plan structure.
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md): decision scaffolds must retain the current decision-status and explained reference contract.

## Design Goals and Constraints
- Reduce blast radius by separating scaffold specs, scaffold rendering, bootstrap artifact builders, planning-surface refresh, and task companion repair into explicit collaborators.
- Keep `PlanningScaffoldService`, `TaskLifecycleService`, `watchtower-core plan`, and `watchtower-core task` behavior stable.
- Preserve fail-closed validation, canonicalized governed paths, deterministic coordination refresh, and acceptance or evidence rewrite semantics.

## Options Considered
### Option 1
- Leave the regrown hotspot in place and treat the audit language as advisory noise because a prior modularity trace already closed.
- Strength: no mechanical refactor churn now.
- Tradeoff: leaves a reproducible same-theme regression unaddressed and keeps the current write path concentrated in a few files again.

### Option 2
- Perform a broader redesign of planning or task authoring around a new generic orchestration framework.
- Strength: could reduce repeated authoring patterns more aggressively.
- Tradeoff: too large for this bounded refactor slice and risks changing stable repo-local behavior while chasing architecture purity.

### Option 3
- Extract focused helper modules for scaffold-kind specs, section rendering, bootstrap artifacts, planning-surface refresh, and task companion repair while keeping the current services as readable orchestration entrypoints.
- Strength: fixes the reproduced hotspot with the smallest behavior-preserving seam changes.
- Tradeoff: still requires disciplined same-change updates across docs, trackers, tests, and machine-readable planning surfaces.

## Recommended Design
### Architecture
- Keep `PlanningScaffoldService` as the stable orchestration entrypoint, but move scaffold-kind contracts into a declarative spec module, move section rendering and rendered-document validation into a dedicated rendering module, and move bootstrap acceptance or evidence building plus planning-surface refresh into dedicated helper modules.
- Keep `planning_scaffold_support.py` as a thin compatibility-oriented support surface that re-exports the stable helpers the service already imports.
- Keep `TaskLifecycleService` as the stable task mutation entrypoint, but move governed companion-path repair into a dedicated helper-backed collaborator instead of inlining acceptance-contract and validation-evidence document traversal inside the service.

### Data and Interface Impacts
- No user-facing CLI payload, schema, or governed artifact shape changes are intended.
- Planning trackers and indexes will refresh because the trace adds new planning and task documents and later lands same-change code or doc updates.
- Adjacent runtime-boundary docs may need small updates so the refactored helper seams are discoverable without changing command docs that describe stable behavior only.

### Execution Flow
1. Replace the scaffold placeholders with the explicit coverage map, findings ledger, accepted direction, acceptance contract, and bounded task chain for this hotspot-regression trace.
2. Extract declarative scaffold-kind specs plus helper-backed scaffold rendering, bootstrap artifact building, and planning-surface refresh while keeping `PlanningScaffoldService` stable.
3. Extract governed task companion-path repair into a helper-backed collaborator and align task docs or tests or runtime-boundary docs with the new seam.
4. Rebuild derived surfaces, run targeted validation and full validation, then perform repeated confirmation passes until the same theme stays clean.

### Invariants and Failure Cases
- Scaffolded PRDs, feature designs, implementation plans, and decisions must still render the same required sections and metadata relationships.
- Task create or update or transition writes must still repair governed acceptance-contract and validation-evidence paths before the old task path disappears.
- Helper extraction must not introduce import cycles or move repo-local semantics into export-safe reusable packages.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle_support.py
- core/python/src/watchtower_core/cli/plan_handlers.py
- core/python/src/watchtower_core/cli/task_handlers.py
- core/python/tests/unit/test_planning_scaffolds.py
- core/python/tests/integration/test_planning_scaffolds_service.py
- core/python/tests/unit/test_task_lifecycle.py
- core/python/tests/integration/test_task_lifecycle_service.py
- core/python/tests/unit/test_plan_and_task_handlers.py
- docs/commands/core_python/watchtower_core_plan.md
- docs/commands/core_python/watchtower_core_task.md
- core/python/src/watchtower_core/repo_ops/README.md

## Design Guardrails
- Prefer helper extraction and thin orchestration over a new meta-framework or reflection-heavy generic planner.
- Do not change command flags, output shapes, task document placement, or planning artifact contracts as part of the refactor.
- Do not rewrite or supersede the historical `trace.repo_local_hotspot_modularity`; record the regression context in this new trace instead.

## Risks
- Over-splitting could make the end-to-end write path harder to inspect.
- A missed same-change update could leave docs or planning projections describing an old hotspot boundary even if runtime code is cleaner.
- The previous trace’s historical “resolved” language may be misread unless this new trace clearly explains why the theme reopened.

## References
- March 13, 2026 refactor audit
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/repo_local_hotspot_modularity_hardening.md)
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/repo_local_hotspot_modularity_hardening.md)
