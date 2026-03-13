---
trace_id: trace.refactor_review_and_hardening
id: design.implementation.refactor_review_and_hardening
title: Refactor Review and Hardening Implementation Plan
summary: Breaks the phase-one refactor slice into workflow-route discrimination,
  compact coordination payloads, route-first entrypoint updates, and closeout.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T15:00:41Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/references/
- docs/standards/
- workflows/
---

# Refactor Review and Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.refactor_review_and_hardening`
- `Plan ID`: `design.implementation.refactor_review_and_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.refactor_review_and_hardening`
- `Linked Decisions`: `decision.refactor_review_and_hardening_direction`
- `Source Designs`: `design.features.refactor_review_and_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.refactor_review_and_hardening`
- `Updated At`: `2026-03-13T15:00:41Z`

## Summary
Breaks the phase-one refactor slice into workflow-route discrimination, compact coordination payloads, route-first entrypoint updates, and closeout.

## Source Request or Design
- Feature design: [refactor_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/refactor_review_and_hardening.md)
- PRD: [refactor_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/refactor_review_and_hardening.md)
- Decision: [refactor_review_and_hardening_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/refactor_review_and_hardening_direction.md)

## Scope Summary
- Complete the audit's phase-one current-state simplification slice plus the workflow-route prerequisite.
- Land the existing workflow-route discrimination change under traced control, then slim the coordination payload and thin route-first planning and command entrypoints.
- Refresh derived routing, planning, and coordination surfaces, validate the repository, and close the initiative only after repeated confirmation passes stay clean.
- Exclude deeper repo-local hotspot decomposition, reference-lifecycle grouping, placeholder-family cleanup, and policy-cost review from this trace.

## Assumptions and Constraints
- The current dirty workflow-routing worktree belongs to the bounded route-discrimination slice and should be completed or replaced deliberately instead of left as untracked drift.
- Coordination current-state compaction must preserve explicit terminal-status lookup behavior even if the default coordination artifact stops carrying full closed-history entries.
- Entry-point thinning should remove low-value duplication, not the most useful help, index, or leaf-document routes.
- The broader refactor audit remains comparative input; this trace should record only the local phase-one conclusions and follow-up boundaries needed to execute safely.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): route-discrimination changes must stay aligned across routing prose, route-preview metadata, and workflow-module boundaries.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): the coordination artifact must remain a compact current-state start-here surface.
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/coordination_tracking_standard.md): the human coordination tracker should mirror the compact coordination contract rather than regrow family-detail duplication.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): umbrella command docs remain command references and should route readers to leaf docs and live help.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): deeper initiative-family views remain valid deeper routes after the planning-root entrypoint is thinned.

## Proposed Technical Approach
- Finish the existing workflow-route discrimination slice, keeping the new documentation-review route and adjacent workflow distinctions aligned across the routing table, workflow metadata registry, workflow index, route index, route-preview docs, and targeted tests.
- Slim `CoordinationIndexSyncService` so the default coordination artifact carries only active initiative entries plus recent-closeout summaries, then adjust coordination-query behavior so explicit terminal-status filters still resolve through initiative-family data without default closed-history duplication.
- Rewrite the planning and command umbrella entrypoints to route readers to coordination, CLI help, command indexes, and leaf docs with the smallest useful example set.
- Keep the standards, examples, indexes, query behavior, trackers, and tests synchronized in the same change sets as their governing surfaces.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Workflow routing | `workflows/ROUTING_TABLE.md`; `workflows/modules/README.md`; `workflows/modules/documentation_review.md`; `workflows/modules/documentation_refresh.md`; `workflows/modules/repository_review.md`; `workflows/modules/task_handoff_review.md`; `core/control_plane/indexes/routes/route_index.v1.json`; `core/control_plane/indexes/workflows/workflow_index.v1.json`; `core/control_plane/registries/workflows/workflow_metadata_registry.v1.json`; `docs/commands/core_python/watchtower_core_route_preview.md`; `core/python/tests/unit/test_route_index_sync.py`; `core/python/tests/unit/test_workflow_index_sync.py` | Route discrimination, metadata alignment, route-preview behavior, and regression coverage |
| Coordination current-state | `core/python/src/watchtower_core/repo_ops/sync/coordination_index.py`; `core/python/src/watchtower_core/repo_ops/query/coordination.py`; `core/python/src/watchtower_core/cli/query_coordination_handlers.py`; `core/python/src/watchtower_core/repo_ops/sync/coordination_tracking.py`; `core/control_plane/indexes/coordination/coordination_index.v1.json`; coordination schema and examples; coordination-related tests; coordination standards | Current-state compactness, explicit terminal lookup behavior, query and tracker alignment |
| Planning entrypoints | `docs/planning/README.md`; `docs/planning/initiatives/README.md`; `docs/planning/coordination_tracking.md`; initiative and coordination standards | Start-here routing, current-state versus deeper-history guidance, artifact-status clarity |
| Command entrypoints | `docs/commands/core_python/watchtower_core.md`; `docs/commands/core_python/watchtower_core_query.md`; `docs/commands/core_python/watchtower_core_sync.md`; `core/python/README.md`; command standards; CLI help behavior | Route-first umbrella docs, low-value catalog removal, leaf-doc and help alignment |
| Trace closeout surfaces | `docs/planning/tasks/`; `docs/planning/coordination_tracking.md`; `docs/planning/initiatives/initiative_tracking.md`; `docs/planning/prds/prd_tracking.md`; `docs/planning/design/design_tracking.md`; `docs/planning/decisions/decision_tracking.md`; `core/control_plane/contracts/acceptance/refactor_review_and_hardening_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/refactor_review_and_hardening_planning_baseline.v1.json` | Bounded task chain, acceptance alignment, evidence refresh, and closeout readiness |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.refactor_review_and_hardening.001` | `high` | `resolved` | workflow routing family, route preview docs, route and workflow indexes, workflow metadata registry, targeted route-preview tests | audit finding `RF-WKF-001`, targeted route and workflow pytest (`66 passed` in the focused validation set), and live route-preview probes now confirm that bounded documentation and standards reviews select the dedicated documentation-review route |
| `finding.refactor_review_and_hardening.002` | `high` | `resolved` | coordination sync and query paths, coordination index, coordination tracker, coordination standards, coordination tests | audit finding `RF-CTL-001`, live coordination artifact inspection after sync all (`record_count: 1`), targeted coordination pytest, and explicit completed-query probes now confirm that the default coordination payload is compact while historical lookup still resolves through initiative-family data |
| `finding.refactor_review_and_hardening.003` | `medium` | `resolved` | root and group command pages, command-family guidance, command docs standards | audit finding `RF-CMD-001`, rewritten umbrella command pages, command-index refresh, and post-fix command-query inspection now confirm that the root, query, and sync entrypoints are route-first instead of handbook-style catalogs |
| `finding.refactor_review_and_hardening.004` | `medium` | `resolved` | planning root and initiative-family READMEs, coordination tracker, initiative tracking semantics | audit findings `RF-PLN-002` and `RF-PLN-003`, refreshed planning entrypoints, coordination-tracker review, and initiative-history query probes now confirm clearer active-current-state versus deeper-history routing |
| `finding.refactor_review_and_hardening.005` | `high` | `resolved` | acceptance contract, validation evidence ledger, validation-closeout task, full validation stack | full `watchtower-core validate all --format json` and full `pytest -q` reopened the loop on one actionable evidence-coverage gap, the evidence ledger was expanded inside the same trace, `watchtower-core validate acceptance --trace-id trace.refactor_review_and_hardening --format json` now passes with `issue_count: 0`, and final planning or evidence queries confirm that all acceptance IDs carry durable passed evidence |
| `finding.refactor_review_and_hardening.006` | `medium` | `resolved` | `core/python/tests/unit/test_coordination_tracking_sync.py`, coordination current-state validation coverage, closed-state pytest baseline | the first adversarial full `pytest -q` after initiative closeout exposed a real regression in test assumptions because the compact coordination slice can legitimately have zero active entries after closeout; the test now synthesizes a valid active-entry fixture when `entries` is empty, targeted coordination reruns passed, and the second full `pytest -q` passed cleanly |

## Work Breakdown
1. Close the bootstrap phase by replacing scaffold placeholders with the real phase-one scope, coverage map, findings ledger, accepted direction, and bounded execution tasks.
2. Complete `task.refactor_review_and_hardening.workflow_route_discrimination.002` by finishing the interrupted workflow-route discrimination slice and aligning its docs, indexes, registry metadata, and targeted regressions.
3. Complete `task.refactor_review_and_hardening.current_state_surface_simplification.003` by slimming default coordination payloads and thinning route-first planning and command entrypoints with aligned standards, examples, trackers, and tests.
4. Complete `task.refactor_review_and_hardening.validation_closeout.004` by running targeted validation, full repository validation, post-fix review, second-angle review, adversarial confirmation, and final trace closeout.

## Risks
- Coordination-query compatibility is the main code risk because the default artifact compaction changes how terminal-status lookups are served even if the user-facing command still supports them.
- Route-first doc thinning can regress discoverability if the replacement routing notes are too sparse or if the documents stop pointing to the right deeper surfaces.
- A second review angle may reveal adjacent workflow or coordination drift after the first fixes land, requiring the same trace loop to reopen before closeout.

## Validation Plan
- Run targeted tests for route preview, route and workflow index sync, coordination index sync, coordination tracking sync, route/query handlers, and any command-doc or artifact contract checks touched by the slice.
- Run `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check .` after the implementation tasks land.
- Re-run the bounded phase-one refactor review from a fresh angle, then run an adversarial confirmation pass whose job is to find missed adjacent route, coordination, or entrypoint drift.
- Refresh the acceptance contract, validation evidence, task state, and initiative closeout surfaces with the final clean-state evidence before committing.

## References
- March 2026 refactor audit
