---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_artifact_role_registry_pilot"
title: "Structural Rewrite Artifact Role Registry Pilot"
summary: "Implements the first bounded Phase 2 slice by publishing an additive, read-only artifact-role registry for the public planning-authority surfaces."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-14T03:56:23Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/design/implementation/"
  - "docs/planning/tasks/"
  - "core/control_plane/schemas/artifacts/"
  - "core/control_plane/registries/"
  - "core/control_plane/examples/"
  - "core/control_plane/contracts/acceptance/"
  - "core/control_plane/ledgers/migrations/"
  - "core/control_plane/ledgers/validation_evidence/"
aliases:
  - "artifact role pilot"
  - "phase 2 artifact role registry slice"
  - "bounded rewrite pilot"
---

# Structural Rewrite Artifact Role Registry Pilot

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_artifact_role_registry_pilot`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-14T03:56:23Z`

## Summary
Implements the first bounded Phase 2 slice by publishing an additive, read-only artifact-role registry for the six public planning-authority surfaces already classified in Phase 1.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [review_structural_rewrite_program_phase2_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_program_phase2_entry_package.md)

## Scope Summary
- Publish the new `artifact_role_registry` family and its schema-backed validation companions.
- Keep the slice additive and read-only.
- Limit entries to the six public planning-authority surfaces already classified in Phase 1.
- Stop after the slice is synced, validated, and handed to a follow-up review task.

## Assumptions and Constraints
- The dedicated registry is descriptive metadata only and must not become runtime authority in this slice.
- The five public planning-authority answers remain the hard parity boundary.
- The slice must stay inside existing control-plane publication families instead of inventing rewrite-only storage.
- The new registry may add no runtime consumers beyond schema-backed validation and review surfaces.

## Current-State Context
- The Phase 2 gate is approved for exactly one bounded slice.
- The live workspace validates cleanly before the slice.
- The follow-on checkpoint after this slice is a review task, not broader implementation authorization.

## Internal Standards and Canonical References Applied
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): the registry entries must use the controlled authority-role, storage-class, compatibility-support, and retention-reason vocabulary already fixed in Phase 1.
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the slice must publish one checkpoint document, one migration record, one validation-evidence artifact, and explicit parity and rollback notes.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the slice may not change the five public planning-authority answers.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): the first slice needs durable evidence, not transient operator notes.

## Slice Boundary
- Publish one new governed family: `artifact_role_registry`.
- Keep the slice additive and read-only.
- Limit entries to the six public planning-authority surfaces already classified in Phase 1.
- Do not add runtime consumers.
- Do not change planning-authority answers, command authority, query routing, sync orchestration, validator dispatch, or planning-boundary behavior.

## Storage Shape Decision
### Chosen shape
- `small dedicated registry`

### Rationale
- Phase 1 classifications span multiple public planning surface families, so embedding metadata inside any one existing family would imply the wrong ownership boundary immediately.
- A dedicated registry stays additive, keeps authored truth explicit, and matches the repo's existing control-plane publication pattern of schema plus registry plus validator plus examples.
- Rollback is smaller and clearer: the pilot can be removed without restoring a replaced authority surface because nothing public is being replaced.

## Proposed Technical Approach
- Publish one new schema under `core/control_plane/schemas/artifacts/`.
- Publish one new authored registry under `core/control_plane/registries/artifact_roles/`.
- Extend the artifact-type registry, schema catalog, and validator registry so the new family participates in normal governed-artifact validation.
- Publish one valid example and one invalid example to make the family reviewable and regression-friendly.
- Use the existing rewrite acceptance contract, plus one dedicated migration record and one dedicated validation-evidence artifact, to record the slice without changing runtime code.

## Authored Truth and Derived Outputs
### Authored truth
- `core/control_plane/registries/artifact_roles/artifact_role_registry.v1.json`

### Derived outputs
- None in this slice.
- Companion publication surfaces are required same-change artifacts, not runtime-derived outputs:
  - `core/control_plane/schemas/artifacts/artifact_role_registry.v1.schema.json`
  - `core/control_plane/registries/artifact_types/artifact_type_registry.v1.json`
  - `core/control_plane/registries/schema_catalog/schema_catalog.v1.json`
  - `core/control_plane/registries/validators/validator_registry.v1.json`
  - `core/control_plane/examples/valid/registries/artifact_role_registry.v1.example.json`
  - `core/control_plane/examples/invalid/registries/artifact_role_registry_missing_retention_reasons.v1.example.json`

## Current Consumers
- Current consumers are governance and validation surfaces only:
  - `./.venv/bin/watchtower-core validate all`
  - `core/python/src/watchtower_core/validation/artifact.py`
  - `core/control_plane/registries/validators/validator_registry.v1.json`
  - `core/control_plane/registries/schema_catalog/schema_catalog.v1.json`
  - `core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json`
  - `core/control_plane/ledgers/validation_evidence/structural_rewrite_artifact_role_registry_pilot.v1.json`
- There are intentionally no runtime query, sync, loader-selection, or validator-dispatch consumers beyond schema-backed validation in this slice.

## Parity Method
- Compare the published registry entries against the Phase 1 critical-surface classification table.
- Confirm that every published entry maps to one of the six public planning-authority surfaces already fixed in the parity contract.
- Re-run:
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
- Accept the slice only if those commands preserve the same public planning-authority answers and the trace stays bounded to the new descriptive family.

## Rollback Path
1. Remove the `artifact_role_registry` schema, registry, validator, artifact-type, schema-catalog, example, and slice-specific checkpoint surfaces.
2. Restore the acceptance contract and trace planning docs to the pre-slice checkpoint state if needed.
3. Rebuild derived planning surfaces.
4. Re-run validation and the planning-authority queries to confirm the repo has returned to the pre-slice parity state.

## Slice Contents
### Registry entries
| Surface ID | Title | Authority Role | Storage Class | Compatibility Support Level |
|---|---|---|---|---|
| `surface.planning.current_state` | Current Planning State | `canonical_machine_answer` | `active_family_location` | `n/a` |
| `surface.planning.trace_catalog` | Trace-Linked Planning Catalog | `canonical_machine_answer` | `active_family_location` | `n/a` |
| `surface.planning.initiative_family_view` | Initiative Family View | `canonical_machine_answer` | `active_family_location` | `n/a` |
| `surface.planning.task_execution_state` | Task Execution State | `canonical_machine_answer` | `active_family_location` | `n/a` |
| `surface.planning.traceability_join` | Traceability Join | `canonical_machine_answer` | `active_family_location` | `n/a` |
| `surface.planning.authority_lookup` | Planning Authority Lookup | `discovery_index` | `active_family_location` | `n/a` |

### Out of scope
- Compatibility-surface classification materialization.
- Workflow, validator-selection, or sync-target metadata rollout.
- Metadata-driven runtime decisions.

## Work Breakdown
1. Publish the dedicated human checkpoint document for the slice.
2. Publish the dedicated migration record and validation-evidence artifact.
3. Publish the schema, registry, validator, artifact-type, and schema-catalog entries for the new family.
4. Publish valid and invalid examples for the family.
5. Sync and validate the repository.
6. Stop with one explicit follow-up review task still open.

## Risks
- The registry could be mistaken for runtime authority if later work starts consuming it implicitly instead of through a new checkpoint.
- The slice could overstate coverage if future readers assume the six public planning-authority entries already generalize to broader compatibility or workflow families.
- The registry could become harder to roll back if later slices start embedding it into other governed families before a new review outcome exists.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json`.
- Run `./.venv/bin/watchtower-core validate all`.
- Re-run:
  - `./.venv/bin/watchtower-core doctor --format json`
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`

## Rollout or Migration Plan
- Land the bounded registry family and its checkpoint companions in one change set.
- Rebuild the derived planning surfaces after the family is published.
- Stop with the follow-up review task open instead of expanding into a second slice.

## Stop Condition
- Stop after the slice is synced, validated, and documented.
- Do not start a second metadata slice or any Phase 3 work in the same pass.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [structural_rewrite_program_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/structural_rewrite_program_acceptance.v1.json)

## Updated At
- `2026-03-14T03:56:23Z`
