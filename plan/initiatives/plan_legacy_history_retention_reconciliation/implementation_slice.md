# Plan Legacy History and Retention Reconciliation Implementation Slice

## Summary
Encodes the transitional archive policy and clean-endstate purge rules for legacy `docs/planning/**` history and closed initiative packages directly in the live plan authority.

## Work Breakdown
- `task.plan_legacy_history_retention_reconciliation.publish_retention_policy_registry_and_loader_support`
  Publish `plan/.wt/schemas/artifacts/retention_policy_registry.schema.json`, `plan/.wt/registries/retention_policy_registry.json`, typed model exports, loader support, and a helper that resolves the current and clean-endstate retention disposition for any covered path.
- `task.plan_legacy_history_retention_reconciliation.classify_legacy_history_and_transitional_archive_surfaces`
  Encode explicit rules for:
  - frozen `docs/planning/**` history
  - authoritative `plan/.wt/**`
  - authoritative `plan/docs/**`
  - transitional pack-wide and project-scoped initiative archives
  - minimal purge ledgers under `core/control_plane/ledgers/purges/`
  Then align the closest human entrypoints so those rules are not visible only in JSON.
- `task.plan_legacy_history_retention_reconciliation.validate_retention_policy_alignment_and_follow_up_linkage`
  Add focused unit coverage, extend pack-context coverage for the new registry, and link the capture-first bootstrap planning package plus the legacy follow-up task to this live plan initiative.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
