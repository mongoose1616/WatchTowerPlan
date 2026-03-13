---
trace_id: trace.validation_test_hotspot_rebalancing
id: design.implementation.validation_test_hotspot_rebalancing
title: Validation Test Hotspot Rebalancing Implementation Plan
summary: Breaks Validation Test Hotspot Rebalancing into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T19:19:06Z'
audience: shared
authority: supporting
applies_to:
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/cli/validation_handlers.py
- docs/commands/core_python/
- docs/planning/
---

# Validation Test Hotspot Rebalancing Implementation Plan

## Record Metadata
- `Trace ID`: `trace.validation_test_hotspot_rebalancing`
- `Plan ID`: `design.implementation.validation_test_hotspot_rebalancing`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.validation_test_hotspot_rebalancing`
- `Linked Decisions`: `decision.validation_test_hotspot_rebalancing_direction`
- `Source Designs`: `design.features.validation_test_hotspot_rebalancing`
- `Linked Acceptance Contracts`: `contract.acceptance.validation_test_hotspot_rebalancing`
- `Updated At`: `2026-03-13T19:19:06Z`

## Summary
Breaks Validation Test Hotspot Rebalancing into a bounded implementation slice.

## Source Request or Design
- Review the March 13, 2026 refactor audit under one stable validation-hotspot theme until repeated confirmation passes find no new actionable issue.
- Feature design: [validation_test_hotspot_rebalancing.md](/home/j/WatchTowerPlan/docs/planning/design/features/validation_test_hotspot_rebalancing.md)
- PRD: [validation_test_hotspot_rebalancing.md](/home/j/WatchTowerPlan/docs/planning/prds/validation_test_hotspot_rebalancing.md)
- Decision: [validation_test_hotspot_rebalancing_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/validation_test_hotspot_rebalancing_direction.md)

## Scope Summary
- Split the remaining oversized integration and unit validation suites into focused family-oriented files backed by small shared helpers.
- Preserve direct validation-service, loader, and command behavior while refreshing README inventories, repository-path indexing, and compatibility markers for the historical hotspot paths.
- Keep acceptance, evidence, task, tracker, and index surfaces aligned with the split through closeout.
- Exclude validator-registry redesign, schema changes, command-surface redesign, and unrelated test families unless the confirmation loop finds a direct same-theme dependency.

## Assumptions and Constraints
- The final suite layout must preserve the same live repository-aware assertions and fail-closed validation behavior that the current hotspot files provide.
- Historical file paths for the two hotspot suites should remain resolvable to avoid reopening widespread planning-path drift.
- README inventories are the authoritative source for repository-path indexing, so discoverability changes must ship in the same change set as the split.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): constrains test layout and same-change documentation alignment in the Python workspace.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): README inventories must remain honest, scoped entrypoints for the touched test families.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): repository-path indexing must stay aligned with README inventory changes.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): traced implementation work needs bounded task records and aligned trackers.

## Proposed Technical Approach
- Introduce one small helper module under `core/python/tests/integration/` for repeated JSON or front-matter loading and related repository-aware assertions, then split `test_control_plane_artifacts.py` into focused integration suites by validation family while keeping the original path as a compatibility marker.
- Introduce one small fixture-writer helper under `core/python/tests/unit/` for repeated document-semantics fixtures, then split `test_document_semantics_validation.py` into focused unit suites by semantic rule family while keeping the original path as a compatibility marker.
- Refresh `core/python/tests/unit/README.md` and `core/python/tests/integration/README.md` so `watchtower-core query paths` and the repository-path index expose the new layout and the preserved compatibility-marker paths.
- Update only the planning, acceptance, evidence, tracker, and index surfaces needed to describe and validate the new suite layout; keep validation runtime code unchanged unless the review loop proves a direct same-theme defect.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Integration validation hotspot | `core/python/tests/integration/test_control_plane_artifacts.py`; new helper-backed integration suites under `core/python/tests/integration/`; `core/python/src/watchtower_core/control_plane/loader.py`; `core/python/src/watchtower_core/validation/artifact.py`; example-artifact helpers | Failure locality, live loader or schema coverage preservation, helper minimalism, compatibility-path strategy |
| Document-semantics hotspot | `core/python/tests/unit/test_document_semantics_validation.py`; new fixture-backed unit suites under `core/python/tests/unit/`; `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`; `core/python/src/watchtower_core/validation/document_semantics.py` | Validator-selection coverage, explicit fixture writing, fail-closed semantic rule preservation, path canonicalization coverage |
| Validation orchestration boundaries | `core/python/src/watchtower_core/repo_ops/validation/all.py`; `core/python/src/watchtower_core/cli/validation_handlers.py`; `docs/commands/core_python/watchtower_core_validate.md` | No runtime behavior drift, no output-contract drift, adjacency review around aggregate validation |
| Discoverability and indexing | `core/python/tests/unit/README.md`; `core/python/tests/integration/README.md`; `core/control_plane/indexes/repository_paths/repository_path_index.v1.json`; `watchtower-core query paths` | README inventory truth, repository-path index coherence, historical-path compatibility, query discoverability |
| Traced governance surfaces | `docs/planning/**`; `core/control_plane/contracts/acceptance/validation_test_hotspot_rebalancing_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/validation_test_hotspot_rebalancing_planning_baseline.v1.json` | Coverage-map durability, findings ledger, acceptance alignment, evidence coverage, closeout state |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.validation_test_hotspot_rebalancing.001` | `medium` | `resolved` | `core/python/tests/integration/test_control_plane_artifacts.py`; integration validation helpers; direct loader or artifact-validation surfaces | the 1171-line integration hotspot now resolves through an 8-line compatibility marker plus four focused suites and a 30-line helper, and both the focused integration pytest subset and the final full `pytest -q` pass stayed green |
| `finding.validation_test_hotspot_rebalancing.002` | `medium` | `resolved` | `core/python/tests/unit/test_document_semantics_validation.py`; document-semantics validator surfaces; shared fixture-writing paths | the 1053-line unit hotspot now resolves through an 8-line compatibility marker plus four focused suites and a shared fixture-writer helper, and both the focused semantic-rule pytest subset and the final full `pytest -q` pass stayed green |
| `finding.validation_test_hotspot_rebalancing.003` | `medium` | `resolved` | `core/python/tests/unit/README.md`; `core/python/tests/integration/README.md`; repository path index; `watchtower-core query paths` | README inventory refresh plus `watchtower-core sync all --write --format json` rebuilt the repository-path index to 557 records, and `query paths` now resolves both preserved hotspot markers and new focused-suite paths |
| `finding.validation_test_hotspot_rebalancing.004` | `high` | `resolved` | `core/python/tests/integration/__init__.py`; `core/python/tests/integration/fixture_repo_support.py`; direct integration and unit consumers of the helper | the first full `pytest -q` rerun exposed a `ModuleNotFoundError` for bare `fixture_repo_support` imports after the new integration package boundary landed; the loop reopened and repaired all direct consumers to import through `tests.integration.fixture_repo_support`, after which the acceptance-aware full `pytest -q` rerun passed |
| `finding.validation_test_hotspot_rebalancing.005` | `medium` | `resolved` | `core/control_plane/contracts/acceptance/validation_test_hotspot_rebalancing_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/validation_test_hotspot_rebalancing_planning_baseline.v1.json` | the first `watchtower-core validate acceptance --trace-id trace.validation_test_hotspot_rebalancing --format json` pass found missing durable evidence coverage for acceptance IDs `002` through `005`; the evidence ledger was expanded and the final acceptance reconciliation plus `watchtower-core validate all --format json` both passed cleanly |

## Work Breakdown
1. Replace the planning, decision, acceptance, evidence, and bootstrap-task placeholders with the real validation-hotspot scope, coverage map, findings ledger, accepted direction, and bounded execution tasks.
2. Complete `task.validation_test_hotspot_rebalancing.integration_suite_split.002` by splitting the integration artifact hotspot into focused suites plus a small helper and compatibility marker, then align integration README inventory coverage.
3. Complete `task.validation_test_hotspot_rebalancing.document_semantics_suite_split.003` by splitting the document-semantics hotspot into focused suites plus reusable fixture helpers and compatibility marker, then align unit README inventory coverage and repository-path discoverability.
4. Complete `task.validation_test_hotspot_rebalancing.validation_closeout.004` by running targeted validation, full validation, post-fix review, second-angle confirmation, adversarial confirmation, evidence refresh, and initiative closeout.

## Risks
- Focused suites could still end up arbitrarily grouped if the split follows line-count targets instead of real validation-family boundaries.
- Compatibility markers could hide accidental coverage loss if targeted validation does not explicitly exercise the new focused files.
- README inventory drift would silently break repository-path discoverability if not tested after the split.

## Validation Plan
- Run targeted pytest coverage for the new integration suites, new document-semantics suites, validation-all unit coverage, and any helper-focused tests while the split lands.
- Run `./.venv/bin/watchtower-core sync all --write --format json` after the planning and README inventory changes are in place so repository-path indexing and planning trackers stay aligned.
- Run full repository validation with `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/ruff check .`, and `./.venv/bin/python -m mypy src/watchtower_core`.
- Re-run the validation-hotspot boundary from a fresh post-fix angle, then perform a second independent no-new-issues review, then an adversarial confirmation pass that tries to falsify the claim that the hotspot area is now clean.
- Refresh the acceptance contract, planning-baseline evidence, planning trackers, indexes, and closeout metadata only after the final clean-state evidence is in hand.

## References
- March 13, 2026 refactor audit
- [validation_test_hotspot_rebalancing.md](/home/j/WatchTowerPlan/docs/planning/prds/validation_test_hotspot_rebalancing.md)
