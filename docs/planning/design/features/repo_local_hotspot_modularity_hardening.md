---
trace_id: trace.repo_local_hotspot_modularity
id: design.features.repo_local_hotspot_modularity
title: Repo-Local Hotspot Modularity Hardening Feature Design
summary: Defines the technical design boundary for reducing the remaining report-validated repo-local hotspot modules without changing behavior.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T06:43:01Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/integrations/github/
---

# Repo-Local Hotspot Modularity Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.repo_local_hotspot_modularity`
- `Design ID`: `design.features.repo_local_hotspot_modularity`
- `Design Status`: `active`
- `Linked PRDs`: `prd.repo_local_hotspot_modularity`
- `Linked Decisions`: `decision.repo_local_hotspot_modularity_direction`
- `Linked Implementation Plans`: `design.implementation.repo_local_hotspot_modularity`
- `Updated At`: `2026-03-11T06:43:01Z`

## Summary
Defines the technical design boundary for reducing the remaining report-validated repo-local hotspot modules without changing behavior.

## Source Request
- Review the March 2026 maintenance findings again, verify each issue, and take every still-valid issue through the standard end-to-end task cycle.

## Scope and Feature Boundary
- Covers the remaining centralized repo-local orchestration surfaces still called out by the report examples: planning scaffolds, task lifecycle, sync CLI registration and handlers, traceability sync, GitHub task sync, and the GitHub client.
- Covers helper-module extraction, thin compatibility facades, and targeted regression coverage for those surfaces.
- Does not reopen the closed runtime-boundary, route-preview, health-reporting, or query-modularity traces.
- Does not change durable CLI contracts, sync artifact shapes, GitHub sync semantics, or task and planning document contracts.

## Current-State Context
- The live repo now closes the other March 2026 report findings through earlier traces, but the report's remaining modularity examples still reproduce as oversized repo-local source files.
- `planning_scaffolds.py` and `task_lifecycle.py` still centralize multiple document-authoring and mutation responsibilities, while `sync_family.py` and `sync_handlers.py` still carry a large amount of parser construction and command execution wiring.
- `traceability.py`, `github_tasks.py`, and `integrations/github/client.py` remain functional and tested, but they still combine several responsibilities in one file and keep the report's centralization concern alive.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the refactor should create explicit, bounded seams instead of replacing the repo's current service boundaries.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): report follow-up should close the still-live issue fail closed with validation and tracker alignment rather than treating it as advisory cleanup.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): internal modularity hardening should improve implementation readiness without expanding scope into new product-facing architecture.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): helper extraction should reduce file-local responsibility concentration while preserving stable behavior.
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): code-adjacent README updates need to stay semantically aligned with the refactored command and package structure.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): the report finding should move through the bounded initiative lifecycle with explicit validation and closeout evidence.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the new planning chain, acceptance contract, tasks, and evidence must remain joined through the trace.

## Design Goals and Constraints
- Reduce maintenance risk by moving repeated or separable logic into explicit helper modules grouped by concern.
- Keep all existing import paths that current code and tests rely on, either directly or through thin facades, so the trace stays behavior-preserving.
- Preserve deterministic sync ordering, task-document validation, planning-scaffold validation, and GitHub API semantics.

## Options Considered
### Option 1
- Leave the remaining hotspots in place and treat the report language as future P2 cleanup only.
- Strength: no immediate refactor churn.
- Tradeoff: leaves the re-review with one still-live report issue cluster and keeps centralization pressure in the exact surfaces the report called out.

### Option 2
- Split the remaining hotspot modules behind helper modules while preserving the current contracts and repo-local boundaries.
- Strength: closes the remaining report-validated modularity gap without reopening broader architecture work.
- Tradeoff: creates a mechanically noisy refactor that depends on disciplined tests and tracker alignment.

## Recommended Design
### Architecture
- Keep the current top-level modules as stable entry surfaces where they are already imported elsewhere, but reduce them to thin facades or focused orchestration layers.
- Extract planning scaffolds into helper modules for metadata normalization, section rendering, and bootstrap orchestration.
- Extract task lifecycle into helpers for normalization, validation, and document mutation so `TaskLifecycleService` stays readable without moving its public contract.
- Split sync CLI registration into grouped parser builders and split sync handlers into grouped execution helpers for document sync, tracker sync, and special-case operations.
- Split traceability sync, GitHub task sync, and GitHub client internals by responsibility while preserving the service classes currently imported by tests and runtime code.

### Data and Interface Impacts
- No new control-plane artifact families or schemas are introduced.
- Planning trackers, task trackers, initiative views, and traceability views will refresh because the trace adds new planning and task documents and then lands code changes.
- Python import surfaces remain stable for existing repo-local consumers; helper modules are internal structure, not new public API.

### Execution Flow
1. Bootstrap the trace, record the direction decision, and create one bounded task per hotspot cluster.
2. Refactor planning scaffolds plus task lifecycle into helper modules and keep their service-level imports stable.
3. Refactor sync CLI registration and handlers plus traceability sync into grouped helpers with targeted regression checks.
4. Refactor GitHub sync and client internals into smaller helpers while preserving `GitHubTaskSyncService` and `GitHubClient`.
5. Refresh derived planning surfaces, validate the repo, publish acceptance evidence, and close the trace.

### Invariants and Failure Cases
- The refactor must not change CLI command names, parser flags, or JSON payload shapes for the affected sync commands.
- The refactor must not relax fail-closed validation for planning scaffolds, task lifecycle references, sync outputs, or GitHub API error handling.
- Helper extraction must not introduce import cycles across `cli`, `repo_ops`, and `integrations/github`.

## Affected Surfaces
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/integrations/github/
- core/python/tests/
- docs/planning/

## Design Guardrails
- Prefer helper extraction and thin facades over renaming or relocating stable service entrypoints that current tests and repo-local callers already use.
- Do not change durable task, planning, sync, traceability, or GitHub behavior as part of the modularity refactor.
- Do not reopen export-safe namespace design or future pack-runtime seam questions in this trace.

## Risks
- The planning-scaffold and task-lifecycle refactors touch validation-backed authoring flows, so a missed helper boundary could create subtle document-generation regressions.
- The sync CLI split can drift from command docs or parser metadata if the refactor is not validated end to end.
- GitHub client helper extraction can accidentally change request-shape behavior if it mixes formatting cleanup with transport logic changes.

## References
- March 2026 review overview and method summary for the remaining modularity hotspots.
- March 2026 core Python architecture review summary for the still-centralized repo-local orchestration surfaces.
- March 2026 remediation-program summary for the final bounded modularity follow-up.
- [core_export_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_hardening.md)
- [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
