---
trace_id: trace.typed_query_surface_modularity_hardening
id: design.implementation.typed_query_surface_modularity_hardening
title: Typed Query Surface Modularity Hardening Implementation Plan
summary: Breaks Typed Query Surface Modularity Hardening into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T18:24:59Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/control_plane/models/
- core/python/src/watchtower_core/control_plane/loader.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/validation/acceptance.py
- core/python/tests/unit/
- core/python/src/watchtower_core/control_plane/README.md
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
---

# Typed Query Surface Modularity Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.typed_query_surface_modularity_hardening`
- `Plan ID`: `design.implementation.typed_query_surface_modularity_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.typed_query_surface_modularity_hardening`
- `Linked Decisions`: `decision.typed_query_surface_modularity_hardening_direction`
- `Source Designs`: `design.features.typed_query_surface_modularity_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.typed_query_surface_modularity_hardening`
- `Updated At`: `2026-03-13T18:24:59Z`

## Summary
Breaks Typed Query Surface Modularity Hardening into a bounded implementation slice.

## Source Request or Design
- Review the March 13, 2026 refactor audit under one stable typed-retrieval theme until repeated confirmation passes find no new actionable issue.
- Feature design: [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/typed_query_surface_modularity_hardening.md)
- PRD: [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/typed_query_surface_modularity_hardening.md)
- Decision: [typed_query_surface_modularity_hardening_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/typed_query_surface_modularity_hardening_direction.md)

## Scope Summary
- Refactor the typed planning and documentation retrieval models into smaller domain-focused modules with explicit shared helpers and preserve the stable public import and loader boundary.
- Split the oversized CLI query regression hotspot into narrower suites with shared helpers while preserving real command coverage and JSON assertions.
- Keep adjacent loader or query consumers, runtime-boundary docs, planning trackers, acceptance contract, evidence ledger, and closeout surfaces aligned inside the same trace.
- Leave command-surface redesign, workflow-lattice cleanup, and unrelated giant validation suites out of scope unless the confirmation loop finds a direct same-theme issue.

## Assumptions and Constraints
- Public import names from `watchtower_core.control_plane.models` and the current `ControlPlaneLoader.load_*` contracts must remain stable.
- No control-plane JSON schema, machine-readable index shape, or CLI argument contract changes are expected in this slice.
- Real command execution, real loader calls, and full-repo validation remain required; shallow helper-only coverage is not acceptable.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): constrains package-boundary updates and requires runtime-boundary docs to stay aligned.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): traced implementation work needs bounded durable tasks and aligned derived trackers.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): constrains the task set and closeout placement used during the loop.
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md): task lifecycle changes must keep the machine-readable companion surface aligned.

## Proposed Technical Approach
- Introduce one small shared helper module under `watchtower_core.control_plane.models` for repeated tuple coercion, index artifact materialization, and identifier lookups that keeps the behavior explicit and inspectable.
- Split the current `planning.py` hotspot into focused modules that separate planning-document index models from reference or foundation or standard or workflow index models while preserving the stable re-export surface in `models/__init__.py`.
- Update direct loader, query, sync, validation, and test consumers only where internal implementation paths changed; do not widen the public surface or change behavior.
- Replace the single `test_cli_query_commands.py` hotspot with narrower suites plus one helper that still runs `watchtower_core.cli.main.main(...)` and parses real JSON output, while keeping a tiny compatibility marker for historical path references.
- Refresh the runtime-boundary docs and the traced planning or acceptance or evidence surfaces only where the refactor materially changes the documented hotspot boundary.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Typed model hotspot | `core/python/src/watchtower_core/control_plane/models/planning.py`; new helper-backed model modules under `core/python/src/watchtower_core/control_plane/models/`; `core/python/src/watchtower_core/control_plane/models/__init__.py` | Domain separation, explicit dataclass contracts, repeated materialization and lookup seams, stable public exports |
| Loader and direct consumers | `core/python/src/watchtower_core/control_plane/loader.py`; `core/python/src/watchtower_core/repo_ops/query/`; `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py`; `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`; `core/python/src/watchtower_core/validation/acceptance.py` | Import stability, typed return contracts, no query or sync behavior drift |
| CLI query regression hotspot | `core/python/tests/unit/test_cli_query_commands.py`; replacement focused CLI suites; shared command or JSON helper module | Failure locality, coverage preservation, real command execution, repeated assertion cleanup, and historical path compatibility |
| Runtime boundaries and docs | `core/python/src/watchtower_core/control_plane/README.md`; any touched package map docs under `core/python/` | Boundary clarity after the split, no stale implementation-path guidance |
| Traced planning and governance surfaces | `docs/planning/**`; `core/control_plane/contracts/acceptance/typed_query_surface_modularity_hardening_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/typed_query_surface_modularity_hardening_planning_baseline.v1.json` | Coverage map durability, findings ledger, acceptance alignment, evidence coverage, task closeout |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.typed_query_surface_modularity_hardening.001` | `medium` | `resolved` | `core/python/src/watchtower_core/control_plane/models/planning.py`; `core/python/src/watchtower_core/control_plane/models/__init__.py`; typed loader and query consumers | the old 548-line mixed-domain hotspot is now a 37-line compatibility re-export over focused model modules plus a 48-line helper, and targeted model or loader regressions passed |
| `finding.typed_query_surface_modularity_hardening.002` | `medium` | `resolved` | `core/python/tests/unit/test_cli_query_commands.py`; CLI query or route-preview or dry-run command coverage | the old 912-line mixed-family regression hotspot is now a focused suite family plus a small helper and compatibility marker, and the targeted CLI family suite passed with real-command assertions intact |
| `finding.typed_query_surface_modularity_hardening.003` | `medium` | `resolved` | historical closed task docs referencing `core/python/tests/unit/test_cli_query_commands.py`; repository path index; task-create dry-run validation surface | the first dry-run adversarial probe exposed stale historical `applies_to` references after the suite split; broadening those legacy task paths to `core/python/tests/unit/` plus keeping the compatibility marker restored deterministic dry-run task creation and clean full validation |
| `finding.typed_query_surface_modularity_hardening.004` | `medium` | `resolved` | `core/control_plane/contracts/acceptance/typed_query_surface_modularity_hardening_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/typed_query_surface_modularity_hardening_planning_baseline.v1.json`; full acceptance-aware validation surfaces | the first acceptance-aware full validation failed on missing evidence coverage for acceptance IDs `002` through `005`; the loop reopened to expand the evidence ledger, and the final `validate all`, `validate acceptance`, and `pytest -q` reruns passed |

## Work Breakdown
1. Replace the planning, decision, acceptance, evidence, and bootstrap-task placeholders with the real typed-retrieval scope, coverage map, findings ledger, decision, and bounded execution-task set.
2. Complete `task.typed_query_surface_modularity_hardening.model_modularity.002` by splitting the typed retrieval models into focused modules plus explicit shared helpers and aligning all direct consumers with stable exports.
3. Complete `task.typed_query_surface_modularity_hardening.query_suite_modularity.003` by replacing the single CLI query hotspot with narrower suites plus shared helpers and a compatibility marker, then align any touched runtime-boundary docs and loader regressions.
4. Complete `task.typed_query_surface_modularity_hardening.validation_closeout.004` by running targeted validation, full validation, post-fix review, second-angle confirmation, adversarial confirmation, evidence refresh, and initiative closeout.

## Risks
- Internal helper design could drift toward clever abstraction and reduce inspectability.
- Import churn across loader, query, sync, validation, and tests could leave one consumer behind.
- The adversarial pass may expose an adjacent loader or query edge case that reopens the loop before closeout.

## Validation Plan
- Run targeted pytest coverage for the new typed-model seams, direct loader regressions, and replacement CLI query suites while the refactor lands.
- Run `./.venv/bin/watchtower-core sync all --write --format json` after the planning and governed-surface edits are in place.
- Run full repository validation with `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/ruff check .`, and `./.venv/bin/python -m mypy src/watchtower_core`.
- Re-run the retrieval boundary from a fresh post-fix angle, then perform a second independent no-new-issues review, then an adversarial confirmation pass that tries to falsify the claim that the typed retrieval surface is now clean.
- Refresh the acceptance contract, planning-baseline evidence, planning trackers, indexes, and closeout metadata only after the final clean-state evidence is in hand.

## References
- March 13, 2026 refactor audit
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/typed_query_surface_modularity_hardening.md)
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/typed_query_surface_modularity_hardening.md)
