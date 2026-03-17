# Plan Generic Sync Harness Export Foundation Implementation Slice

## Summary
Exports a reusable sync harness from watchtower_core.sync and refactors repo-local sync orchestration onto that generic layer so requirements.md and decisions.md no longer depend on a repo_ops-only sync coordinator.

## Initial Work Breakdown
- `task.plan_generic_sync_harness_export_foundation.publish_generic_sync_harness_contracts`: Add the export-safe sync harness, shared result types, and reusable protocols under watchtower_core.sync.
- `task.plan_generic_sync_harness_export_foundation.refactor_repo_sync_orchestration_onto_generic_harness`: Move all-sync and coordination-sync orchestration onto the generic sync harness without changing current sync target behavior.
- `task.plan_generic_sync_harness_export_foundation.validate_sync_harness_export_and_guidance`: Add tests and documentation proving watchtower_core.sync now publishes the reusable harness and remains aligned with requirements.md and decisions.md.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
