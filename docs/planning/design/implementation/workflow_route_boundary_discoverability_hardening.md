---
trace_id: trace.workflow_route_boundary_discoverability_hardening
id: design.implementation.workflow_route_boundary_discoverability_hardening
title: Workflow Route Boundary Discoverability Hardening Implementation Plan
summary: Breaks Workflow Route Boundary Discoverability Hardening into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T21:40:13Z'
audience: shared
authority: supporting
applies_to:
- workflows/ROUTING_TABLE.md
- workflows/modules/
- core/python/src/watchtower_core/repo_ops/query/routes.py
- core/python/src/watchtower_core/repo_ops/query/workflows.py
- core/control_plane/registries/workflows/
- core/control_plane/indexes/routes/
- core/control_plane/indexes/workflows/
- docs/commands/core_python/
---

# Workflow Route Boundary Discoverability Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.workflow_route_boundary_discoverability_hardening`
- `Plan ID`: `design.implementation.workflow_route_boundary_discoverability_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.workflow_route_boundary_discoverability_hardening`
- `Linked Decisions`: `decision.workflow_route_boundary_discoverability_hardening_direction`
- `Source Designs`: `design.features.workflow_route_boundary_discoverability_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.workflow_route_boundary_discoverability_hardening`
- `Updated At`: `2026-03-13T21:40:13Z`

## Summary
Breaks Workflow Route Boundary Discoverability Hardening into a bounded implementation slice.

## Source Request or Design
- Do another comprehensive internal project review for refactor under one stable workflow-boundary theme until no new actionable issues remain.
- Address the remaining workflow discoverability and route-boundary drift identified by the March 13, 2026 refactor audit.

## Scope Summary
- Route-preview scoring and selection behavior in `core/python/src/watchtower_core/repo_ops/query/routes.py`.
- Workflow lookup discoverability in `core/python/src/watchtower_core/repo_ops/query/workflows.py` plus the authored workflow metadata or derived workflow index surfaces that support it.
- Authored route examples, workflow metadata trigger tags, command docs, targeted tests, and companion route or workflow indexes.
- Exclude workflow-family consolidation, unrelated query-service rewrites, and any schema changes that are not directly required by this workflow-boundary slice.

## Assumptions and Constraints
- Explicit `--task-type` route-preview behavior is already correct and should remain unchanged.
- The workflow family should stay explicit and advisory; the fix should sharpen routing and lookup behavior rather than introduce a new source of procedural authority.
- The workflow metadata registry and route table should remain the authored source for retrieval cues, with the route and workflow indexes staying derived.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): constrains the route-preview behavior to stay deterministic and to use full prompt context rather than exact keyword matching alone.
- [route_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/route_index_standard.md): requires the route index to stay derived from the authored routing table and aligned in the same change set.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): constrains how workflow retrieval metadata and trigger tags should appear in the derived workflow index.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): preserves the distinct module boundaries that the discoverability fix must support rather than collapse.

## Proposed Technical Approach
- Add lightweight token canonicalization and near-complete multi-token keyword matching to the route-preview scorer so realistic adjacent-route prompts can match without verbatim routing-table phrases.
- Filter free-form route-preview results to drop low-signal secondary matches that are materially weaker than the dominant route while preserving intentionally composite prompts.
- Expand the authored routing-table examples and workflow metadata trigger tags for the adjacent reconciliation and task workflows so the machine lookup surfaces publish better retrieval cues.
- Refresh `watchtower-core route preview` and `watchtower-core query workflows` docs plus focused unit tests to prove the same adjacent-route distinctions through both lookup surfaces.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Route preview runtime | `core/python/src/watchtower_core/repo_ops/query/routes.py`; `core/python/src/watchtower_core/cli/route_handlers.py` | token normalization, realistic prompt matching, dominant-route filtering, advisory warnings |
| Workflow lookup runtime | `core/python/src/watchtower_core/repo_ops/query/workflows.py`; `core/python/src/watchtower_core/repo_ops/query/common.py` | realistic workflow discovery, trigger-tag use, bounded search behavior |
| Authored route guidance | `workflows/ROUTING_TABLE.md`; `workflows/modules/documentation_implementation_reconciliation.md`; `workflows/modules/governed_artifact_reconciliation.md`; `workflows/modules/traceability_reconciliation.md`; `workflows/modules/task_lifecycle_management.md`; `workflows/modules/task_phase_transition.md` | adjacent-route discrimination, realistic example phrasing, preserved workflow boundaries |
| Governed workflow metadata | `core/control_plane/registries/workflows/workflow_metadata_registry.v1.json`; `core/control_plane/indexes/routes/route_index.v1.json`; `core/control_plane/indexes/workflows/workflow_index.v1.json` | trigger-term publication, derived-index alignment, same-change sync integrity |
| Companion docs and query entrypoints | `docs/commands/core_python/watchtower_core_route_preview.md`; `docs/commands/core_python/watchtower_core_query_workflows.md` | adjacent-route guidance, realistic examples, route-vs-query lookup usage |
| Regression and validation surfaces | `core/python/tests/unit/test_cli_route_and_path_commands.py`; `core/python/tests/unit/test_cli_knowledge_query_commands.py`; `core/python/tests/unit/test_route_index_sync.py`; `core/python/tests/unit/test_workflow_index_sync.py` | realistic reconciliation prompts, handoff leakage regression, workflow-query discoverability, derived-surface sync coverage |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.workflow_route_boundary_discoverability_hardening.001` | `high` | `resolved` | `core/python/src/watchtower_core/repo_ops/query/routes.py`; `workflows/ROUTING_TABLE.md`; `core/control_plane/indexes/routes/route_index.v1.json` | `route preview --request "reconcile command docs with current cli behavior" --format json` now returns only `Documentation-Implementation Reconciliation`, and `route preview --request "reconcile schema-backed indexes examples and validators for one artifact family" --format json` now returns only `Governed Artifact Reconciliation` |
| `finding.workflow_route_boundary_discoverability_hardening.002` | `medium` | `resolved` | `core/python/src/watchtower_core/repo_ops/query/routes.py`; `core/python/src/watchtower_core/cli/route_handlers.py`; `workflows/ROUTING_TABLE.md`; `docs/commands/core_python/watchtower_core_route_preview.md` | the adversarial successor-task prompts `move task to validation and create successor tasks` and `hand off this task from implementation to validation and create successor tasks` now return only `Task Phase Transition`, while `Code Validation` and `Task Lifecycle Management` no longer leak into the result set |
| `finding.workflow_route_boundary_discoverability_hardening.003` | `medium` | `resolved` | `core/control_plane/registries/workflows/workflow_metadata_registry.v1.json`; `core/control_plane/indexes/workflows/workflow_index.v1.json`; `docs/commands/core_python/watchtower_core_query_workflows.md` | `query workflows --query "current cli behavior" --format json` now resolves `workflow.documentation_implementation_reconciliation`, and `query workflows --query "successor tasks" --format json` now resolves `workflow.task_phase_transition` |
| `finding.workflow_route_boundary_discoverability_hardening.004` | `medium` | `resolved` | `core/control_plane/contracts/acceptance/workflow_route_boundary_discoverability_hardening_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/workflow_route_boundary_discoverability_hardening_planning_baseline.v1.json`; `docs/planning/tasks/closed/validate_and_close_workflow_route_boundary_discoverability_hardening.md` | the acceptance contract and planning-baseline evidence ledger were expanded from the bootstrap-only state to cover all five PRD acceptance IDs before the final acceptance-aware validation loop |

## Work Breakdown
1. Replace the planning placeholders with the bounded workflow-boundary coverage map, confirmed findings ledger, accepted direction, and concrete execution tasks.
2. Implement the route-preview scorer and workflow-lookup hardening, then refresh authored route examples, workflow metadata, derived indexes, command docs, and focused regressions in the same change set.
3. Run targeted validation, full validation, post-fix review, second-angle confirmation, adversarial confirmation, evidence refresh, initiative closeout, and commit closeout.

## Risks
- A too-loose scorer could widen route ambiguity instead of reducing it.
- Updating only route preview without strengthening workflow-query discoverability would leave the adjacent workflow boundaries under-documented for manual lookup.

## Validation Plan
- Run focused route-preview, workflow-query, route-index, and workflow-index unit suites covering realistic reconciliation prompts, handoff prompts, and derived trigger metadata.
- Probe live `watchtower-core route preview` and `watchtower-core query workflows` behavior in JSON mode with realistic adjacent-route prompts before and after the fix.
- Run `watchtower-core validate acceptance --trace-id trace.workflow_route_boundary_discoverability_hardening --format json`, `watchtower-core validate all --format json`, `pytest -q`, `ruff check .`, and `python -m mypy src/watchtower_core`.
- Re-review the touched workflow modules, route/index artifacts, command docs, and direct consumers from a second angle, then run an adversarial confirmation pass that tries to reintroduce no-match reconciliation prompts and low-signal validation leakage.

## References
- March 13, 2026 refactor audit
- [workflow_route_boundary_discoverability_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_route_boundary_discoverability_hardening.md)
- [workflow_route_boundary_discoverability_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_route_boundary_discoverability_hardening.md)
