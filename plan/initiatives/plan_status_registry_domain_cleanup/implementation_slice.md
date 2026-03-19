# Plan Status Registry Domain Cleanup Implementation Slice

## Summary
Removes legacy challenge-specific status leakage from the shared status registry and reconciles the authoritative requirements notes to the current pack-facing interface state.

## Work Breakdown
- `task.plan_status_registry_domain_cleanup.generalize_shared_status_vocabulary`: Replace the legacy challenge-scoped blocked and terminal status entries with plan-domain-neutral status vocabulary.
- `task.plan_status_registry_domain_cleanup.add_focused_status_registry_coverage`: Lock the cleaned status-registry shape through targeted pack-context or loader coverage.
- `task.plan_status_registry_domain_cleanup.reconcile_requirements_notes`: Update requirements.md so the status-registry and artifact-index leakage notes reflect the current implemented state.

## Acceptance Shape
- The shared status registry no longer publishes `challenge`-only family bindings or the `solved` and `unresolved` values.
- Typed loader coverage proves the cleaned vocabulary through the reusable-core load path.
- The authoritative requirements notes stop claiming that artifact-index field leakage is still present.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
