---
trace_id: trace.planning_query_efficiency_and_handler_modularity
id: design.implementation.planning_query_efficiency_and_handler_modularity
title: Planning Query Efficiency and Coordination Handler Modularity Implementation
  Plan
summary: Breaks Planning Query Efficiency and Coordination Handler Modularity into
  a bounded implementation slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T23:40:35Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_projection_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_family.py
- core/python/src/watchtower_core/repo_ops/query/common.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/control_plane/models/planning_catalog.py
- docs/commands/core_python/
---

# Planning Query Efficiency and Coordination Handler Modularity Implementation Plan

## Record Metadata
- `Trace ID`: `trace.planning_query_efficiency_and_handler_modularity`
- `Plan ID`: `design.implementation.planning_query_efficiency_and_handler_modularity`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.planning_query_efficiency_and_handler_modularity`
- `Linked Decisions`: `decision.planning_query_efficiency_and_handler_modularity_direction`
- `Source Designs`: `design.features.planning_query_efficiency_and_handler_modularity`
- `Linked Acceptance Contracts`: `contract.acceptance.planning_query_efficiency_and_handler_modularity`
- `Updated At`: `2026-03-13T23:40:35Z`

## Summary
Breaks Planning Query Efficiency and Coordination Handler Modularity into a bounded implementation slice.

## Source Request or Design
- Comprehensive redesign review for planning-surface/query-model efficiency and the remaining concentrated coordination-query handler family under one stable trace.

## Scope Summary
- Covers one redesign boundary: shared runtime search mechanics for the planning,
  initiative, and coordination query projections plus the concentrated coordination-query
  handler family and their adjacent docs/tests.
- Covers the in-scope docs, indexes, trackers, acceptance/evidence artifacts, and direct
  compatibility consumers needed to land the redesign safely.
- Excludes planning-catalog schema redesign, new governed summary indexes, query payload
  changes, or another disconnected refactor umbrella.

## Coverage Map
- Runtime query-model layer:
  `core/python/src/watchtower_core/repo_ops/query/initiatives.py`;
  `core/python/src/watchtower_core/repo_ops/query/planning.py`;
  `core/python/src/watchtower_core/repo_ops/query/coordination.py`;
  `core/python/src/watchtower_core/repo_ops/query/common.py`
- Concentrated CLI family:
  `core/python/src/watchtower_core/cli/query_coordination_handlers.py`;
  `core/python/src/watchtower_core/cli/query_coordination_family.py`;
  `core/python/src/watchtower_core/cli/query_handlers.py`;
  `core/python/src/watchtower_core/cli/handler_common.py`
- Loader, projection, and adjacent read-model surfaces:
  `core/python/src/watchtower_core/control_plane/loader.py`;
  `core/python/src/watchtower_core/control_plane/models/coordination.py`;
  `core/python/src/watchtower_core/control_plane/models/planning_catalog.py`;
  `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`;
  `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py`;
  `core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py`
- Direct tests and consumers:
  `core/python/tests/unit/test_route_and_query_handlers.py`;
  `core/python/tests/unit/test_cli_planning_query_commands.py`;
  `core/python/tests/unit/test_planning_catalog_sync.py`;
  `core/python/tests/unit/test_coordination_index_sync.py`;
  `core/python/tests/unit/test_initiative_index_sync.py`;
  `core/python/tests/unit/test_cli.py`;
  `core/python/tests/integration/test_control_plane_loader_and_foundation_contracts.py`
- Companion docs and lookup surfaces:
  `docs/commands/core_python/watchtower_core_query_coordination.md`;
  `docs/commands/core_python/watchtower_core_query_planning.md`;
  `docs/commands/core_python/watchtower_core_query_initiatives.md`;
  `core/control_plane/indexes/commands/command_index.v1.json`;
  `docs/planning/coordination_tracking.md`;
  `docs/planning/design/design_tracking.md`;
  `docs/planning/prds/prd_tracking.md`;
  `docs/planning/tasks/task_tracking.md`

## Discovery Notes
- Current hotspot sizes:
  `query_coordination_handlers.py` `591` lines;
  `query_coordination_family.py` `392`;
  `repo_ops/query/coordination.py` `128`;
  `repo_ops/query/planning.py` `121`;
  `repo_ops/query/initiatives.py` `119`;
  `repo_ops/sync/planning_catalog.py` `409`;
  `repo_ops/sync/initiative_index.py` `540`.
- Current governed artifact sizes:
  `planning_catalog.v1.json` `1092237` bytes;
  `initiative_index.v1.json` `295669`;
  `traceability_index.v1.json` `295254`;
  `coordination_index.v1.json` `6235`.
- Current representative JSON payload sizes:
  `query planning --trace-id trace.refactor_umbrella_regression_and_growth_control --format json`
  about `18321` bytes;
  `query coordination --format json` about `5669` bytes;
  `query initiatives --initiative-status completed --trace-id trace.refactor_umbrella_regression_and_growth_control --format json`
  about `4783` bytes.
- Prior trace review:
  `lazy_planning_query_payload_emission` already removed the eager human-path serializer
  cost, so reopening that optimization would duplicate completed work instead of fixing a
  still-live root cause.
  `query_family_source_surface_alignment` explicitly deferred splitting
  `query_coordination_handlers.py` unless a later confirmation pass proved the family had
  become a live maintainability issue again. The current discovery confirms that it has.

## Findings Ledger
| Finding | Severity | Status | Affected Surfaces | Verification Target |
|---|---|---|---|---|
| `finding.001` | `high` | `resolved` | `core/python/src/watchtower_core/repo_ops/query/common.py`; `core/python/src/watchtower_core/repo_ops/query/initiatives.py`; `core/python/src/watchtower_core/repo_ops/query/planning.py`; `core/python/src/watchtower_core/repo_ops/query/coordination.py` | Initiative, planning, and coordination query services now share one explicit runtime helper for the duplicated filter and ranking mechanics while preserving service-specific term selection and ordering. |
| `finding.002` | `high` | `resolved` | `core/python/src/watchtower_core/cli/query_coordination_handlers.py`; `core/python/src/watchtower_core/cli/query_coordination_projection_handlers.py`; `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`; direct tests and command docs | The concentrated coordination-query handler file is now a compatibility facade and the current subcommands live in focused modules without breaking current imports or CLI behavior. |
| `finding.003` | `medium` | `resolved` | `docs/commands/core_python/watchtower_core_query_coordination.md`; `docs/commands/core_python/watchtower_core_query_planning.md`; `docs/commands/core_python/watchtower_core_query_initiatives.md`; `docs/commands/core_python/watchtower_core_query_authority.md`; `docs/commands/core_python/watchtower_core_query_tasks.md`; `docs/commands/core_python/watchtower_core_query_trace.md`; `core/python/tests/unit/test_cli.py`; `core/python/tests/unit/test_route_and_query_handlers.py` | The handler split stayed aligned with command docs and direct consumer tests so source-surface or compatibility drift did not replace the current hotspot. |
| `finding.004` | `medium` | `resolved` | `core/control_plane/contracts/acceptance/planning_query_efficiency_and_handler_modularity_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/planning_query_efficiency_and_handler_modularity_planning_baseline.v1.json`; `docs/planning/tasks/closed/validate_and_close_planning_query_efficiency_and_handler_modularity.md` | Acceptance-aware validation now covers the final closed validation task path and all five acceptance IDs instead of stopping at bootstrap-only evidence. |
| `finding.005` | `low` | `resolved` | `docs/planning/prds/planning_query_efficiency_and_coordination_handler_modularity.md`; `docs/planning/design/features/planning_query_efficiency_and_coordination_handler_modularity.md`; `docs/planning/design/implementation/planning_query_efficiency_and_coordination_handler_modularity.md`; `docs/planning/decisions/planning_query_efficiency_and_coordination_handler_modularity_direction.md` | Front matter `updated_at` values and Record Metadata `Updated At` lines now stay aligned across the traced planning corpus. |
| `finding.006` | `low` | `resolved` | `docs/planning/decisions/planning_query_efficiency_and_coordination_handler_modularity_direction.md` | The decision record now satisfies document-semantics validation for explained bullets in `Applied References and Implications`. |

## Assumptions and Constraints
- Preserve current query payload schemas, command IDs, default browse semantics, and
  result ordering.
- Use the current planning catalog, initiative index, and coordination index as existing
  governed authorities; do not add a new index family unless confirmation work proves the
  runtime redesign is insufficient.
- Preserve compatibility imports for the legacy `query_coordination_handlers.py` surface
  because direct tests and internal consumers import it explicitly.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: constrains runtime placement
  and validation entrypoints.
- `docs/standards/governance/traceability_standard.md`: constrains the traced planning
  chain and closeout alignment.
- `docs/standards/documentation/command_md_standard.md`: requires command-doc source
  surfaces to stay aligned with the runtime ownership model.
- `docs/standards/data_contracts/command_index_standard.md`: constrains any
  machine-readable source-surface changes that become visible to command discovery.

## Proposed Technical Approach
- Add one shared query-projection helper layer for the common filtering and ranking
  mechanics used by planning, initiative, and coordination searches.
- Refactor the three query services to consume that helper with explicit service-specific
  term builders.
- Split the coordination-query handler hotspot into focused handler modules and keep the
  legacy module as a compatibility facade.
- Reconcile command docs, direct tests, trackers, acceptance, and evidence in the same
  change set.

## Work Breakdown
1. Publish the coverage map, findings ledger, and accepted redesign direction under this
   single trace, then create bounded execution tasks for query-model refactoring,
   handler-family modularity, and final validation/closeout.
2. Implement the shared projection-search helper and refactor initiative, planning, and
   coordination query services onto it with targeted regressions.
3. Split the concentrated coordination-query handler surface into focused modules behind a
   compatibility facade, then reconcile command docs and direct consumers.
4. Run targeted validation, full validation, post-fix review, second-angle confirmation,
   and adversarial confirmation; reopen the loop if any new same-theme issue appears.

## Risks
- A too-generic search abstraction could obscure the differences between planning and
  initiative term selection.
- A handler split could leave stale source-surface references or compatibility drift in
  docs and tests if the reconciliation is incomplete.
- The review may still conclude that a later governed data-model redesign is warranted,
  but that should be recorded as explicit follow-up rather than smuggled into this trace
  without evidence.

## Validation Plan
- Run targeted pytest for:
  `tests/unit/test_route_and_query_handlers.py`;
  `tests/unit/test_cli_planning_query_commands.py`;
  `tests/unit/test_planning_catalog_sync.py`;
  `tests/unit/test_coordination_index_sync.py`;
  `tests/unit/test_initiative_index_sync.py`;
  `tests/unit/test_cli.py`;
  and any new focused query-service tests added by the redesign.
- Run `watchtower-core validate acceptance --trace-id trace.planning_query_efficiency_and_handler_modularity --format json`.
- Run `watchtower-core sync all --write --format json`, `watchtower-core validate all --format json`,
  `pytest -q`, `ruff check .`, and `python -m mypy src/watchtower_core`.
- Re-run confirmation from a different angle by checking command docs, query output, loader
  consumers, and the final closed-state planning surfaces.

## References
- docs/planning/prds/lazy_planning_query_payload_emission.md
- docs/planning/design/features/query_family_source_surface_alignment.md
- docs/planning/design/implementation/refactor_umbrella_regression_and_growth_control.md

## Fixes Applied
- Added the shared projection-search helper in
  `core/python/src/watchtower_core/repo_ops/query/common.py` and refactored
  `planning.py`, `initiatives.py`, and `coordination.py` to consume it with
  explicit service-owned query-term builders.
- Split the coordination-query runtime boundary into
  `query_coordination_projection_handlers.py` and
  `query_coordination_lookup_handlers.py`, while reducing
  `query_coordination_handlers.py` to a compatibility facade and keeping
  `query_coordination_family.py` as the authoritative registrar.
- Added targeted regression coverage in
  `core/python/tests/unit/test_projection_search_common.py` and reconciled the
  direct CLI or handler tests in `test_route_and_query_handlers.py` and
  `test_cli.py`.
- Refreshed the affected query command pages, the repository-path index, the
  planning trackers, the planning catalog, the initiative or coordination views,
  the acceptance contract, and the evidence ledger in the same change set.
- Preserved the current governed planning catalog, initiative index, and
  coordination index families instead of adding a new planning-summary artifact
  family; the accepted redesign stayed in the runtime layer only.

## Post-Remediation State
- Hotspot sizes after the redesign:
  `query_coordination_handlers.py` `25` lines;
  `query_coordination_projection_handlers.py` `354`;
  `query_coordination_lookup_handlers.py` `243`;
  `repo_ops/query/common.py` `212`;
  `repo_ops/query/planning.py` `61`;
  `repo_ops/query/initiatives.py` `61`;
  `repo_ops/query/coordination.py` `73`.
- Same-theme concentration remains visible but is now bounded by coherent
  runtime seams rather than one mixed handler file plus three duplicated search
  implementations.

## Validation and Review Results
- Targeted validation passed for the shared query helper, the planning-catalog
  and coordination sync consumers, the direct CLI or handler suites, acceptance
  reconciliation, full repo validation, `pytest -q`, `ruff check .`, and
  `python -m mypy src/watchtower_core`.
- The first closeout-oriented reruns reopened the loop on three same-theme drift
  issues: decision-record explained-bullet formatting, bootstrap-only
  acceptance or evidence coverage, and planning-doc metadata timestamp drift.
  Each issue was repaired in the same trace before the final reruns.
- Post-fix review on the planning surfaces now shows the split handler modules,
  the shared query helper, the closed validation task path, one passed evidence
  ledger, and the expected related paths for the trace.

## Independent Confirmation Results
- Discovery-surface confirmation found the shared search helper referenced only
  by the three in-scope query services plus its direct helper test, which
  confirms that the duplicated runtime search logic no longer lives in several
  service files.
- `watchtower-core query commands --query "query planning" --format json` and
  `watchtower-core query commands --query "query coordination" --format json`
  continue to resolve the current command family through
  `core/python/src/watchtower_core/cli/query_coordination_family.py`, which is
  the intended registrar authority after the split.
- `watchtower-core query paths --query query_coordination_handlers --format json`,
  `--query query_coordination_projection_handlers`, and
  `--query query_coordination_lookup_handlers` all resolve the expected current
  files with updated summaries, which confirms that repository-path discovery
  stayed aligned with the redesign.

## Adversarial Confirmation Results
- A pre-closeout adversarial probe with
  `watchtower-core closeout initiative --trace-id trace.planning_query_efficiency_and_handler_modularity --initiative-status completed --closure-reason "Adversarial probe before task closeout" --format json`
  failed with the expected open-task error while the validation task was still
  non-terminal.
- After the validation task closed, the coordination projection moved to
  `current_phase: closeout`, `open_task_count: 0`, and the recommended next step
  became the initiative-closeout command, which confirmed that the lifecycle
  boundary stayed deterministic before the final write.
- No additional same-theme issue appeared after the closeout gate, the
  discovery-surface confirmation, and the rerun validation stack were applied
  together.

## Commit and Pass-History Review
- The redesign is a root-cause repair, not another disconnected bounded
  umbrella. The earlier umbrella trace already identified the live remaining
  runtime redesign debt as `RF-PY-004`, and this trace consumes that debt
  directly without creating a new governed planning family or reopening older
  lazy-payload work.
- The current change reduces the live runtime hotspot count by collapsing three
  duplicated query-search implementations into one helper and by replacing the
  `591`-line handler hotspot with one compatibility facade plus two focused
  runtime modules.
- The review did not find new evidence that the governed planning catalog schema
  itself is the root bottleneck. A broader planning-model or index redesign
  would add control-plane surface area without current proof that the data model
  is the next constraint.

## Final Stop-Condition Evidence
- The validation task is now terminal at
  `docs/planning/tasks/closed/validate_and_close_planning_query_efficiency_and_handler_modularity.md`.
- The initiative closeout was written with `initiative_status: completed`,
  `open_task_count: 0`, and `closed_at: 2026-03-13T23:40:00Z`.
- The current stop condition for this trace is a closed task set, one passed
  evidence ledger, zero acceptance issues, and a closed initiative after
  repeated confirmation passes with no new actionable issue under the same
  redesign theme.
