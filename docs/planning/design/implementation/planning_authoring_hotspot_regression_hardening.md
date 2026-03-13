---
trace_id: trace.planning_authoring_hotspot_regression_hardening
id: design.implementation.planning_authoring_hotspot_regression_hardening
title: Planning Authoring Hotspot Regression Hardening Implementation Plan
summary: Breaks Planning Authoring Hotspot Regression Hardening into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T17:44:44Z'
audience: shared
authority: supporting
---

# Planning Authoring Hotspot Regression Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.planning_authoring_hotspot_regression_hardening`
- `Plan ID`: `design.implementation.planning_authoring_hotspot_regression_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.planning_authoring_hotspot_regression_hardening`
- `Linked Decisions`: `decision.planning_authoring_hotspot_regression_hardening_direction`
- `Source Designs`: `design.features.planning_authoring_hotspot_regression_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.planning_authoring_hotspot_regression_hardening`
- `Updated At`: `2026-03-13T17:44:44Z`

## Summary
Breaks Planning Authoring Hotspot Regression Hardening into a bounded implementation slice.

## Source Request or Design
- Review the March 13, 2026 refactor audit and keep reviewing under one stable planning-authoring hotspot theme until repeated confirmation passes find no new actionable issue.
- Feature design: [planning_authoring_hotspot_regression_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/planning_authoring_hotspot_regression_hardening.md)
- PRD: [planning_authoring_hotspot_regression_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authoring_hotspot_regression_hardening.md)
- Decision: [planning_authoring_hotspot_regression_hardening_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/planning_authoring_hotspot_regression_hardening_direction.md)

## Scope Summary
- Recover smaller helper-backed seams around planning scaffolds and task lifecycle mutation where the hotspot regrew after the earlier modularity trace.
- Cover code, docs, tests, trackers, indexes, acceptance or evidence surfaces, and adjacent runtime-boundary docs relevant to that hotspot.
- Leave unrelated sync CLI, traceability-sync, and GitHub hotspot surfaces untouched unless the review loop finds a new same-theme dependency that must move with this slice.

## Assumptions and Constraints
- Top-level command behavior and governed artifact shapes must remain stable.
- The refactor must preserve deterministic coordination refresh and fail-closed validation under both dry-run and write paths.
- The earlier hotspot-modularity trace remains historical context and should not be retroactively rewritten to mask later regrowth.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task moves must keep governed acceptance and validation-evidence references aligned.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): task record placement and required sections stay stable.
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md): PRD scaffolds must keep the current metadata and acceptance contract shape.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): feature-design scaffolds must preserve required explained-source sections.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): implementation-plan scaffolds must preserve required source and validation sections.
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md): decision scaffolds must preserve decision-status and applied-reference structure.

## Proposed Technical Approach
- Extract scaffold-kind specs into a declarative helper so plan-kind contract changes stop relying on several parallel maps in one file.
- Extract scaffold rendering and rendered-document validation into focused helper-backed seams so `planning_scaffolds.py` becomes a smaller orchestration layer.
- Extract bootstrap acceptance-contract or validation-evidence builders and planning-surface refresh helpers out of `planning_scaffolds.py`.
- Extract governed task companion-path repair into a dedicated helper-backed collaborator so `task_lifecycle.py` no longer owns acceptance-contract and validation-evidence traversal directly.
- Refresh only the docs and runtime-boundary surfaces that materially describe the hotspot seam; leave operator-facing command behavior docs untouched unless their behavior description actually changes.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Planning scaffold service | `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`; new helper-backed scaffold modules under `core/python/src/watchtower_core/repo_ops/` | Orchestration readability, bootstrap artifact generation, planning-surface refresh isolation, stable result payloads |
| Scaffold contracts and rendering | `core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py`; any new scaffold spec or rendering helpers; planning document standards under `docs/standards/documentation/` | Declarative plan-kind contracts, render-path drift risk, section and metadata stability |
| Task lifecycle mutation | `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`; `core/python/src/watchtower_core/repo_ops/task_lifecycle_support.py`; new task companion repair helper | Stable task mutation behavior, isolated governed companion repair, path-canonicalization preservation |
| Command and runtime boundaries | `core/python/src/watchtower_core/cli/plan_handlers.py`; `core/python/src/watchtower_core/cli/task_handlers.py`; [watchtower_core_plan.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_plan.md); [watchtower_core_task.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_task.md); `core/python/src/watchtower_core/repo_ops/README.md` | Behavior drift, source-surface clarity, same-change doc alignment |
| Governed planning companions | `docs/planning/**`; `core/control_plane/contracts/acceptance/planning_authoring_hotspot_regression_hardening_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/planning_authoring_hotspot_regression_hardening_planning_baseline.v1.json`; planning trackers and indexes | Traceability alignment, task-path references, closeout evidence, tracker or index coherence |
| Regression coverage and validation | `core/python/tests/unit/test_planning_scaffolds.py`; `core/python/tests/integration/test_planning_scaffolds_service.py`; `core/python/tests/unit/test_task_lifecycle.py`; `core/python/tests/integration/test_task_lifecycle_service.py`; `core/python/tests/unit/test_plan_and_task_handlers.py` | Behavior preservation, adjacent dependency coverage, confirmation-pass probes |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.planning_authoring_hotspot_regression_hardening.001` | `high` | `resolved` | `planning_scaffolds.py`; `planning_bootstrap_support.py`; bootstrap acceptance or evidence write path; planning-surface refresh path | the service entrypoint is now `308` lines, while bootstrap artifact builders and refresh logic moved into focused helpers; targeted scaffold or handler suites and `ruff check` passed |
| `finding.planning_authoring_hotspot_regression_hardening.002` | `high` | `resolved` | `task_lifecycle.py`; `task_companion_path_repair.py`; acceptance contracts; validation evidence ledgers | `task_lifecycle.py` is now `492` lines and governed companion traversal lives in `task_companion_path_repair.py`; targeted lifecycle suites and the new helper regression test passed |
| `finding.planning_authoring_hotspot_regression_hardening.003` | `medium` | `resolved` | `planning_scaffold_support.py`; `planning_scaffold_specs.py`; planning document standards; scaffold tests | `planning_scaffold_support.py` is now `249` lines, plan-kind metadata lives in declarative scaffold specs, and the new spec-alignment test locks the scaffold contracts to planning-document requirements |
| `finding.planning_authoring_hotspot_regression_hardening.004` | `medium` | `resolved` | acceptance contract or validation evidence surfaces; `validate all`; `test_all_validation.py` | the first acceptance-aware full validation failed with `acceptance_ids_missing_evidence_coverage` for acceptance IDs `002` through `005`; the loop reopened to refresh durable evidence coverage, and the final `validate all`, `validate acceptance`, and `pytest -q` reruns all passed |

## Work Breakdown
1. Replace the planning scaffolds, decision, acceptance contract, evidence stub, and bootstrap task placeholders with the real hotspot-regression scope, accepted direction, coverage map, findings ledger, and bounded execution-task set.
2. Complete `task.planning_authoring_hotspot_regression_hardening.scaffold_modularity.002` by extracting declarative scaffold specs, helper-backed rendering, bootstrap artifact builders, and planning-surface refresh seams while preserving current plan command behavior.
3. Complete `task.planning_authoring_hotspot_regression_hardening.task_companion_repair.003` by isolating governed task companion-path repair from `TaskLifecycleService`, then align adjacent runtime-boundary docs and regression suites.
4. Complete `task.planning_authoring_hotspot_regression_hardening.validation_closeout.004` by running targeted validation, full validation, post-fix review, second-angle review, adversarial confirmation, evidence refresh, task closeout, and initiative closeout.

## Risks
- Moving too much logic out of the current services could obscure the write path.
- A helper split that misses loader cache override behavior could break companion-path repair or post-write validation.
- The command docs could drift if they start describing internal helper modules instead of the stable user-facing behavior.

## Validation Plan
- Run targeted pytest coverage for planning scaffolds, plan or task handlers, task lifecycle, and the matching integration suites while the refactor lands.
- Run `./.venv/bin/watchtower-core sync all --write --format json` after the planning and governed-surface edits are in place.
- Run full repository validation with `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/ruff check .`, and `./.venv/bin/python -m mypy src/watchtower_core`.
- Re-run the hotspot boundary from a fresh post-fix angle, then perform a second independent no-new-issues review, then an adversarial confirmation pass that tries to falsify the claim that planning authoring is now clean.
- Refresh the acceptance contract, planning-baseline evidence, planning trackers, indexes, and closeout metadata only after the final clean-state evidence is in hand.

## References
- March 13, 2026 refactor audit
- [planning_authoring_hotspot_regression_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authoring_hotspot_regression_hardening.md)
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/repo_local_hotspot_modularity_hardening.md)
