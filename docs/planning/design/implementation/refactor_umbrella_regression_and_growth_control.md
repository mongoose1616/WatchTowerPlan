---
trace_id: trace.refactor_umbrella_regression_and_growth_control
id: design.implementation.refactor_umbrella_regression_and_growth_control
title: Refactor Umbrella Regression and Growth Control Implementation Plan
summary: Breaks Refactor Umbrella Regression and Growth Control into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T22:47:49Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/closeout/initiative.py
- workflows/modules/repository_review.md
- workflows/modules/initiative_closeout.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
- docs/commands/core_python/watchtower_core_closeout.md
- docs/standards/governance/initiative_closeout_standard.md
- docs/planning/
---

# Refactor Umbrella Regression and Growth Control Implementation Plan

## Record Metadata
- `Trace ID`: `trace.refactor_umbrella_regression_and_growth_control`
- `Plan ID`: `design.implementation.refactor_umbrella_regression_and_growth_control`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.refactor_umbrella_regression_and_growth_control`
- `Linked Decisions`: `decision.refactor_umbrella_regression_and_growth_control_direction`
- `Source Designs`: `design.features.refactor_umbrella_regression_and_growth_control`
- `Linked Acceptance Contracts`: `contract.acceptance.refactor_umbrella_regression_and_growth_control`
- `Updated At`: `2026-03-13T22:47:49Z`

## Summary
Breaks Refactor Umbrella Regression and Growth Control into a bounded implementation slice.

## Source Request or Design
- User-requested umbrella refactor review across REFACTOR.md, pass traces, and commit history with root-cause hardening for regression, duplication, and surface-growth drift.

## Scope Summary
- Cover the full external `REFACTOR.md` finding matrix, the seven completed refactor traces, the
  recent refactor commit series, and the closeout or workflow seams that caused repeated late
  regressions and local-only stop conditions.
- Exclude archival deletion of historical refactor traces, broad policy rewrites for planning
  thresholds, and unrelated runtime redesign outside the closeout and themed-review boundaries.

## Coverage Map
- External audit baseline and finding matrix:
  `/home/j/WatchTower/REFACTOR.md`
- Prior refactor traces and their acceptance or evidence surfaces:
  `docs/planning/design/implementation/refactor_review_and_hardening.md`;
  `docs/planning/design/implementation/reference_and_reserved_surface_maturity_signaling.md`;
  `docs/planning/design/implementation/planning_authoring_hotspot_regression_hardening.md`;
  `docs/planning/design/implementation/typed_query_surface_modularity_hardening.md`;
  `docs/planning/design/implementation/validation_test_hotspot_rebalancing.md`;
  `docs/planning/design/implementation/data_contract_index_family_baseline_alignment.md`;
  `docs/planning/design/implementation/active_first_planning_query_history_alignment.md`;
  `docs/planning/design/implementation/workflow_route_boundary_discoverability_hardening.md`;
  `docs/planning/design/implementation/query_family_source_surface_alignment.md`
- Commit-history and surface-growth review:
  `origin/initiative/core-export-readiness-and-optimization..HEAD`;
  `docs/planning/**`;
  `core/control_plane/contracts/acceptance/**`;
  `core/control_plane/ledgers/validation_evidence/**`
- Closeout runtime and direct consumers:
  `core/python/src/watchtower_core/closeout/initiative.py`;
  `core/python/src/watchtower_core/cli/closeout_handlers.py`;
  `core/python/tests/unit/test_initiative_closeout.py`;
  `core/python/tests/unit/test_closeout_handlers.py`;
  `core/python/tests/integration/test_task_workflow_end_to_end.py`
- Companion workflow, standards, and command docs:
  `workflows/modules/repository_review.md`;
  `workflows/modules/initiative_closeout.md`;
  `docs/standards/governance/initiative_closeout_standard.md`;
  `docs/commands/core_python/watchtower_core_closeout.md`;
  `docs/commands/core_python/watchtower_core_closeout_initiative.md`

## Original Audit Status Matrix
| Audit ID | Current Status | Evidence |
|---|---|---|
| `RF-CTL-001` | `resolved` | Coordination index is now active-first with empty `entries` and compact recent-closeout summaries only. |
| `RF-PLN-001` | `remaining_design_debt` | Planning file count grew from `359` to `431`; navigation improved, but historical corpus volume remains high. |
| `RF-CMD-001` | `resolved` | Root/group command pages were reduced to route-first sizes (`watchtower_core.md` `77`, `query` `86`, `sync` `79`). |
| `RF-PY-001` | `resolved` | `planning_scaffolds.py` and `task_lifecycle.py` were split down to materially smaller seams. |
| `RF-PLN-002` | `partially_mitigated` | Active-first coordination and planning entrypoints reduced overlap, but planning remains a large projection family. |
| `RF-STD-001` | `partially_mitigated` | Planning-index family baseline work reduced one high-overlap standard cluster, but standards-family repetition remains broad. |
| `RF-STD-002` | `remaining_design_debt` | Policy-amplified planning and task volume remains and the recent refactor pass series increased traced planning surface further. |
| `RF-CMD-002` | `deferred` | Command breadth is still largely downstream of artifact-family breadth; no new direct regression confirmed in this pass. |
| `RF-CTL-002` | `resolved` | README-only control-plane families are now explicitly marked as reserved placeholders. |
| `RF-PY-002` | `resolved` | Declarative planning scaffold specs replaced the larger hard-coded map pattern. |
| `RF-PY-003` | `resolved` | Planning models were split into focused modules. |
| `RF-TST-001` | `resolved` | Large validation and CLI hotspots were split into focused suites with shared helpers. |
| `RF-WKF-001` | `partially_mitigated` | Route discrimination and workflow discoverability improved, but the route lattice remains intentionally explicit. |
| `RF-REF-001` | `resolved` | Reference maturity signaling now distinguishes active support, supporting authority, and candidate future guidance. |
| `RF-PLN-003` | `partially_mitigated` | Status semantics are better documented, but artifact lifecycle versus initiative state still requires explicit interpretation. |
| `RF-PY-004` | `deferred` | `query_coordination_handlers.py` remains concentrated and grew to `591` lines; this pass records it but does not redesign the family. |
| `RF-CTL-003` | `intentionally_preserved` | Acceptance and evidence one-per-trace density remains standards-backed and is not a simplification target. |

## Findings Ledger
| Finding | Severity | Status | Affected Surfaces | Verification Target |
|---|---|---|---|---|
| `finding.001` | `high` | `resolved` | umbrella refactor planning surfaces; `workflows/modules/repository_review.md`; recent refactor trace chain | One umbrella refactor matrix records the original audit findings, the completed follow-up traces, and the pass-series conclusions so same-theme review no longer depends on lost chat context or per-slice memory. |
| `finding.002` | `high` | `resolved` | `core/python/src/watchtower_core/closeout/initiative.py`; `core/python/src/watchtower_core/cli/closeout_handlers.py`; closeout docs and tests | Initiative closeout fails by default when acceptance reconciliation reports issues and only proceeds when an explicit override records the exception. |
| `finding.003` | `medium` | `resolved` | `workflows/modules/initiative_closeout.md`; `docs/standards/governance/initiative_closeout_standard.md`; `docs/commands/core_python/watchtower_core_closeout*.md` | Runtime closeout behavior and authored operator guidance stay aligned on the acceptance gate and the exception path. |

## Pass-Trace and Commit-History Review Conclusions
- The `origin/initiative/core-export-readiness-and-optimization..HEAD` refactor pass series
  changed `202` files with `26514` insertions and `12953` deletions, so the audit concern about
  surface growth was real and not a false positive.
- The dominant duplication or regression pattern was not runtime capability loss. It was
  governance churn: repeated late acceptance or evidence repairs, repeated same-theme planning
  trace creation, and added human or machine artifacts required to close each bounded slice.
- The current tree shows that most original audit hotspots were fixed materially, so the
  highest-leverage root fix is process hardening at the review and closeout boundaries rather
  than another broad runtime redesign in this same change.
- The remaining design-debt items are still `RF-PLN-001`, `RF-STD-002`, and `RF-PY-004`.
  These are now explicitly monitored instead of being conflated with the resolved closeout and
  review-loop regressions.
- Do not start a broad redesign from this trace. Open a new redesign effort only if the new
  umbrella-trace rule and fail-closed acceptance gate still fail to flatten same-theme planning
  growth or if concentrated surfaces such as `query_coordination_handlers.py` continue to regrow
  under later confirmation passes.

## Assumptions and Constraints
- Preserve existing closeout semantics for open-task blocking, traceability updates, and derived
  surface refresh.
- Preserve all standards-backed explicit families; this pass should reduce duplicated work and
  late regressions without weakening governance.
- Use one umbrella trace for this continuing review theme rather than creating further
  same-theme subtraces during the pass.

## Internal Standards and Canonical References Applied
- `docs/standards/governance/traceability_standard.md`: closeout and validation changes must
  preserve explicit trace links.
- `docs/standards/governance/initiative_closeout_standard.md`: closeout exceptions must be
  explicit and mirrored consistently.
- `docs/standards/data_contracts/acceptance_contract_standard.md`: acceptance contracts must stay
  aligned with PRD acceptance IDs.
- `docs/standards/data_contracts/validation_evidence_standard.md`: evidence artifacts must stay
  aligned with validators, acceptance IDs, and subject surfaces.

## Proposed Technical Approach
- Publish the master umbrella status matrix and the accepted direction decision before
  implementation so the review has one stable memory surface.
- Extend `InitiativeCloseoutService` to invoke `AcceptanceReconciliationService` and block
  closeout on issues unless an explicit acceptance-drift override is present.
- Expose the override through the CLI and result payload, then align the initiative-closeout
  workflow, governing standard, and closeout command pages to the new fail-closed behavior.
- Validate the final tree through targeted closeout coverage, full repository validation, and
  repeated confirmation passes that revisit the original audit matrix from a second angle.

## Work Breakdown
1. Publish the umbrella refactor audit matrix, findings ledger, and direction decision, then
   create the bounded execution tasks under the same trace.
2. Implement the initiative-closeout acceptance gate plus explicit override and add direct unit
   or integration coverage.
3. Reconcile the workflow, standards, and closeout command docs with the runtime behavior.
4. Run targeted validation, full validation, post-fix review, second-angle confirmation, and an
   adversarial closeout probe; reopen the loop if the same root-cause boundary yields a new
   actionable issue.

## Risks
- A too-strict closeout gate could block legitimate cancellation or abandonment paths if the
  exception path is not explicit enough.
- The umbrella matrix may surface unresolved design debt that this pass can document but not
  erase from historical repository volume.

## Validation Plan
- Run targeted pytest for `test_initiative_closeout.py`, `test_closeout_handlers.py`, and the
  closeout-focused integration coverage in `test_task_workflow_end_to_end.py`.
- Run `watchtower-core validate acceptance --trace-id trace.refactor_umbrella_regression_and_growth_control --format json`.
- Run `watchtower-core validate all --format json`, `pytest -q`, `ruff check .`, and
  `python -m mypy src/watchtower_core`.
- Re-run the original audit questions from a second angle by checking the current audit matrix,
  the refactor commit series, and a dry-run closeout with intentionally broken acceptance state.

## Final Validation and Confirmation Evidence
- Targeted closeout-focused pytest passed: `8` tests.
- `watchtower-core validate acceptance --trace-id trace.refactor_umbrella_regression_and_growth_control --format json`
  passed with `issue_count: 0`.
- `watchtower-core validate all --format json` passed with `1176` passed and `0` failed.
- `pytest -q` passed on the final pre-closeout tree.
- `ruff check .` passed.
- `python -m mypy src/watchtower_core` passed with no issues in `191` source files.
- Live confirmation shows `watchtower-core query commands --query "closeout initiative" --format json`
  resolving `watchtower_core_closeout*.md` to
  `core/python/src/watchtower_core/cli/closeout_family.py` with the explicit
  `--allow-acceptance-issues` synopsis preserved.

## References
- REFACTOR.md
- docs/planning/decisions/refactor_umbrella_regression_and_growth_control_direction.md
