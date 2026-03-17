# Plan Legacy History and Retention Reconciliation

## Summary
Encodes the transitional archive policy and clean-endstate purge rules for legacy `docs/planning/**` history and closed initiative packages directly in the live `plan/**` authority.

## Identity
- `initiative_id`: `initiative.plan_legacy_history_retention_reconciliation`
- `trace_id`: `trace.plan_legacy_history_retention_reconciliation`
- `scope_type`: `pack_wide`

## Authority
- [requirements.md](/home/j/WatchTowerPlan/requirements.md) and [decisions.md](/home/j/WatchTowerPlan/decisions.md) are the authoritative implementation contract for this initiative.
- Existing purge tooling and retention standards may inform the implementation only where they stay consistent with the locked hard-cutover, transitional-archive, and clean-endstate decisions.
- This slice specifically implements the follow-up required by `Q24`, `Q31`, `Q48`, and `Q50` in [decisions.md](/home/j/WatchTowerPlan/decisions.md) and the cleanup rules named in [requirements.md](/home/j/WatchTowerPlan/requirements.md#L533), [requirements.md](/home/j/WatchTowerPlan/requirements.md#L541), [requirements.md](/home/j/WatchTowerPlan/requirements.md#L564), and [requirements.md](/home/j/WatchTowerPlan/requirements.md#L696).

## Acceptance Boundary
- Publish a governed `retention_policy_registry` under `plan/.wt/registries/` with matching schema, schema-catalog entry, validator entry, pack-settings declaration, and typed loader support.
- Encode explicit machine-readable dispositions for the frozen `docs/planning/**` corpus, live `plan/.wt/**` authority, promoted `plan/docs/**` guidance, transitional initiative archives, and minimal purge ledgers.
- Add helper and tests that prove the live repository roots resolve to the expected retention policy and that the clean-endstate purge rule is explicit rather than implicit prose.
- Link the new live initiative from the capture-first bootstrap planning package so the legacy follow-up is no longer just an open reminder in the docs-backed backlog.

## Initial Task Set
- `task.plan_legacy_history_retention_reconciliation.publish_retention_policy_registry_and_loader_support`: Add the retention_policy_registry schema, registry, typed model support, and helper methods for resolving current versus clean-endstate retention decisions.
- `task.plan_legacy_history_retention_reconciliation.classify_legacy_history_and_transitional_archive_surfaces`: Encode the current and clean-endstate retention policy for docs/planning history, plan initiative archives, promoted guidance, and purge ledgers, and align adjacent entrypoint docs.
- `task.plan_legacy_history_retention_reconciliation.validate_retention_policy_alignment_and_follow_up_linkage`: Add focused tests and close the legacy follow-up task once the new plan initiative and policy artifacts are linked from the capture-first bootstrap package.
