---
trace_id: trace.active_first_planning_query_history_alignment
id: design.implementation.active_first_planning_query_history_alignment
title: Active-First Planning Query History Alignment Implementation Plan
summary: Breaks Active-First Planning Query History Alignment into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T21:01:42Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- docs/commands/core_python/
- docs/planning/
---

# Active-First Planning Query History Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.active_first_planning_query_history_alignment`
- `Plan ID`: `design.implementation.active_first_planning_query_history_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.active_first_planning_query_history_alignment`
- `Linked Decisions`: `decision.active_first_planning_query_history_alignment_direction`
- `Source Designs`: `design.features.active_first_planning_query_history_alignment`
- `Linked Acceptance Contracts`: `contract.acceptance.active_first_planning_query_history_alignment`
- `Updated At`: `2026-03-13T21:01:42Z`

## Summary
Breaks Active-First Planning Query History Alignment into a bounded implementation slice.

## Source Request or Design
- Do another comprehensive internal project review for refactor under one stable planning-navigation theme until no new actionable issues remain.
- Address the remaining active-vs-history planning navigation drift identified by the March 13, 2026 refactor audit.

## Scope Summary
- Align the default browse behavior of `watchtower-core query planning` and `watchtower-core query initiatives` with the repository's active-first planning-navigation model, plus the direct JSON signaling, command docs, planning READMEs, and regression tests that govern the same seam.
- Review adjacent query services, loaders, initiative and planning read models, and planning trackers or indexes for same-theme drift, but limit remediation to the bounded entrypoint and companion-surface slice unless discovery proves a wider same-theme defect.
- Exclude schema changes, planning-family consolidation, workflow-lattice refactors, and standards-threshold policy changes.

## Assumptions and Constraints
- Explicit historical or known-trace lookups must remain available and deterministic after the active-default browse behavior lands.
- The initiative index, planning catalog, and authority map already encode the intended surface boundary; the issue is primarily entrypoint behavior and companion guidance, not index design.
- The active-default browse rule should apply only when the user has not already supplied a meaningful filter that implies explicit trace or history intent.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): keeps the trace-linked deep-planning and initiative-family surfaces distinct but aligned.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): constrains initiative-family projection semantics and explicit status handling.
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md): requires explicit status-field separation rather than generic `status` reuse.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): requires behavior, defaults, and related-command routing to be described accurately in the command pages.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): supports tightening the planning navigation docs without turning them into handbooks.

## Proposed Technical Approach
- Keep the core initiative and planning query services unchanged and inject the active-default browse policy at the CLI handler layer, mirroring the existing coordination pattern.
- Add a small helper or bounded conditional path that determines when the active default applies for planning and initiative browse commands, then plumb the applied default into JSON payloads and human empty-state messaging.
- Refresh the planning and initiative command docs plus the planning root and initiative-family README guidance so the documented navigation hierarchy matches the runtime behavior.
- Extend the direct CLI planning-query regression suite to cover filterless default behavior, explicit history lookup, and explicit trace lookup after the default lands.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Query-entrypoint behavior | `core/python/src/watchtower_core/cli/query_coordination_handlers.py`; `core/python/src/watchtower_core/cli/query_coordination_family.py` | active-default browse policy, explicit-history escape hatches, payload signaling, human empty-state guidance |
| Direct query services and read models | `core/python/src/watchtower_core/repo_ops/query/planning.py`; `core/python/src/watchtower_core/repo_ops/query/initiatives.py`; `core/python/src/watchtower_core/control_plane/models/planning_catalog.py`; `core/python/src/watchtower_core/control_plane/loader.py` | verify the issue is entrypoint policy rather than loader, model, or service drift |
| Planning navigation docs | `docs/planning/README.md`; `docs/planning/initiatives/README.md` | active-first routing cues, explicit history-browse guidance, status-language clarity |
| Command docs and authority guidance | `docs/commands/core_python/watchtower_core_query_planning.md`; `docs/commands/core_python/watchtower_core_query_initiatives.md`; `docs/commands/core_python/watchtower_core_query_authority.md`; `docs/commands/core_python/watchtower_core_query.md` | documented defaults, deep-planning-vs-initiative boundary, explicit history opt-in |
| Adjacent governed planning surfaces | `docs/planning/coordination_tracking.md`; `docs/planning/initiatives/initiative_tracking.md`; `core/control_plane/indexes/initiatives/initiative_index.v1.json`; `core/control_plane/indexes/planning/planning_catalog.v1.json`; `core/control_plane/registries/authority_map/authority_map.v1.json` | confirm existing indexes and trackers already support the intended authority split and do not need structural remediation |
| Regression and validation surfaces | `core/python/tests/unit/test_cli_planning_query_commands.py`; targeted CLI queries; full validation suite | default-behavior coverage, preserved history lookup, no new same-theme drift |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.active_first_planning_query_history_alignment.001` | `high` | `resolved` | `core/python/src/watchtower_core/cli/query_coordination_handlers.py`; `core/python/src/watchtower_core/cli/query_coordination_family.py`; `docs/commands/core_python/watchtower_core_query_planning.md`; `docs/commands/core_python/watchtower_core_query_initiatives.md` | discovery reproduced that unfiltered `query planning` and `query initiatives` returned completed traces even though authority and README guidance describe an active-first navigation path; after the fix, filterless browse calls report `default_initiative_status: active` and no longer surface terminal-history rows by default |
| `finding.active_first_planning_query_history_alignment.002` | `medium` | `resolved` | `docs/planning/README.md`; `docs/planning/initiatives/README.md`; `docs/commands/core_python/watchtower_core_query_planning.md`; `docs/commands/core_python/watchtower_core_query_initiatives.md`; `docs/commands/core_python/watchtower_core_query.md` | companion planning and command docs now explain the active-default browse path and explicit historical opt-in consistently, matching the final runtime behavior |
| `finding.active_first_planning_query_history_alignment.003` | `medium` | `resolved` | `core/python/src/watchtower_core/cli/query_coordination_handlers.py`; `core/python/tests/unit/test_cli_planning_query_commands.py` | the planning and initiative query payloads now expose `default_initiative_status` when the active-default path applies, matching the existing coordination payload pattern and making the implicit filter explicit to machine consumers |
| `finding.active_first_planning_query_history_alignment.004` | `medium` | `resolved` | `core/control_plane/contracts/acceptance/active_first_planning_query_history_alignment_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/active_first_planning_query_history_alignment_planning_baseline.v1.json`; `core/python/tests/unit/test_all_validation.py` | the first acceptance-aware full rerun exposed bootstrap-only acceptance and evidence coverage for IDs `002` through `005`; the loop reopened, the contract and evidence ledger were expanded, `watchtower-core validate acceptance --trace-id trace.active_first_planning_query_history_alignment --format json` returned `issue_count: 0`, and `watchtower-core validate all --format json` then passed with `1131` passed and `0` failed |
| `finding.active_first_planning_query_history_alignment.005` | `medium` | `resolved` | `core/python/tests/unit/test_route_and_query_handlers.py`; `core/python/src/watchtower_core/cli/query_coordination_handlers.py` | the adversarial full `pytest -q` rerun exposed a stale empty-message assertion that still expected the pre-change initiative browse text; the regression was updated to assert the new active-default guidance, the focused handler or CLI subset passed, and the subsequent full `pytest -q` rerun passed cleanly |
| `finding.active_first_planning_query_history_alignment.006` | `low` | `resolved` | `core/python/tests/unit/test_route_and_query_handlers.py`; `core/python/` validation tooling | the final closed-state Ruff pass caught a line-length regression in the updated empty-message assertion; the assertion was wrapped and the final Ruff plus repository validation reruns passed cleanly |

## Work Breakdown
1. Replace the scaffold placeholders with the real PRD, accepted direction decision, feature design, implementation plan, coverage map, findings ledger, and bounded task set for the active-first planning-navigation slice.
2. Implement the bounded query-entrypoint behavior change and payload signaling, keeping the initiative and planning query services, loaders, and artifact schemas unchanged unless the same-theme review proves otherwise.
3. Refresh the planning README and command-doc guidance plus the direct CLI planning-query regressions so the documented navigation model and runtime behavior match.
4. Run targeted validation, full validation, post-fix review, second-angle confirmation, adversarial confirmation, evidence refresh, task closeout, initiative closeout, and commit closeout.

## Risks
- The active-default policy could be applied in cases that should remain explicit-history lookups if the handler boundary is defined too loosely.
- Documentation might overstate the behavior change if the tests do not cover both the new default and the preserved historical path.
- Acceptance and evidence coverage can drift during closeout if the final confirmation-loop results are not recorded back into the contract and ledger.

## Validation Plan
- Run targeted CLI planning-query regression tests covering default browse behavior, explicit trace lookup, and explicit historical lookup.
- Probe live command behavior with `watchtower-core query planning`, `watchtower-core query initiatives`, and `watchtower-core query authority` in JSON mode to verify the active-default and preserved history paths.
- Run full repository validation with `watchtower-core validate all --format json`, `pytest -q`, `ruff check .`, and `python -m mypy src/watchtower_core`.
- Re-run the same themed area from a fresh post-fix angle, then a second independent no-new-issues review, then an adversarial confirmation pass that tries to retrieve historical records through explicit filters after the default has changed.

## References
- March 13, 2026 refactor audit
- [active_first_planning_query_history_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/active_first_planning_query_history_alignment.md)
- [active_first_planning_query_history_alignment.md](/home/j/WatchTowerPlan/docs/planning/design/features/active_first_planning_query_history_alignment.md)
