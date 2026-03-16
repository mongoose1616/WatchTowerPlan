---
trace_id: trace.core_split_compatibility_wrapper_retirement
id: design.implementation.core_split_compatibility_wrapper_retirement
title: Core Split Compatibility Wrapper Retirement Implementation Plan
summary: Breaks compatibility-wrapper retirement into a bounded implementation slice
  that leaves `watchtower_core` cleaner for future extraction.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-16T03:31:47Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/query/
- core/python/src/watchtower_core/sync/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/README.md
- core/python/src/watchtower_core/query/README.md
- core/python/src/watchtower_core/sync/README.md
- core/python/src/watchtower_core/validation/README.md
- core/python/src/watchtower_core/cli/
- core/python/README.md
- core/python/tests/unit/test_repo_ops_boundary.py
---

# Core Split Compatibility Wrapper Retirement Implementation Plan

## Record Metadata
- `Trace ID`: `trace.core_split_compatibility_wrapper_retirement`
- `Plan ID`: `design.implementation.core_split_compatibility_wrapper_retirement`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.core_split_compatibility_wrapper_retirement`
- `Linked Decisions`: `decision.core_split_compatibility_wrapper_retirement_direction`
- `Source Designs`: `design.features.core_split_compatibility_wrapper_retirement`
- `Linked Acceptance Contracts`: `contract.acceptance.core_split_compatibility_wrapper_retirement`
- `Updated At`: `2026-03-16T03:31:47Z`

## Summary
Breaks compatibility-wrapper retirement into a bounded implementation slice that leaves `watchtower_core` cleaner for future extraction.

## Source Request or Design
- Feature design: `docs/planning/design/features/core_split_compatibility_wrapper_retirement.md`
- PRD: `docs/planning/prds/core_split_compatibility_wrapper_retirement.md`
- Decision: `docs/planning/decisions/core_split_compatibility_wrapper_retirement_direction.md`

## Scope Summary
- Retire repo-specific compatibility wrapper leaf modules from top-level query, sync, and aggregate-validation namespaces.
- Cover code, tests, and runtime package docs needed to prove the split-ready boundary.
- Leave package extraction itself, release shims, and broader architecture changes out of scope.

## Assumptions and Constraints
- `repo_ops` remains the authoritative home for `WatchTowerPlan`-specific query, sync, validation, and CLI orchestration behavior.
- Reusable validators that are genuinely export-safe must stay available from top-level validation namespaces.
- The current dirty worktree does not change the implementation target boundary.
- Repo-native planning surfaces can be refreshed from the canonical Python workspace under `core/python/` while the trace stays in planning-only state.

## Current-State Context
- The active initiative inventory is currently empty, so this trace becomes the next bounded split-prep slice rather than a child of an existing active initiative.
- The March 16, 2026 code still carries compatibility wrapper trees beneath `watchtower_core.query/` and `watchtower_core.sync/`, and the aggregate validation compatibility module remains at `watchtower_core.validation.all`.
- The existing compatibility regression test still encodes wrapper preservation rather than wrapper retirement.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: package code, tests, and README updates stay inside `core/python/`.
- `docs/standards/engineering/engineering_best_practices_standard.md`: keep the cleanup modular, explicit, and backed by targeted regression tests.
- `docs/standards/governance/task_tracking_standard.md`: execute the change through bounded tasks with explicit dependency ordering.
- `docs/standards/governance/traceability_standard.md`: preserve explicit links from the implementation work back to the planning chain.

## Proposed Technical Approach
- Replace repo-local imports that still rely on wrapper paths with direct `repo_ops` or reusable validation imports.
- Remove retired wrapper modules and narrow the remaining package roots to explicit guardrails or genuinely reusable exports only.
- Rewrite the old compatibility test into boundary-proof coverage and align package README guidance with the new surface.
- Refresh derived planning surfaces and close out only after the repo-native command path is healthy enough to rerun sync and validation deterministically.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Query wrapper retirement | `core/python/src/watchtower_core/query/`; repo-local callers and tests | Remove repo-specific forwarding imports from the export-safe query namespace. |
| Sync wrapper retirement | `core/python/src/watchtower_core/sync/`; repo-local callers and tests | Remove repo-specific forwarding imports from the export-safe sync namespace. |
| Validation boundary cleanup | `core/python/src/watchtower_core/validation/`; `core/python/src/watchtower_core/repo_ops/validation/` | Keep reusable validators at top level while retiring repo-wide aggregate validation compatibility paths. |
| Runtime boundary proof | `core/python/src/watchtower_core/README.md`; package READMEs; `core/python/README.md`; boundary tests | Make the split-ready package boundary explicit and fail closed when wrappers reappear. |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.core_split_compatibility_wrapper_retirement.001` | `high` | `open` | `watchtower_core.query`; `watchtower_core.sync`; `watchtower_core.validation.all` | Representative leaf modules remain direct `repo_ops` re-exports from export-safe namespaces. |
| `finding.core_split_compatibility_wrapper_retirement.002` | `high` | `open` | `core/python/tests/unit/test_repo_ops_boundary.py` | The current regression test still asserts that the legacy compatibility wrappers remain available. |
| `finding.core_split_compatibility_wrapper_retirement.003` | `medium` | `open` | package READMEs; `core/python/README.md` | Runtime-boundary docs still describe supported compatibility-wrapper imports for query and sync. |

## Work Breakdown
1. Publish the planning chain, accepted direction, acceptance contract, planning-baseline evidence, and bounded task queue for wrapper retirement.
2. Complete `task.core_split_compatibility_wrapper_retirement.wrapper_retirement.002` by removing repo-specific leaf wrappers and moving remaining callers to direct `repo_ops` or reusable validation imports.
3. Complete `task.core_split_compatibility_wrapper_retirement.boundary_proof.003` by tightening package-boundary docs and replacing compatibility-preservation tests with fail-closed boundary proofs.
4. Complete `task.core_split_compatibility_wrapper_retirement.validation_closeout.004` by rerunning targeted tests, full validation, derived-surface refresh, acceptance evidence refresh, and initiative closeout.

## Risks
- Hidden imports may still depend on wrapper paths and only fail after broader test execution.
- Boundary-proof tests can accidentally over-constrain legitimate reusable validation services if the split is classified incorrectly.
- Derived planning surfaces may remain stale until the current repo command path is healthy enough for deterministic refresh.

## Validation Plan
- Run targeted boundary coverage for the retired wrapper modules and their direct callers.
- Run `pytest -q`, `ruff check .`, and `python -m mypy src/watchtower_core` after the wrapper cleanup lands.
- Refresh derived planning and task surfaces plus acceptance evidence with repo-native sync and validation reruns as the implementation slice lands.
- Close the trace only after targeted boundary tests and the full repository validation loop pass cleanly.

## References
- `docs/planning/prds/core_split_compatibility_wrapper_retirement.md`
- `docs/planning/design/features/core_split_compatibility_wrapper_retirement.md`
- `docs/planning/prds/core_export_hardening_followup.md`
- `docs/planning/design/features/core_export_hardening.md`
