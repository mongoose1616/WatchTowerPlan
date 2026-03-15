---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_program"
title: "Structural Rewrite Program Implementation Plan"
summary: "Records the completed Phase 0 and Phase 1 package, the Phase 2 gate outcome, the bounded artifact-role registry pilot, the Phase 3 command companion slice and outcome review, the closed first Phase 4 slice and outcome review, the approved closeout-coordination entry review, the landed bounded Phase 4 closeout coordination sync-reuse slice, the closed outcome review for that slice, the approved closeout-tracking entry review, the landed bounded closeout-tracking refresh-boundary slice, the closed final outcome review for that slice, and the explicit structural-rewrite program closeout decision."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T09:55:03Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/standards/"
  - "docs/planning/"
  - "core/control_plane/"
  - "core/python/"
aliases:
  - "rewrite implementation plan"
  - "phase 2 gate record"
  - "structural rewrite checkpoint"
---

# Structural Rewrite Program Implementation Plan

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_program`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-15T09:55:03Z`

## Summary
Records the completed Phase 0 and Phase 1 rewrite package, closes the Phase 2 entry gate explicitly, records the bounded artifact-role registry pilot outcome, closes the Phase 3 entry review explicitly, records the first bounded Phase 3 command companion normalization slice and its outcome review, closes the Phase 4 shared-projection entry review explicitly, records the implemented first bounded Phase 4 planning projection snapshot slice and its closed outcome review, closes the Phase 4 closeout-coordination entry review explicitly, lands one bounded Phase 4 closeout coordination sync-reuse slice, closes that slice through explicit outcome review, closes the Phase 4 closeout-tracking entry review explicitly, lands the bounded closeout-tracking refresh-boundary slice, closes its final outcome review explicitly, and records the structural-rewrite program closeout decision.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)

## Scope Summary
- Complete Phase 0 by refreshing the live baseline and hotspot inventory, publishing rewrite governance standards, publishing the public planning-authority parity contract, publishing the slice-control package model, and fixing one Phase 2 pilot family.
- Complete Phase 1 by classifying critical surfaces, mapping history and compatibility consumers, classifying compatibility surfaces by support level and retention reason, and publishing no-go conditions, rollback expectations, and Phase 2 entry conditions.
- Record the Phase 2 entry review outcome, the chosen storage shape, and the bounded first-slice boundary.
- Hand the approved Phase 2 slice to [structural_rewrite_artifact_role_registry_pilot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md).
- Stop broader implementation after the pilot review and open one explicit Phase 3 entry package instead of a second Phase 2 slice.
- After the Phase 3 entry review closes, hand the trace to one bounded command companion normalization slice instead of broader Phase 3 rollout.
- After the Phase 3 slice outcome review closes cleanly, hand the trace to one bounded Phase 4 shared-projection entry package instead of direct Phase 4 implementation.
- After the Phase 4 entry review closes cleanly, implement one bounded Phase 4 planning projection snapshot slice, close that slice through an explicit outcome review, close the successor closeout-coordination entry review explicitly, implement one bounded closeout coordination sync-reuse slice, close that slice through explicit outcome review, close the successor closeout-tracking entry review explicitly, land one bounded closeout-tracking refresh-boundary slice, close its explicit outcome review, and then end the trace through one explicit program-closeout decision instead of broader rollout.
- Exclude broader Phase 2 rollout, history relocation, compatibility retirement, runtime behavior changes, and command-authority or planning-authority rewrites.

## Assumptions and Constraints
- The live repository state and accepted repo-native documents outrank any stale external rewrite assumptions.
- The five current planning-authority answers remain the public machine boundary unless a separate accepted decision changes them.
- Any later pilot family must declare its authored truth, derived outputs, and rollback path before implementation begins.
- The Phase 2 gate approval authorizes only one additive, read-only artifact-role metadata slice backed by a dedicated registry family.
- The Phase 3 entry review may authorize only one rollback-safe command companion normalization slice and may not be treated as standing approval for broader command-authority rewrites.
- A passing Phase 3 outcome review may authorize only one bounded later-phase entry package and may not be treated as standing approval for Phase 4 implementation.
- A passing Phase 4 entry review may authorize only one bounded private planning projection snapshot slice and may not be treated as standing approval for broader Phase 4 rollout.
- A passing Phase 4 slice outcome review may authorize only one bounded successor checkpoint and may not be treated as standing approval for broader Phase 4 or later-phase implementation.

## Current-State Context
- The live rewrite checkpoint remains healthy under `./core/python/.venv/bin/watchtower-core doctor --format json` and `./core/python/.venv/bin/watchtower-core validate all`.
- `./core/python/.venv/bin/watchtower-core query authority --domain planning --format json` still resolves the same five public planning questions to the same canonical machine surfaces.
- The first bounded Phase 3 slice has already reconciled the root command page plus the bounded `doctor`, `sync`, and `validate` command docs to the existing command-index implementation paths, and `./core/python/.venv/bin/watchtower-core sync command-index --format json` plus `./core/python/.venv/bin/python -m pytest core/python/tests/unit/test_command_index_sync.py` keep that boundary green.
- The Phase 4 entry review passed, reaffirmed the five public planning-authority answers plus the private-graph guardrail, named the full coordination-sync and mutation-path consumer boundary, and approved one private trace-scoped planning projection snapshot slice as the first bounded checkpoint.
- That first Phase 4 slice now exists as `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py`, `InitiativeIndexSyncService` plus `PlanningCatalogSyncService` consume that shared private snapshot, and the bounded sync plus closeout suite passed alongside green doctor, validation, authority, coordination, and planning query reruns.
- The closed outcome review for that slice kept the shared helper private, reaffirmed unchanged public planning parity, and named the next bounded checkpoint as a closeout-coordination entry package around the remaining direct `InitiativeCloseoutService` rebuild outlier.
- That closeout-coordination entry review then passed. The approved post-traceability closeout seam landed by reusing `CoordinationSyncService` for the five shared planning and coordination outputs while keeping the PRD, decision, and design tracking outputs direct for that slice.
- The closeout coordination sync-reuse outcome review has now also passed, reaffirmed that shared seam and result-contract boundary, and named the remaining direct PRD, decision, and design tracking refresh step as the next bounded entry question.
- The closeout-tracking entry review has now also passed, and the bounded closeout-tracking refresh-boundary slice has now landed by routing the remaining tracker refresh step through one private closeout-local helper while preserving the approved shared seam and explicit closeout result-contract fields.
- The final controlling surface was [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md), and that closed review recorded the explicit program-closeout decision instead of opening broader Phase 4 rollout or later-phase work.
- The rewrite-relevant hotspot picture now centers on `planning_projection_snapshot.py` (`513`), `document_semantics.py` (`494`), `task_lifecycle.py` (`492`), `acceptance.py` (`471`), `workflow_index.py` (`463`), `planning_scaffold_specs.py` (`431`), `loader.py` (`431`), and `planning_projection_serialization.py` (`419`) rather than the older hotspot examples from earlier rewrite prose.

## Internal Standards and Canonical References Applied
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): Phase 1 classifications, support levels, and retention reasons must use one controlled model.
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the Phase 2 gate and bounded slice must use the repo-native checkpoint package and parity contract.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the rewrite needs a traced planning chain, evidence artifacts, and active task ownership.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the review and follow-up checkpoints must remain task-backed instead of implicit.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the public planning-authority parity contract must preserve the live authority-map answers.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): the parity boundary is captured as a machine-readable contract instead of prose-only promises.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): baseline refresh, checkpoint completion, and readiness need durable evidence.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): the rewrite package still needs inspect, refresh, rebuild, validate, and record discipline.

## Proposed Technical Approach
- Bootstrap the rewrite as one traced initiative with the minimum durable planning, contract, ledger, and task surfaces required by the live repo's governance model.
- Publish two rewrite-specific governance standards:
  - one for four-axis classification, compatibility support levels, and retention reasons
  - one for the public parity boundary, slice-control package, authored-versus-derived declarations, checkpoints, no-go conditions, and rollback expectations
- Use this implementation plan as the human Phase 0 and Phase 1 package. It carries the live baseline, hotspot inventory, critical-surface classification, consumer maps, compatibility classifications, and the Phase 2 pilot-family decision.
- Materialize the public planning-authority parity contract as an acceptance contract and use one migration record plus one validation-evidence artifact as the machine-readable checkpoint pair for the completed Phase 0 and Phase 1 package.
- Fix Phase 2 to the artifact-role metadata family only, choose a small dedicated registry as the first storage shape, and route implementation through one dedicated slice plan instead of broadening the main package.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Public planning authorities | `core/control_plane/registries/authority_map/authority_map.v1.json`; `core/control_plane/indexes/coordination/coordination_index.v1.json`; `core/control_plane/indexes/planning/planning_catalog.v1.json`; `core/control_plane/indexes/initiatives/initiative_index.v1.json`; `core/control_plane/indexes/tasks/task_index.v1.json`; `core/control_plane/indexes/traceability/traceability_index.v1.json`; planning query command docs and trackers | Preserve the current five planning answers and classify them explicitly before later slices touch internals. |
| Runtime hotspot inventory | `core/python/src/watchtower_core/repo_ops/task_lifecycle.py`; `core/python/src/watchtower_core/control_plane/loader.py`; `core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py`; `core/python/src/watchtower_core/repo_ops/planning_scaffold_specs.py`; `core/python/src/watchtower_core/repo_ops/planning_bootstrap_support.py`; `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py` | Refresh the live hotspot picture and reject stale rewrite assumptions before choosing a pilot or later hotspot slice. |
| Compatibility surfaces | `core/python/src/watchtower_core/query/`; `core/python/src/watchtower_core/sync/`; `core/python/src/watchtower_core/validation/all.py`; `core/python/src/watchtower_core/cli/query_coordination_handlers.py`; `core/python/tests/integration/test_control_plane_artifacts.py`; `core/python/tests/unit/test_document_semantics_validation.py`; `core/python/tests/unit/test_cli_query_commands.py`; `core/control_plane/contracts/compatibility/core_python_workspace_compatibility.v1.json` | Separate intentional supported boundaries from transitional facades and historical path markers. |
| Historical planning surfaces | `docs/planning/prds/decision_supersession_and_regression_evidence_alignment.md`; `docs/planning/design/features/decision_supersession_and_regression_evidence_alignment.md`; `docs/planning/design/implementation/decision_supersession_and_regression_evidence_alignment.md`; `docs/planning/decisions/decision_supersession_and_regression_evidence_alignment_direction.md` | Confirm that current in-place historical records already use repo-native history signaling and should not be relocated casually. |
| Rewrite control package | `docs/standards/governance/rewrite_surface_classification_standard.md`; `docs/standards/governance/rewrite_execution_control_standard.md`; `core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_program_phase0_phase1_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_program_phase0_phase1_baseline.v1.json`; rewrite tasks | Publish the durable standards, contract, evidence, transition record, and gate surfaces that later phases must obey. |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.structural_rewrite_program.001` | `high` | `resolved` | required baseline commands; authority map; coordination query | The required baseline commands reran cleanly and confirmed the live repo is healthy and still exposes the same five planning-authority answers. |
| `finding.structural_rewrite_program.002` | `medium` | `resolved` | rewrite hotspot assumptions; `core/python/src/watchtower_core/` live inventory | The current hotspot inventory differs materially from older rewrite examples; the plan now treats previous counts as historical review context only and records live file sizes explicitly. |
| `finding.structural_rewrite_program.003` | `high` | `resolved` | planning traceability; task handling; coordination start-here surfaces | The rewrite is anchored in a full traced planning chain plus explicit review and execution tasks instead of prose-only execution. |
| `finding.structural_rewrite_program.004` | `medium` | `resolved` | compatibility namespaces, facades, test markers, historical planning records | Phase 1 classification confirms that several surfaces that look like cleanup debt are still intentional supported boundaries or historical context and therefore need explicit retention reasons instead of blanket retirement. |

## Critical Surface Classification
| Surface Family | Lifecycle Status | Authority Role | Storage or Placement Class | Compatibility Support Level | Notes |
|---|---|---|---|---|---|
| `coordination_index` plus `query coordination` plus `coordination_tracking.md` | `active` | `canonical_machine_answer` | `active_family_location` | `n/a` | Current-state start-here answer; the bounded pilot may classify it but may not replace it. |
| `planning_catalog` plus `query planning` | `active` | `canonical_machine_answer` | `active_family_location` | `n/a` | Deep trace-linked planning answer; later rewrite internals may change only behind this contract. |
| `initiative_index` plus `query initiatives` plus `initiative_tracking.md` | `active` | `canonical_machine_answer` | `active_family_location` | `n/a` | Compact initiative-family and history browse answer. |
| `task_index` plus `query tasks` plus `task_tracking.md` | `active` | `canonical_machine_answer` | `active_family_location` | `n/a` | Authoritative task execution and dependency answer. |
| `traceability_index` plus `query trace` | `active` | `canonical_machine_answer` | `active_family_location` | `n/a` | Durable trace-linked source join and initiative closeout answer. |
| `authority_map` plus `query authority --domain planning` | `active` | `discovery_index` | `active_family_location` | `n/a` | Canonical lookup policy for the planning questions above. |
| CLI registry plus parser tree | `active` | `authored_authority` | `active_family_location` | `n/a` | Remains the machine authority for command presence and hierarchy; not an allowed first pilot family. |
| Command index plus command docs | `active` | `generated_projection` | `active_family_location` | `n/a` | Supporting discovery surfaces derived from the live command authority model. |
| `watchtower_core.query/` namespace | `active` | `compatibility_surface` | `compatibility_namespace_or_marker` | `supported` | Current boundary-layer namespace with explicit supported-import guidance and compatibility tests. |
| `watchtower_core.sync/` namespace | `active` | `compatibility_surface` | `compatibility_namespace_or_marker` | `supported` | Current boundary-layer namespace for explicit sync wrappers with supported-import guidance. |
| `watchtower_core.validation.all` | `active` | `compatibility_surface` | `compatibility_namespace_or_marker` | `transitional` | Aggregate validation wrapper retained for compatibility while repo-local aggregate validation stays under `repo_ops.validation`. |
| `query_coordination_handlers.py` compatibility facade | `active` | `compatibility_surface` | `compatibility_namespace_or_marker` | `transitional` | Thin facade retained after the handler split; current tests still import it directly. |
| Historical test marker files | `active` | `compatibility_surface` | `compatibility_namespace_or_marker` | `supported` | `test_control_plane_artifacts.py`, `test_document_semantics_validation.py`, and `test_cli_query_commands.py` remain current compatibility markers for planning references and repository-path discoverability. |
| Cancelled rewrite-adjacent planning chain with `authority: historical` | `deprecated` | `historical_record` | `active_family_location` | `n/a` | Current repo-native in-place historical model; not a relocation candidate in the bounded pilot. |

## History and Compatibility Consumer Maps
| Candidate Surface | Current Consumers | Retention Reason | Cleanup Preconditions |
|---|---|---|---|
| `watchtower_core.query/` boundary namespace | `core/python/src/watchtower_core/query/README.md`; `core/python/README.md`; `core/python/tests/unit/test_repo_ops_compatibility.py`; foundations-adjacent planning docs that describe the namespace as a live boundary layer | `import_stability`; `boundary_clarity` | Direct consumer audit outside compatibility tests, updated runtime-boundary docs, and an explicit accepted migration decision. |
| `watchtower_core.sync/` boundary namespace | `core/python/src/watchtower_core/sync/README.md`; `core/python/README.md`; `core/python/tests/unit/test_repo_ops_compatibility.py`; runtime-boundary planning docs | `import_stability`; `boundary_clarity` | Same as query namespace: prove that wrapper imports are no longer needed and keep boundary docs coherent. |
| `watchtower_core.validation.all` wrapper | `core/python/tests/unit/test_repo_ops_compatibility.py`; guardrail messaging in `core/python/src/watchtower_core/validation/__init__.py`; operator expectations around explicit aggregate-validation wrapper imports | `import_stability`; `migration_window` | Remove direct imports, refresh compatibility tests, and confirm aggregate validation is intentionally repo-local only. |
| `query_coordination_handlers.py` facade | `core/python/tests/unit/test_cli.py`; `core/python/tests/unit/test_route_and_query_handlers.py`; historical planning and task docs that still cite the old path | `import_stability`; `historical_context` | Shift direct test imports to stable family surfaces or behavior assertions, then audit historical planning references before retirement. |
| `test_control_plane_artifacts.py` marker | `core/python/tests/integration/README.md`; repository-path index; more than 300 planning references recorded by the validation-hotspot trace | `repository_path_continuity`; `discoverability` | Rewrite surviving planning references or broaden them to the focused suite family without breaking query-path navigation. |
| `test_document_semantics_validation.py` marker | `core/python/tests/unit/README.md`; repository-path index; more than 100 planning references recorded by the validation-hotspot trace | `repository_path_continuity`; `discoverability` | Historical references and path-index discoverability must stay intact before retirement. |
| `test_cli_query_commands.py` marker | `core/python/tests/unit/README.md`; typed-query and standards-family planning traces; repository-path index | `repository_path_continuity`; `discoverability` | Historical planning references and task dry-run discoverability must move to the focused CLI suite family first. |
| Cancelled historical planning chain under `trace.decision_supersession_and_regression_evidence_alignment` | explicit `query planning --trace-id ...` history lookups; planning catalog; PRD or design or decision trackers; traceability history | `historical_context` | None for the bounded pilot. Current action is retain in place with existing historical signaling. |

## Compatibility Support Classification
| Surface | Support Level | Retention Reason | Current Retention Justification |
|---|---|---|---|
| `core/control_plane/contracts/compatibility/core_python_workspace_compatibility.v1.json` | `supported` | `public_contract_preservation` | Published compatibility contract for the governed Python workspace and command boundary. |
| `core/python/src/watchtower_core/query/` | `supported` | `import_stability`; `boundary_clarity` | The repo still documents the namespace as a supported boundary-layer import surface. |
| `core/python/src/watchtower_core/sync/` | `supported` | `import_stability`; `boundary_clarity` | Same as query namespace for explicit sync wrappers. |
| `core/python/src/watchtower_core/validation/all.py` | `transitional` | `import_stability`; `migration_window` | Aggregate validation is explicitly repo-local, but the wrapper still exists for compatibility coverage. |
| `core/python/src/watchtower_core/cli/query_coordination_handlers.py` | `transitional` | `import_stability`; `historical_context` | The file is already a thin facade after the handler split and should not be treated as a long-term authority surface. |
| `core/python/tests/integration/test_control_plane_artifacts.py` | `supported` | `repository_path_continuity`; `discoverability` | The file is a deliberate compatibility marker surfaced through README inventory and planning history. |
| `core/python/tests/unit/test_document_semantics_validation.py` | `supported` | `repository_path_continuity`; `discoverability` | Same supported compatibility-marker role as the integration hotspot file. |
| `core/python/tests/unit/test_cli_query_commands.py` | `supported` | `repository_path_continuity`; `discoverability` | Historical planning and query-path continuity still rely on the marker file. |

## Phase 2 Pilot Family Selection
### Chosen Pilot
- `artifact-role metadata family`

### Approved first-slice storage shape
- `small dedicated registry`

### Rationale
- The pilot is additive and can be kept behind existing public planning and command authority boundaries.
- The authored truth is already explicit after Phase 1 classification: the pilot materializes that classification into a small governed metadata family instead of inventing a new public answer.
- The family can be validated deterministically against the Phase 1 classification tables without changing `query authority`, planning indexes, command presence, or runtime behavior.
- The rollback path is simple: remove the additive metadata family and its companions without restoring a replaced public surface.
- A dedicated registry is safer than embedding additive metadata inside one existing governed family because the current classification spans multiple public planning surfaces and should not imply that any one of those families owns the rewrite metadata canonically.

### First-slice boundary
- Publish an additive `artifact_role_registry` family under `core/control_plane/registries/artifact_roles/`.
- Limit entries to the six public planning-authority surfaces already classified in Phase 1:
  - `surface.planning.current_state`
  - `surface.planning.trace_catalog`
  - `surface.planning.initiative_family_view`
  - `surface.planning.task_execution_state`
  - `surface.planning.traceability_join`
  - `surface.planning.authority_lookup`
- Keep runtime consumers out of scope. The slice may publish only schema, registry, validator, catalog, artifact-type, example, checkpoint, and task surfaces.

## Work Breakdown
1. Bootstrap the rewrite trace with the PRD, feature design, implementation plan, acceptance contract, migration record, validation-evidence artifact, and explicit task chain.
2. Publish the rewrite classification and execution-control standards, refresh the live baseline and hotspot inventory, and fix the public planning-authority parity contract to the current five planning questions.
3. Complete Phase 1 classification by publishing the critical-surface table, history or compatibility consumer maps, support-level classifications, retention reasons, and the chosen Phase 2 pilot family.
4. Review the Phase 2 entry package, choose the dedicated-registry storage shape, and record the bounded approval outcome.
5. Publish the dedicated slice plan, dedicated migration record, and dedicated validation-evidence artifact for the first slice.
6. Publish the additive artifact-role registry family and its schema, validator, artifact-type, schema-catalog, and example companions.
7. Sync the derived planning surfaces, validate the repo, close the pilot follow-up review explicitly, and hand control to the Phase 3 entry-review task.

## No-Go Conditions
- Do not start Phase 2 implementation before `task.structural_rewrite_program.phase2_entry_review.003` records an explicit approval outcome.
- Do not change any planning-authority answer returned by `watchtower-core query authority --domain planning --format json` in this trace.
- Do not move, delete, or retire a historical or compatibility surface in this trace.
- Do not choose more than one Phase 2 pilot family.
- Do not choose command authority, public planning projections, or live sync-family selection as the first pilot.
- Do not introduce `archived` as a lifecycle label or create a new rewrite-only archive area.
- Do not let the first slice drive live query routing, sync selection, validator dispatch, command presence, or planning-boundary changes.

## Rollback Expectations
- Any later pilot slice must preserve the current public planning-authority answers until parity evidence says otherwise.
- Any later pilot slice must record the old and new authority or builder in its checkpoint package and keep the previous path or builder restorable.
- Any later compatibility cleanup slice must keep repository-path discoverability intact until all historical references are rewritten or intentionally broadened.
- If a later pilot family creates dual truth, rollback means removing the new metadata family and reverting consumers to the previous explicit source rather than widening the control surface.
- For the bounded artifact-role registry slice, rollback means removing the new schema, registry, validator, artifact-type, schema-catalog, example, and slice-specific checkpoint surfaces, then rebuilding derived planning indexes with no public parity changes required.

## Phase 2 Gate Outcome
- `Review Task`: [review_structural_rewrite_program_phase2_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_program_phase2_entry_package.md)
- `Outcome`: approved for exactly one bounded slice.
- `Approved Storage Shape`: small dedicated registry under `core/control_plane/registries/artifact_roles/`.
- `Approval Guardrails`:
  - keep the slice additive and read-only
  - keep public planning-authority answers unchanged
  - keep runtime routing, sync selection, validator dispatch, command authority, and planning-boundary behavior unchanged
  - stop after the first bounded slice with a successor review task

## Active Control Package
- `Program Plan`: [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- `Slice Plan`: [structural_rewrite_artifact_role_registry_pilot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md)
- `Acceptance Contract`: [structural_rewrite_program_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json)
- `Historical Gate Migration`: [structural_rewrite_program_phase0_phase1_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_program_phase0_phase1_ready.v1.json)
- `Historical Gate Evidence`: [structural_rewrite_program_phase0_phase1_baseline.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_program_phase0_phase1_baseline.v1.json)
- `Slice Migration`: [structural_rewrite_artifact_role_registry_pilot.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_artifact_role_registry_pilot.v1.json)
- `Slice Evidence`: [structural_rewrite_artifact_role_registry_pilot.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_artifact_role_registry_pilot.v1.json)
- `Pilot Review Task`: [review_structural_rewrite_artifact_role_registry_pilot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_artifact_role_registry_pilot_outcome.md)
- `Phase 3 Entry Package`: [structural_rewrite_phase3_command_authority_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_authority_entry.md)
- `Phase 3 Slice Plan`: [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- `Phase 3 Entry Migration`: [structural_rewrite_phase3_command_companion_source_surface_normalization_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization_ready.v1.json)
- `Phase 3 Entry Evidence`: [structural_rewrite_phase3_command_companion_source_surface_normalization_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase3_command_companion_source_surface_normalization_ready.v1.json)
- `Closed Phase 3 Review Task`: [review_structural_rewrite_phase3_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_entry_package.md)
- `Phase 3 Slice Migration`: [structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json)
- `Phase 3 Slice Evidence`: [structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json)
- `Closed Phase 3 Implementation Task`: [implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- `Closed Phase 3 Outcome Review Task`: [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)
- `Phase 4 Entry Package`: [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- `Phase 4 Entry Migration`: [structural_rewrite_phase4_shared_projection_entry_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_shared_projection_entry_ready.v1.json)
- `Phase 4 Entry Evidence`: [structural_rewrite_phase4_shared_projection_entry_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_shared_projection_entry_ready.v1.json)
- `Closed Phase 4 Review Task`: [review_structural_rewrite_phase4_shared_projection_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_shared_projection_entry_package.md)
- `Phase 4 Slice Plan`: [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- `Phase 4 Slice Ready Migration`: [structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json)
- `Phase 4 Slice Ready Evidence`: [structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json)
- `Phase 4 Slice Migration`: [structural_rewrite_phase4_planning_projection_snapshot.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot.v1.json)
- `Phase 4 Slice Evidence`: [structural_rewrite_phase4_planning_projection_snapshot.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot.v1.json)
- `Closed Phase 4 Implementation Task`: [implement_structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_planning_projection_snapshot.md)
- `Closed Phase 4 Outcome Review Task`: [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md)
- `Next Phase 4 Entry Package`: [structural_rewrite_phase4_closeout_coordination_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md)
- `Next Phase 4 Entry Migration`: [structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json)
- `Next Phase 4 Entry Evidence`: [structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json)
- `Closed Next Phase 4 Review Task`: [review_structural_rewrite_phase4_closeout_coordination_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md)
- `Historical Phase 4 Closeout Slice Plan`: [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- `Historical Phase 4 Closeout Slice Ready Migration`: [structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json)
- `Historical Phase 4 Closeout Slice Ready Evidence`: [structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json)
- `Historical Phase 4 Closeout Slice Migration`: [structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json)
- `Historical Phase 4 Closeout Slice Evidence`: [structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json)
- `Closed Historical Phase 4 Closeout Implementation Task`: [implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- `Closed Historical Phase 4 Closeout Outcome Review Task`: [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)
- `Historical Phase 4 Tracking Entry Package`: [structural_rewrite_phase4_closeout_tracking_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_entry.md)
- `Historical Phase 4 Tracking Entry Migration`: [structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json)
- `Historical Phase 4 Tracking Entry Evidence`: [structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json)
- `Closed Historical Phase 4 Tracking Review Task`: [review_structural_rewrite_phase4_closeout_tracking_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md)
- `Final Phase 4 Tracking Slice Plan`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- `Final Phase 4 Tracking Slice Ready Migration`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json)
- `Final Phase 4 Tracking Slice Ready Evidence`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json)
- `Final Phase 4 Tracking Slice Migration`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_refresh_boundary.v1.json)
- `Final Phase 4 Tracking Slice Evidence`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary.v1.json](/home/j/WatchTowerPlan/core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_refresh_boundary.v1.json)
- `Closed Final Phase 4 Tracking Implementation Task`: [implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- `Closed Final Phase 4 Tracking Outcome Review Task`: [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md)

## Pilot Review Outcome
- `Decision`: passed.
- `Phase 2 conclusion`: the first bounded slice proved the additive metadata-family pattern cleanly enough that broader rewrite work no longer needs to stay blocked at the pilot-review checkpoint.
- `Next boundary`: do not open a second broader Phase 2 slice. The next safe step is the Phase 3 entry package for command-authority normalization.

## Phase 3 Entry Review Outcome
- `Decision`: passed for one bounded Phase 3 slice only.
- `Current command-authority boundary`: unchanged. `registry.py` plus `parser.py` remain the only accepted machine authority for command presence and hierarchy.
- `Approved first slice`: [structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md)
- `Classification sufficiency`: no additional command-adjacent workflow, route, or compatibility classification addendum is required for the first slice because it stays inside already-classified command companion surfaces.
- `Entry checkpoint hard stop`: [implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md)

## Phase 3 Slice Outcome
- `Decision`: implemented as one bounded companion-only slice.
- `Bounded doc set`: the root command page's primary Source Surface section plus the `23` affected `doctor`, `sync`, and `validate` command docs now align with the parser-owned or family-owned implementation paths already published in the command index.
- `Drift guard`: `core/python/src/watchtower_core/repo_ops/sync/command_index.py` now fails closed when a companion command doc Command table or primary Source Surface entry drifts from the registry-backed implementation path, and `core/python/tests/unit/test_command_index_sync.py` covers that guard directly.
- `Outcome-review handoff`: [review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md)

## Phase 3 Outcome Review Outcome
- `Decision`: passed.
- `Docs-plus-index parity`: held through the closed review, with the root command page plus the bounded `doctor`, `sync`, and `validate` command docs still aligned to the command-index implementation paths.
- `Command-authority boundary`: unchanged. `registry.py` plus `parser.py` remain the only accepted machine authority for command presence and hierarchy.
- `Public planning parity`: unchanged. The five planning-authority answers remain the same after the bounded Phase 3 slice.
- `Next boundary`: do not open broader Phase 3 rollout. Open the bounded Phase 4 shared-projection entry package and keep Phase 4 implementation blocked until its entry review closes explicitly.

## Phase 4 Entry Review Outcome
- `Decision`: passed for one bounded Phase 4 slice only.
- `Public planning boundary`: unchanged. The five planning-authority answers remain the same after the entry review closes.
- `Private internal-graph boundary`: reaffirmed. Any internal planning graph introduced by the first Phase 4 slice remains a private runtime detail rather than a new public artifact family.
- `Consumer boundary`: explicit. The approved boundary now names the coordination-sync ordering, the task lifecycle and planning scaffold write paths that call `CoordinationSyncService`, the direct initiative-closeout rebuild path, and the touched tracker emitters.
- `Approved first slice`: [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
- `Exact seam`: one private trace-scoped planning projection snapshot consumed by `InitiativeIndexSyncService` and `PlanningCatalogSyncService`.
- `Next boundary`: do not broaden Phase 4 rollout. Start the bounded Phase 4 planning projection snapshot task and keep later rewrite phases blocked until that slice lands and reaches its own explicit outcome review.

## Phase 4 Slice Outcome
- `Decision`: implemented as one bounded private shared-projection slice.
- `Shared helper boundary`: `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py` now owns the trace-scoped planning source assembly and coordination derivation used by `initiative_index` and `planning_catalog`.
- `Public planning parity`: held. `watchtower-core query authority --domain planning --format json`, `watchtower-core query coordination --format json`, and `watchtower-core query planning --trace-id trace.structural_rewrite_program --format json` continue to resolve the same public planning answers after the slice lands.
- `Direct parity coverage`: `core/python/tests/unit/test_planning_catalog_sync.py` now asserts that the planning-catalog coordination section matches the initiative projection, and the bounded sync plus closeout suite passed cleanly.
- `Outcome-review handoff`: [review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md)

## Phase 4 Slice Outcome Review Outcome
- `Decision`: passed.
- `Shared snapshot boundary`: unchanged. `planning_projection_snapshot.py` remains a private runtime helper behind `initiative_index` and `planning_catalog`; it does not become a public planning authority surface.
- `Public planning parity`: held through the closed review. The five planning-authority answers and the existing coordination-sync ordering, mutation callers, and downstream tracker behavior remain unchanged.
- `Next boundary`: do not broaden Phase 4 rollout. Open the bounded Phase 4 closeout-coordination entry package and keep further Phase 4 plus later-phase implementation blocked until that entry review closes explicitly.

## Phase 4 Closeout Coordination Entry Review Outcome
- `Decision`: approved for one bounded Phase 4 slice only.
- `Public planning boundary`: unchanged. The five planning-authority answers remain the same after the closeout-coordination entry review closes.
- `Closeout result contract boundary`: explicit. `traceability_output_path` remains the pre-seam write, the approved shared-output seam is limited to `initiative_index_output_path`, `planning_catalog_output_path`, `coordination_index_output_path`, `initiative_tracking_output_path`, and `coordination_tracking_output_path`, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain direct outputs outside the approved seam for this slice.
- `Approved first slice`: [structural_rewrite_phase4_closeout_coordination_sync_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md)
- `Exact seam`: one post-traceability closeout step that reuses `CoordinationSyncService` for the shared planning and coordination outputs only while leaving `TaskLifecycleService`, `PlanningScaffoldService`, and the direct PRD, decision, and design tracking outputs unchanged.
- `Next boundary`: do not broaden Phase 4 rollout. Land the bounded Phase 4 closeout coordination sync-reuse task, then keep later rewrite phases blocked until its explicit outcome review closes.

## Phase 4 Closeout Coordination Sync-Reuse Slice Outcome
- `Decision`: implemented as one bounded closeout convergence slice.
- `Shared orchestration seam`: `InitiativeCloseoutService.close` now writes traceability first, then reuses `CoordinationSyncService.run_closeout_shared_outputs` for exactly `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking` without widening into `task-index`, `traceability-index`, or `task-tracking`.
- `Closeout result contract`: held. `traceability_output_path` remains the pre-seam canonical write, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain direct outputs outside the approved seam while the closeout CLI payload keeps the full output-path contract explicit.
- `Direct parity coverage`: `core/python/tests/unit/test_initiative_closeout.py` now pins the exact shared coordination target subset plus the preserved direct tracker outputs, and the closeout-plus-sync regression suite passed cleanly before the repo-wide reruns.
- `Outcome-review handoff`: [review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md)

## Phase 4 Closeout Coordination Sync-Reuse Outcome Review Outcome
- `Decision`: passed.
- `Parity result`: held through the closed review. `doctor`, `validate all`, the five public planning-authority answers, the coordination view, and the structural rewrite planning view remained unchanged while the bounded shared closeout seam stayed active.
- `Boundary result`: unchanged. `traceability_output_path` remains pre-seam, the approved shared coordination outputs remain fixed to `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking`, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain direct and explicit.
- `Next boundary`: do not broaden Phase 4 rollout. Open the bounded Phase 4 closeout-tracking entry package and keep further Phase 4 plus later-phase implementation blocked until that entry review closes explicitly.

## Phase 4 Closeout Tracking Entry Review Outcome
- `Decision`: approved for one bounded Phase 4 slice only.
- `Public planning boundary`: unchanged. The five planning-authority answers remain the same after the closeout-tracking entry review closes.
- `Approved shared closeout seam`: unchanged. `traceability_output_path` remains pre-seam, the approved shared coordination outputs remain fixed, and the review does not authorize adding the tracker targets to `CoordinationSyncService`.
- `Closeout result contract boundary`: explicit. `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain individually reported result fields and CLI payload fields for the approved slice.
- `Approved first slice`: [structural_rewrite_phase4_closeout_tracking_refresh_boundary.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md)
- `Exact seam`: one private closeout-local refresh boundary for the three remaining tracker outputs after the approved shared closeout seam completes, while the public tracker sync family names and current mutation callers remain unchanged.
- `Next boundary`: do not broaden Phase 4 rollout. Keep later rewrite phases blocked until the bounded Phase 4 closeout-tracking refresh-boundary outcome review records an explicit decision.

## Phase 4 Closeout Tracking Refresh-Boundary Slice Outcome
- `Decision`: implemented as one bounded private closeout-local tracker-refresh slice.
- `Private boundary`: `InitiativeCloseoutService.close` now routes the remaining `prd-tracking`, `decision-tracking`, and `design-tracking` refresh step through `_run_closeout_tracking_refresh_boundary()` after the approved shared coordination seam completes.
- `Closeout result contract`: held. `traceability_output_path` remains pre-seam, the approved shared coordination outputs remain fixed, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain explicit result and CLI payload fields outside the shared seam.
- `Outcome-review handoff`: [review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_refresh_boundary_outcome.md)

## Phase 4 Closeout Tracking Refresh-Boundary Outcome Review Outcome
- `Decision`: passed.
- `Parity result`: held through the closed review. `doctor`, `validate all`, the five public planning-authority answers, the coordination view, the structural rewrite planning view, command-index drift checks, and the targeted closeout-plus-sync tests all remained green while the final bounded slice stayed under review.
- `Boundary result`: unchanged. `traceability_output_path` remains pre-seam, the approved shared coordination seam remains fixed to `initiative-index`, `planning-catalog`, `coordination-index`, `initiative-tracking`, and `coordination-tracking`, and `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain explicit and direct outside that seam while the five public planning-authority answers, public tracker sync family names, current mutation callers, and private planning-graph boundary remain unchanged.
- `Closeout decision`: no successor checkpoint. Close `trace.structural_rewrite_program` as `completed` and require any later rewrite work to start as a new bounded trace rather than continuing implicitly from this program.

## Risks
- The implementation plan can still overstate readiness if later readers treat the bounded pilot as general authorization for broader Phase 2 rollout.
- Compatibility markers may look cheap to retire even when repository-path continuity still depends on them.
- The artifact-role metadata pilot can drift upward in blast radius if it starts to drive live query or sync behavior before its additive read-only model is proven.
- The approved Phase 3 slice can still widen unsafely if command companion cleanup starts acting like a new command-authority source instead of remaining a bounded docs-plus-index normalization pass.

## Validation Plan
- Re-run the required baseline commands:
  - `./core/python/.venv/bin/watchtower-core doctor --format json`
  - `./core/python/.venv/bin/watchtower-core validate all`
  - `./core/python/.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./core/python/.venv/bin/watchtower-core query coordination --format json`
- Rebuild derived planning surfaces with `./core/python/.venv/bin/watchtower-core sync all --write --format json`.
- Re-run `./core/python/.venv/bin/watchtower-core validate all`.
- Probe the live planning and trace surfaces after sync with:
  - `./core/python/.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./core/python/.venv/bin/watchtower-core query coordination --format json`
  - `./core/python/.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Confirm that the closed Phase 4 closeout-tracking refresh-boundary outcome review leaves no active rewrite checkpoint and no broader Phase 4 or later-phase continuation implied.

## Rollout or Migration Plan
- Land the traced rewrite package, close the Phase 2 gate explicitly, publish one additive dedicated-registry slice, sync and validate, close the pilot review explicitly, close the Phase 3 entry review explicitly, implement one bounded Phase 3 command companion slice, close that slice through explicit outcome review, close the Phase 4 entry review explicitly, implement one bounded Phase 4 planning projection snapshot slice, close that slice through explicit outcome review, close the Phase 4 closeout-coordination entry review explicitly, land one bounded Phase 4 closeout coordination sync-reuse slice, close that slice through explicit outcome review, close the Phase 4 closeout-tracking entry review explicitly, land the bounded closeout-tracking refresh-boundary slice, close its explicit outcome review, and end the trace through one explicit program-closeout decision.
- Do not expand the approved Phase 4 seams into broader shared-projection rollout, public-planning-boundary changes, broader mutation-path convergence, broader tracker-family convergence, compatibility retirement, or later rewrite phases without a new explicit review outcome.

## Open Questions
- None. The final outcome review closed the trace with an explicit program-closeout decision; any later rewrite work belongs to a new bounded trace.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [structural_rewrite_artifact_role_registry_pilot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md)

## Updated At
- `2026-03-15T09:55:03Z`
