# Plan Evidence Bundle Helper Foundation Implementation Slice

## Summary
Broaden watchtower_core.evidence with a reusable evidence-bundle helper, then route live plan evidence bootstrap and indexing through that boundary.

## Initial Work Breakdown
- `task.plan_evidence_bundle_helper_foundation.define_evidence_bundle_helper_contract`: Add typed evidence-bundle models and helper surfaces under watchtower_core.evidence.
- `task.plan_evidence_bundle_helper_foundation.refactor_live_plan_evidence_callers`: Use the new helper for initiative bootstrap evidence bundles and evidence-index summaries.
- `task.plan_evidence_bundle_helper_foundation.reconcile_evidence_requirements_and_docs`: Update requirements.md and evidence package docs to reflect the broadened reusable evidence boundary.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
