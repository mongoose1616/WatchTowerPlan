# `core/control_plane/ledgers/migrations`

## Description
`This directory holds the committed append-only history of schema, registry, contract, policy, and workspace migrations that need durable reviewable records.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/ledgers/migrations/README.md` | Describes the purpose of the migration ledger directory and its current contents. |
| `core/control_plane/ledgers/migrations/core_python_workspace_bootstrap.v1.json` | Migration record for the transition from a reserved Python scaffold to an active governed local workspace. |
| `core/control_plane/ledgers/migrations/structural_rewrite_artifact_role_registry_pilot.v1.json` | Migration record for the first bounded Phase 2 slice that publishes the additive artifact-role registry pilot. |
| `core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization.v1.json` | Migration record for the completed first bounded Phase 3 slice that reconciles command companion source surfaces and publishes the sync-time drift guard. |
| `core/control_plane/ledgers/migrations/structural_rewrite_phase3_command_companion_source_surface_normalization_ready.v1.json` | Migration record for the Phase 3 entry outcome that approves the first bounded command companion source-surface normalization slice. |
| `core/control_plane/ledgers/migrations/structural_rewrite_phase4_shared_projection_entry_ready.v1.json` | Migration record for the closed Phase 3 outcome review that opens the bounded Phase 4 shared-projection entry checkpoint. |
| `core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot_ready.v1.json` | Migration record for the approved Phase 4 entry review that opens the first bounded planning projection snapshot slice. |
| `core/control_plane/ledgers/migrations/structural_rewrite_phase4_planning_projection_snapshot.v1.json` | Migration record for the completed first bounded Phase 4 planning projection snapshot slice. |
| `core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_entry_ready.v1.json` | Migration record for the closed first Phase 4 slice outcome review that opens the bounded closeout-coordination entry checkpoint. |
| `core/control_plane/ledgers/migrations/structural_rewrite_phase4_closeout_coordination_sync_reuse_ready.v1.json` | Migration record for the approved closeout-coordination entry review that opens the bounded post-traceability coordination-sync reuse slice. |
| `core/control_plane/ledgers/migrations/structural_rewrite_program_phase0_phase1_ready.v1.json` | Migration record for moving the structural rewrite from external prose into a traced Phase 0 and Phase 1 package with the Phase 2 review gate prepared. |
