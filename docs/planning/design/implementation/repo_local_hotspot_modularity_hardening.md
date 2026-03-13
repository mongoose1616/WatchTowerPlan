---
trace_id: trace.repo_local_hotspot_modularity
id: design.implementation.repo_local_hotspot_modularity
title: Repo-Local Hotspot Modularity Hardening Implementation Plan
summary: Breaks the remaining report-validated repo-local hotspot modularity work into bounded refactor slices.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T06:43:01Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/integrations/github/
---

# Repo-Local Hotspot Modularity Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.repo_local_hotspot_modularity`
- `Plan ID`: `design.implementation.repo_local_hotspot_modularity`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.repo_local_hotspot_modularity`
- `Linked Decisions`: `decision.repo_local_hotspot_modularity_direction`
- `Source Designs`: `design.features.repo_local_hotspot_modularity`
- `Linked Acceptance Contracts`: `contract.acceptance.repo_local_hotspot_modularity`
- `Updated At`: `2026-03-11T06:43:01Z`

## Summary
Breaks the remaining report-validated repo-local hotspot modularity work into bounded refactor slices.

## Source Request or Design
- Review the March 2026 maintenance findings again, verify each issue, and take every still-valid issue through the standard end-to-end task cycle.
- Feature design: [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/repo_local_hotspot_modularity_hardening.md)

## Scope Summary
- Reduce the still-live report-example hotspots in planning scaffolds, task lifecycle, sync CLI registration and handlers, traceability sync, GitHub task sync, and GitHub client internals.
- Keep the work behavior-preserving and bounded to repo-local modularity.
- Close the remaining modularity concern from the March 2026 report set without reopening already-completed traces.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): each slice should favor small helpers, thin facades, and targeted regression coverage.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): task closure and validation evidence need to match the initiative's active-to-validation-to-closeout progression.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the bounded execution slices should each close through terminal task state rather than leaving the report work implicit.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): the final baseline must be published as durable evidence before initiative closeout.

## Assumptions and Constraints
- Existing service and module import paths should remain usable by current repo-local callers and tests.
- The repository is currently green and has no other active initiatives, so this trace can stay tightly focused on the hotspot refactor work.
- The work should land in a small number of coherent slices grouped by responsibility rather than one large mechanical commit.

## Proposed Technical Approach
- Use helper-module extraction to pull normalization, rendering, validation, parser-building, and transport-specific logic out of the oversized files.
- Keep the current top-level modules as compatibility facades or narrow orchestration layers where that avoids wider churn.
- Refresh planning and coordination surfaces after the planning-task changes and validate the end-to-end Python/runtime baseline after each code slice.

## Work Breakdown
1. Bootstrap the trace, publish the direction decision, and create the bounded implementation tasks.
2. Refactor `planning_scaffolds.py` and `task_lifecycle.py` into smaller helper-backed structures, keeping service entrypoints stable.
3. Refactor `sync_family.py`, `sync_handlers.py`, and `traceability.py` into grouped helpers while preserving sync command behavior and payloads.
4. Refactor `github_tasks.py` and `integrations/github/client.py` into smaller helper-backed structures while preserving GitHub sync behavior.
5. Publish an acceptance contract and evidence, rerun the validation baseline, close the tasks, and close the initiative.

## Risks
- The refactor footprint spans several highly used repo-local services, so missing one shared helper import can cascade into multiple command failures.
- Existing tests focus on behavior rather than file topology, so extra targeted regression checks may be needed when facades replace large modules.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json` after planning and governed-surface changes.
- Run `./.venv/bin/watchtower-core validate all --skip-acceptance --format json` after each refactor slice.
- Run targeted unit and integration coverage for planning scaffolds, task lifecycle, traceability sync, GitHub sync, GitHub client, and CLI sync handlers while the slices land.
- Run the final closeout baseline with `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src`, `./.venv/bin/ruff check .`, and `./.venv/bin/watchtower-core validate acceptance --trace-id trace.repo_local_hotspot_modularity --format json`.

## References
- March 2026 review overview and method summary for the remaining modularity hotspots.
- March 2026 core Python architecture review summary for the still-centralized repo-local orchestration surfaces.
- March 2026 remediation-program summary for the final bounded modularity follow-up.
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/repo_local_hotspot_modularity_hardening.md)
- [core_export_hardening_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_hardening_execution.md)
- [end_to_end_repo_rationalization_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/end_to_end_repo_rationalization_execution.md)
