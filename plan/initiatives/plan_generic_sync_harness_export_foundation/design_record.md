# Plan Generic Sync Harness Export Foundation Design Record

## Summary
Exports a reusable sync harness from watchtower_core.sync and refactors repo-local sync orchestration onto that generic layer so requirements.md and decisions.md no longer depend on a repo_ops-only sync coordinator.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_generic_sync_harness_export_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
