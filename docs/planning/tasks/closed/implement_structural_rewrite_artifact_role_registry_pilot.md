---
id: task.structural_rewrite_program.artifact_role_registry_pilot.004
trace_id: trace.structural_rewrite_program
title: Implement structural rewrite artifact role registry pilot
summary: Publish the bounded artifact-role registry family and its checkpoint companions without changing live planning authority behavior.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-14T04:31:59Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md
- core/control_plane/schemas/artifacts/artifact_role_registry.v1.schema.json
- core/control_plane/registries/artifact_roles/artifact_role_registry.v1.json
- core/control_plane/registries/artifact_types/artifact_type_registry.v1.json
- core/control_plane/registries/schema_catalog/schema_catalog.v1.json
- core/control_plane/registries/validators/validator_registry.v1.json
- core/control_plane/examples/valid/registries/artifact_role_registry.v1.example.json
- core/control_plane/examples/invalid/registries/artifact_role_registry_missing_retention_reasons.v1.example.json
- core/control_plane/ledgers/migrations/structural_rewrite_artifact_role_registry_pilot.v1.json
- core/control_plane/ledgers/validation_evidence/structural_rewrite_artifact_role_registry_pilot.v1.json
related_ids:
- prd.structural_rewrite_program
- design.features.structural_rewrite_program
- design.implementation.structural_rewrite_program
- design.implementation.structural_rewrite_artifact_role_registry_pilot
- contract.acceptance.structural_rewrite_program
depends_on:
- task.structural_rewrite_program.phase2_entry_review.003
---

# Implement structural rewrite artifact role registry pilot

## Summary
Publish the bounded artifact-role registry family and its checkpoint companions without changing live planning authority behavior.

## Scope
- Publish the new `artifact_role_registry` schema, registry, validator, catalog, artifact-type, and example surfaces.
- Publish the dedicated migration record and validation-evidence artifact for the slice.
- Keep the slice additive and read-only.

## Done When
- The dedicated registry family validates successfully.
- The public planning-authority answers remain unchanged.
- The trace stops with a successor review task rather than broader rollout.

## Outcome
- The first Phase 2 slice uses a dedicated registry, not additive metadata inside an existing governed family.
- The published entries cover only the six public planning-authority surfaces fixed by the parity contract.
- The slice remains descriptive only and does not change runtime routing, sync selection, validator dispatch, command authority, or planning-boundary behavior.

## Links
- [structural_rewrite_artifact_role_registry_pilot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md)
- [review_structural_rewrite_artifact_role_registry_pilot_outcome.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_artifact_role_registry_pilot_outcome.md)

## Updated At
- `2026-03-14T04:31:59Z`
