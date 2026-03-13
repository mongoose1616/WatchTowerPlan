---
trace_id: trace.data_contract_index_family_baseline_alignment
id: design.implementation.data_contract_index_family_baseline_alignment
title: Data-Contract Index Family Baseline Alignment Implementation Plan
summary: Breaks Data-Contract Index Family Baseline Alignment into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T20:16:31Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/data_contracts/
- core/control_plane/indexes/standards/standard_index.v1.json
- docs/commands/core_python/watchtower_core_query_standards.md
- core/python/tests/unit/
---

# Data-Contract Index Family Baseline Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.data_contract_index_family_baseline_alignment`
- `Plan ID`: `design.implementation.data_contract_index_family_baseline_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.data_contract_index_family_baseline_alignment`
- `Linked Decisions`: `decision.data_contract_index_family_baseline_alignment_direction`
- `Source Designs`: `design.features.data_contract_index_family_baseline_alignment`
- `Linked Acceptance Contracts`: `contract.acceptance.data_contract_index_family_baseline_alignment`
- `Updated At`: `2026-03-13T20:16:31Z`

## Summary
Breaks Data-Contract Index Family Baseline Alignment into a bounded implementation slice.

## Source Request or Design
- design.features.data_contract_index_family_baseline_alignment
- Review the March 13, 2026 refactor audit under one stable standards-family theme until repeated confirmation passes find no new actionable issue.
- PRD: [data_contract_index_family_baseline_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/data_contract_index_family_baseline_alignment.md)
- Decision: [data_contract_index_family_baseline_alignment_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/data_contract_index_family_baseline_alignment_direction.md)

## Scope Summary
- Add one shared baseline standard for the planning-related data-contract index family and refactor the affected member standards to reference it while keeping their family-specific deltas explicit.
- Refresh the surrounding discoverability surfaces: standards READMEs, standard-index output, `watchtower-core query standards` documentation, and the direct standard-index query or sync tests.
- Keep acceptance, evidence, tasks, trackers, and derived planning indexes aligned through the full validation and closeout loop.
- Exclude whole-corpus templating, policy changes, CLI redesign, or unrelated low-priority refactor findings unless the confirmation loop discovers a direct same-theme dependency.

## Assumptions and Constraints
- The refactor must preserve current standard-query and standard-index runtime behavior unless a direct same-theme defect is discovered.
- The member standards must stay independently readable and governable after the shared baseline lands.
- README, command-doc, standard-index, and traced planning surfaces are companion authorities for this slice and must ship in the same change set as the member-standard refactor.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): constrains the required standard sections and the need to keep the shared baseline explicit rather than implicit.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): keeps the family discoverability work tied to the governed standard index and its query consumers.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): supports reducing repeated boilerplate only when the resulting standards remain easy to review.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): requires bounded traced tasks and aligned closeout surfaces for the implementation loop.

## Proposed Technical Approach
- Add `docs/standards/data_contracts/planning_index_family_standard.md` as the narrow shared baseline for the planning-related derived index standards.
- Refactor the targeted member standards so their shared rules move into the new baseline while `Guidance`, `Validation`, and `Change Control` retain only family-specific deltas plus an explicit pointer back to the baseline.
- Add the shared tag `planning_index_family` to the new baseline and every targeted member standard so `watchtower-core query standards --tag planning_index_family` becomes a stable retrieval path without any runtime code change.
- Refresh `docs/standards/README.md`, `docs/standards/data_contracts/README.md`, `docs/commands/core_python/watchtower_core_query_standards.md`, and the direct standard-index sync or CLI-query tests so the new family is visible in both prose navigation and machine-readable discovery.
- Rebuild derived surfaces with repository sync commands instead of editing generated indexes by hand.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Planning-index family standards | `docs/standards/data_contracts/planning_index_family_standard.md`; `coordination_index_standard.md`; `initiative_index_standard.md`; `planning_catalog_standard.md`; `prd_index_standard.md`; `decision_index_standard.md`; `design_document_index_standard.md`; `task_index_standard.md`; `traceability_index_standard.md` | repeated baseline prose, family-specific delta preservation, tag consistency, explicit operationalization or validation contracts |
| Standards navigation and family orientation | `docs/standards/README.md`; `docs/standards/data_contracts/README.md`; `docs/standards/documentation/standard_md_standard.md` | grouped navigation, reusable boilerplate guidance, family-boundary clarity, authoring guardrails |
| Standard index and query discoverability | `core/control_plane/indexes/standards/standard_index.v1.json`; `core/python/src/watchtower_core/repo_ops/sync/standard_index.py`; `core/python/src/watchtower_core/repo_ops/query/standards.py`; `docs/commands/core_python/watchtower_core_query_standards.md` | metadata sufficiency, no runtime regression, stable shared tag retrieval, human or machine parity |
| Validation and regression coverage | `core/python/tests/unit/test_standard_index_sync.py`; `core/python/tests/unit/test_cli_knowledge_query_commands.py` | shared-tag projection, query-surface discoverability, family-baseline inclusion, no stale expectations |
| Traced governance surfaces | `docs/planning/**`; `core/control_plane/contracts/acceptance/data_contract_index_family_baseline_alignment_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/data_contract_index_family_baseline_alignment_planning_baseline.v1.json` | coverage-map durability, findings ledger, acceptance alignment, evidence coverage, closeout state |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.data_contract_index_family_baseline_alignment.001` | `medium` | `resolved` | `docs/standards/data_contracts/planning_index_family_standard.md`; `coordination_index_standard.md`; `initiative_index_standard.md`; `planning_catalog_standard.md`; `prd_index_standard.md`; `decision_index_standard.md`; `design_document_index_standard.md`; `task_index_standard.md`; `traceability_index_standard.md` | the new shared planning-index family baseline now holds the repeated derived-index contract, the eight member standards cite it and keep explicit family-specific deltas, and the exact-set verification over the rebuilt standard index resolved to the expected nine-family set with no extras or misses |
| `finding.data_contract_index_family_baseline_alignment.002` | `medium` | `resolved` | `docs/standards/README.md`; `docs/standards/data_contracts/README.md`; `core/control_plane/indexes/standards/standard_index.v1.json`; `docs/commands/core_python/watchtower_core_query_standards.md`; `core/python/tests/unit/test_standard_index_sync.py`; `core/python/tests/unit/test_cli_knowledge_query_commands.py` | the standards READMEs now expose the family explicitly, `watchtower-core query standards --category data_contracts --tag planning_index_family --limit 20 --format json` returned `result_count: 9`, the command-doc operationalization probe returned only `std.data_contracts.planning_index_family`, and the focused sync or CLI-query pytest subset passed |
| `finding.data_contract_index_family_baseline_alignment.003` | `low` | `resolved` | `docs/standards/documentation/standard_md_standard.md`; member standards that rely on repeated boilerplate | `standard_md_standard.md` now governs the narrow shared-baseline pattern explicitly, and both `planning_index_family_standard.md` and the refactored `prd_index_standard.md` passed targeted document-semantics validation with `issue_count: 0` |
| `finding.data_contract_index_family_baseline_alignment.004` | `low` | `resolved` | `core/python/tests/unit/test_standard_index_sync.py`; `core/python/tests/unit/test_all_validation.py`; `core/python/` validation suite | the first full repository pass exposed a line-length regression in the new `test_standard_index_sync.py` assertion; the loop reopened, the assertion was wrapped, `ruff check .` passed, and the subsequent `pytest -q` rerun passed cleanly |
| `finding.data_contract_index_family_baseline_alignment.005` | `medium` | `resolved` | `core/control_plane/contracts/acceptance/data_contract_index_family_baseline_alignment_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/data_contract_index_family_baseline_alignment_planning_baseline.v1.json` | the first full `watchtower-core validate all --format json` pass exposed bootstrap-only acceptance or evidence alignment drift for acceptance IDs `002` through `005`; the loop reopened, the contract and evidence ledger were expanded, `watchtower-core validate acceptance --trace-id trace.data_contract_index_family_baseline_alignment --format json` returned `issue_count: 0`, `watchtower-core validate all --format json` passed with `1116` passed and `0` failed, and `pytest -q` then passed |

## Work Breakdown
1. Replace the planning placeholders with the real coverage map, findings ledger, accepted direction, and bounded execution tasks for the standards-family refactor.
2. Complete `task.data_contract_index_family_baseline_alignment.family_baseline.002` by adding the shared planning-index-family baseline standard and refactoring the targeted member standards plus adjacent authoring guidance and README navigation.
3. Complete `task.data_contract_index_family_baseline_alignment.standard_index_discoverability.003` by refreshing the standard index, query command docs, and regression tests around the new shared family tag and discoverability path.
4. Complete `task.data_contract_index_family_baseline_alignment.validation_closeout.004` by running targeted validation, full validation, post-fix review, second-angle confirmation, adversarial confirmation, evidence refresh, and initiative closeout.

## Risks
- A weak family baseline could add another document without materially shrinking the repeated member-standard prose.
- Shared tagging can regress into noise if the family boundary is not kept narrow and consistently applied.
- Acceptance and evidence coverage can drift if the trace closes without refreshing the contract and ledger after the final confirmation loop.

## Validation Plan
- Run targeted tests for standard-index sync and CLI standards-query coverage after the family baseline and tag changes land.
- Rebuild derived surfaces with `./.venv/bin/watchtower-core sync all --write --format json` once the authored standards and README updates are in place.
- Run full repository validation with `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/ruff check .`, and `./.venv/bin/python -m mypy src/watchtower_core`.
- Re-run the same theme from a fresh post-fix angle, then a second independent no-new-issues review, then an adversarial confirmation pass aimed at falsifying the claim that the planning-index family is now clean.
- Refresh the acceptance contract, evidence ledger, planning trackers, and closeout metadata only after the final no-new-issues state is verified.

## References
- March 13, 2026 refactor audit
- [data_contract_index_family_baseline_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/data_contract_index_family_baseline_alignment.md)
