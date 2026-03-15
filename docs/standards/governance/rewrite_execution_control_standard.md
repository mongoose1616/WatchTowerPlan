---
id: "std.governance.rewrite_execution_control"
title: "Rewrite Execution Control Standard"
summary: "This standard defines the parity contract, slice-control package, checkpoint workflow, and phase-entry guardrails for the structural rewrite program."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "rewrite"
  - "phase_control"
owner: "repository_maintainer"
updated_at: "2026-03-15T08:14:01Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/design/implementation/"
  - "docs/planning/tasks/"
  - "core/control_plane/contracts/acceptance/"
  - "core/control_plane/ledgers/migrations/"
  - "core/control_plane/ledgers/validation_evidence/"
aliases:
  - "rewrite phase control"
  - "rewrite parity contract"
  - "rewrite checkpoint workflow"
---

# Rewrite Execution Control Standard

## Summary
This standard defines the parity contract, slice-control package, checkpoint workflow, and phase-entry guardrails for the structural rewrite program.

## Purpose
- Keep the structural rewrite phased, reviewable, and bounded against the live repository baseline.
- Reuse existing repo-native planning, contract, migration, and evidence surfaces instead of inventing rewrite-only storage.
- Prevent later rewrite slices from changing public authority boundaries or starting high-blast-radius work without an explicit checkpoint.

## Scope
- Applies to the structural rewrite program from Phase 0 through rewrite closeout.
- Covers the public planning-authority parity contract, slice-control package, descriptor-authority declaration, rollback expectations, and mandatory phase-entry checkpoints.
- Does not define the content of every future rewrite slice; it defines the control surfaces those slices must publish.

## Use When
- Publishing rewrite prerequisites in Phase 0 or Phase 1.
- Preparing or reviewing any Phase 2 or later rewrite slice.
- Deciding whether a proposed rewrite change is allowed to enter implementation.

## Related Standards and Sources
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): later rewrite slices must pair execution control with surface classification.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): the public planning-authority parity contract is materialized as a machine-readable acceptance contract.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): durable parity and checkpoint evidence must land in the validation-evidence ledger.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): parity checks must preserve the current canonical planning-authority answers unless an accepted decision changes them.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): rewrite control surfaces must stay joined through one trace and active task chain.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): rewrite slices still need the normal inspect, refresh, rebuild, validate, and record loop.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): compatibility and helper-layer changes must stay bounded and explicit.

## Guidance
- Phase 0 and Phase 1 may publish prerequisites, classifications, and review packages only. They do not authorize Phase 2 implementation by themselves.
- The program-level machine-readable parity contract lives at [structural_rewrite_program_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json).
- The default slice-control package for Phase 2 and later is:
  - one human checkpoint document under `docs/planning/design/implementation/`
  - one machine migration record under `core/control_plane/ledgers/migrations/`
  - one machine validation-evidence artifact under `core/control_plane/ledgers/validation_evidence/`
- The human checkpoint document is the place to record:
  - the slice boundary
  - the old and new authority or builder
  - the authored-truth source
  - the derived outputs
  - the shadow-mode or parity window when applicable
  - approved intentional improvements
  - rollback procedure
  - phase-entry or phase-exit decision
- The migration record is the machine-readable state-transition anchor. Use it to record the subject, from-state, to-state, summary, and related paths for the approved slice transition.
- The validation-evidence artifact is the durable proof surface for parity, validation, and checkpoint outcomes.
- If a slice needs new or changed parity obligations, update the acceptance contract in the same change set rather than hiding those obligations only in prose.
- Every descriptor-backed or derivation-backed slice must declare, before implementation:
  - one authored truth surface
  - the derived outputs
  - the loader, query, sync, or validator consumers
  - the parity method
  - the rollback path
- A positive later-phase entry review must name the full consumer boundary for the approved slice. For projection or orchestration slices, that boundary includes the coordination-sync ordering, write-side mutation callers, direct rebuild paths, affected tracker emitters, and one exact rollback-safe builder or orchestration seam.
- A positive slice outcome review does not authorize an unnamed successor checkpoint. If a review passes, it must name the next bounded checkpoint explicitly and keep higher-blast-radius implementation blocked until that checkpoint's own review closes.
- If a later-phase outcome review passes and the next materially different rewrite risk sits on a different consumer boundary inside the same phase, prefer a new bounded entry package over direct implementation so the next seam is reviewed explicitly before code changes begin.
- Command presence and hierarchy are not an allowed first pilot family for the rewrite because the live CLI registry and parser tree remain the current authority.
- Treat the five planning questions already published in the authority map as the public rewrite-parity boundary unless an accepted decision changes them.
- Do not start a later rewrite phase if the corresponding checkpoint is still only implied in tasks, commit messages, or external notes.

## Structure or Data Model
### Required control surfaces
| Control Surface | Canonical Home | Role |
|---|---|---|
| Human checkpoint document | `docs/planning/design/implementation/` | Reviewable phase plan, parity notes, and rollback procedure. |
| Acceptance contract | `core/control_plane/contracts/acceptance/` | Machine-readable parity and entry-condition contract. |
| Migration record | `core/control_plane/ledgers/migrations/` | Machine-readable state-transition record for the slice. |
| Validation evidence | `core/control_plane/ledgers/validation_evidence/` | Durable proof of baseline, parity, and validation outcomes. |
| Active gate task | `docs/planning/tasks/open/` | Explicit execution and review ownership for the current checkpoint. |

### Public planning parity boundary
| Planning Question | Canonical Surface That Must Stay Stable |
|---|---|
| Current planning state and next action | `coordination_index` plus `watchtower-core query coordination` |
| Full trace-linked planning context | `planning_catalog` plus `watchtower-core query planning` |
| Compact initiative-family view | `initiative_index` plus `watchtower-core query initiatives` |
| Authoritative task execution state and dependency graph | `task_index` plus `watchtower-core query tasks` |
| Durable trace-linked source join and initiative closeout state | `traceability_index` plus `watchtower-core query trace` |

### Phase 2 entry conditions
| Condition | Expectation |
|---|---|
| Pilot family fixed | Exactly one low-blast-radius pilot family is selected and justified. |
| Authored-versus-derived direction published | The chosen pilot has a declared authored truth surface, derived outputs, and consumer set. |
| Classification complete | Critical and candidate cleanup surfaces have four-axis classification plus current consumer maps where needed. |
| Compatibility classified | Compatibility surfaces have support levels and retention reasons. |
| Rollback explicit | The checkpoint package records rollback expectations for the pilot slice. |
| Review task open | A non-terminal review task is the next controlling surface before implementation starts. |

### No-go conditions
| Condition | Meaning |
|---|---|
| Public planning-authority drift | Do not change the five planning answers without an accepted decision and matching same-change contract updates. |
| Unclassified retirement | Do not move, delete, or retire a surface before classification and consumer mapping exist. |
| Unbounded dual truth | Do not add a new descriptor or registry path that competes with an existing authority source without declared derivation direction and rollback. |
| Premature pilot start | Do not start Phase 2 implementation before the Phase 2 entry review task reaches an explicit approval outcome. |
| Archive vocabulary drift | Do not introduce a new archive taxonomy or lifecycle state as an execution shortcut. |

## Process or Workflow
1. Start the rewrite slice from the active checkpoint document and gate task.
2. Confirm that the acceptance contract still captures the public parity and entry conditions for the proposed slice.
3. Publish or update the human checkpoint document with authored truth, derived outputs, parity method, and rollback notes.
4. Publish or update the migration record and validation-evidence artifact for the same slice.
5. Run the required validation and parity checks.
6. Record the phase-entry or phase-exit decision explicitly before any higher-blast-radius implementation continues.

## Operationalization
- `Modes`: `documentation`; `artifact`; `workflow`
- `Operational Surfaces`: `docs/planning/design/implementation/structural_rewrite_program.md`; `docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md`; `docs/planning/design/implementation/structural_rewrite_phase3_command_authority_entry.md`; `docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md`; `docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md`; `docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md`; `docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_entry.md`; `docs/planning/design/implementation/structural_rewrite_phase4_closeout_coordination_sync_reuse.md`; `docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_entry.md`; `docs/planning/design/implementation/structural_rewrite_phase4_closeout_tracking_refresh_boundary.md`; `docs/planning/tasks/closed/review_structural_rewrite_program_phase2_entry_package.md`; `docs/planning/tasks/closed/review_structural_rewrite_artifact_role_registry_pilot_outcome.md`; `docs/planning/tasks/closed/review_structural_rewrite_phase3_entry_package.md`; `docs/planning/tasks/closed/implement_structural_rewrite_phase3_command_companion_source_surface_normalization.md`; `docs/planning/tasks/closed/review_structural_rewrite_phase3_command_companion_source_surface_normalization_outcome.md`; `docs/planning/tasks/closed/review_structural_rewrite_phase4_shared_projection_entry_package.md`; `docs/planning/tasks/closed/implement_structural_rewrite_phase4_planning_projection_snapshot.md`; `docs/planning/tasks/closed/review_structural_rewrite_phase4_planning_projection_snapshot_outcome.md`; `docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_entry_package.md`; `docs/planning/tasks/closed/implement_structural_rewrite_phase4_closeout_coordination_sync_reuse.md`; `docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_coordination_sync_reuse_outcome.md`; `docs/planning/tasks/closed/review_structural_rewrite_phase4_closeout_tracking_entry_package.md`; `docs/planning/tasks/open/implement_structural_rewrite_phase4_closeout_tracking_refresh_boundary.md`; `core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_program_phase0_phase1_ready.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_artifact_role_registry_pilot.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization_ready.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_shared_projection_entry_ready.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json`; `core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_program_phase0_phase1_baseline.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_artifact_role_registry_pilot.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase3_command_companion_source_surface_normalization_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_shared_projection_entry_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_planning_projection_snapshot.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_coordination_sync_reuse.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_entry_ready.v1.json`; `core/control_plane/ledgers/validation_evidence/structural_rewrite_phase4_closeout_tracking_refresh_boundary_ready.v1.json`

## Validation
- Rewrite checkpoints should not rely on prose-only approval.
- Reviewers should reject a Phase 2 or later slice whose authored truth, derived outputs, or rollback path are missing.
- Reviewers should reject phase entry when the parity contract and authority map disagree about the public planning boundary.
- Reviewers should reject rewrite slices that start implementation before the gate task or checkpoint document records an explicit decision.

## Change Control
- Update this standard when the rewrite control package, phase-entry rules, or parity boundary changes materially.
- Update the structural rewrite acceptance contract, migration records, validation evidence, and checkpoint plan in the same change set when this standard changes materially.

## References
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_program_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json)
- [authority_map.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/authority_map/authority_map.v1.json)

## Updated At
- `2026-03-15T08:14:01Z`
