# `core/control_plane/ledgers/migrations`

## Description
`This directory holds the committed append-only history of schema, registry, contract, policy, and workspace migrations that need durable reviewable records.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/ledgers/migrations/README.md` | Describes the purpose of the migration ledger directory and its current contents. |
| `core/control_plane/ledgers/migrations/core_python_workspace_bootstrap.v1.json` | Migration record for the transition from a reserved Python scaffold to an active governed local workspace. |
| `core/control_plane/ledgers/migrations/structural_rewrite_artifact_role_registry_pilot.v1.json` | Migration record for the first bounded Phase 2 slice that publishes the additive artifact-role registry pilot. |
| `core/control_plane/ledgers/migrations/structural_rewrite_program_phase0_phase1_ready.v1.json` | Migration record for moving the structural rewrite from external prose into a traced Phase 0 and Phase 1 package with the Phase 2 review gate prepared. |
