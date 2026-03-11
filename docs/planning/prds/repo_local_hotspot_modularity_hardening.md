---
trace_id: trace.repo_local_hotspot_modularity
id: prd.repo_local_hotspot_modularity
title: Repo-Local Hotspot Modularity Hardening PRD
summary: Reduce the remaining centralized repo-local hotspot modules that the March
  2026 report set still identifies as maintenance pressure.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T05:43:42Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/integrations/github/
---

# Repo-Local Hotspot Modularity Hardening PRD

## Record Metadata
- `Trace ID`: `trace.repo_local_hotspot_modularity`
- `PRD ID`: `prd.repo_local_hotspot_modularity`
- `Status`: `active`
- `Linked Decisions`: `decision.repo_local_hotspot_modularity_direction`
- `Linked Designs`: `design.features.repo_local_hotspot_modularity`
- `Linked Implementation Plans`: `design.implementation.repo_local_hotspot_modularity`
- `Updated At`: `2026-03-11T05:43:42Z`

## Summary
Reduce the remaining centralized repo-local hotspot modules that the March 2026 report set still identifies as maintenance pressure.

## Problem Statement
The March 2026 report set was re-reviewed against the live repository after the standard-operationalization, runtime-boundary, route-preview, planning-contract, health-reporting, and query-modularity traces closed. Those earlier findings no longer reproduce as active defects. One issue cluster still does: several repo-local orchestration surfaces remain oversized enough that the report's centralization warning still validates.

The still-live hotspots are concentrated in:

- `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`
- `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`
- `core/python/src/watchtower_core/repo_ops/sync/traceability.py`
- `core/python/src/watchtower_core/repo_ops/sync/github_tasks.py`
- `core/python/src/watchtower_core/integrations/github/client.py`
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/cli/sync_handlers.py`

Those modules still carry too much registration, builder, and orchestration responsibility in one place. That raises maintenance cost, makes future review harder, and leaves the report's remaining modularity concern unresolved.

## Goals
- Reduce the size and responsibility concentration of the remaining report-validated repo-local hotspot modules.
- Preserve current CLI contracts, task and planning behavior, sync outputs, and GitHub integration behavior while modularizing the code behind them.
- Keep the final report remediation state explicit by closing the last still-live modularity issue cluster in one bounded trace.

## Non-Goals
- Reopening already-closed report issues around standards metadata, runtime package documentation, route preview, planning-contract unification, or health-reporting clarity.
- Starting product-facing pack implementation or changing the public export-safe boundary for `watchtower_core`.
- Redesigning repo-local orchestration behavior; this trace is a structure-hardening pass, not a behavior change initiative.

## Requirements
- `req.repo_local_hotspot_modularity.001`: The initiative must reduce the remaining report-validated hotspot modules by splitting centralized builder, registration, or orchestration logic into smaller helpers while preserving existing import paths for current internal consumers.
- `req.repo_local_hotspot_modularity.002`: Sync CLI registration and runtime handlers must remain behaviorally stable while becoming materially smaller and easier to review.
- `req.repo_local_hotspot_modularity.003`: Planning scaffolds, task lifecycle operations, traceability sync, GitHub task sync, and GitHub client surfaces must preserve their current contracts and tests while reducing centralization pressure.
- `req.repo_local_hotspot_modularity.004`: The work must stay bounded to repo-local orchestration surfaces and must not reopen export-boundary or product-scope decisions.
- `req.repo_local_hotspot_modularity.005`: The repository must remain green on the current sync, validation, unit-test, typecheck, and lint baseline throughout the trace.

## Acceptance Criteria
- `ac.repo_local_hotspot_modularity.001`: The planning corpus publishes an active PRD, accepted direction decision, feature design, implementation plan, closed bootstrap task, and durable execution tasks for `trace.repo_local_hotspot_modularity`.
- `ac.repo_local_hotspot_modularity.002`: `planning_scaffolds.py`, `task_lifecycle.py`, `sync_family.py`, `sync_handlers.py`, `traceability.py`, `github_tasks.py`, and `client.py` are materially smaller or reduced to thin facades backed by explicit helper modules.
- `ac.repo_local_hotspot_modularity.003`: Existing task, planning, sync, and GitHub-facing behavior remains stable under targeted regression coverage.
- `ac.repo_local_hotspot_modularity.004`: Companion planning trackers, derived indexes, and affected docs stay aligned in the same change set.
- `ac.repo_local_hotspot_modularity.005`: The repository passes the final closeout baseline, including `watchtower-core sync all --write`, `watchtower-core validate all --skip-acceptance --format json`, targeted `watchtower-core validate acceptance --trace-id trace.repo_local_hotspot_modularity --format json`, `pytest`, `mypy`, and `ruff`.

## Risks and Dependencies
- Mechanical modularity refactors can create import drift unless thin compatibility facades and regression coverage stay explicit.
- Splitting repo-local orchestration too aggressively could obscure the current authority boundary instead of clarifying it.
- The trace depends on the already-closed export-boundary and query-modularity work, which established the current runtime/package shape and should not be reopened here.

## Open Questions
- Whether `query_coordination_handlers.py` should be pulled into a later follow-up if coordination-query growth continues after this remaining report-set hotspot pass closes.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): simplify hidden machinery without changing durable behavior or flattening the architecture.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep planning docs, trackers, tests, and machine-readable surfaces aligned as the refactor lands.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): keep the work inside the shared repository-maintenance substrate rather than expanding into future pack behavior.

## References
- report/01_overview_and_method.md
- report/06_core_python_architecture_and_exportability.md
- report/09_remediation_program.md
- [core_export_readiness_and_optimization.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_readiness_and_optimization.md)
- [core_export_hardening_followup.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_hardening_followup.md)
- [end_to_end_repo_review_and_rationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/end_to_end_repo_review_and_rationalization.md)
