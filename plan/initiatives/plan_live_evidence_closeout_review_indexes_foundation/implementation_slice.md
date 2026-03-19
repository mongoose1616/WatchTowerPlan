# Plan Live Evidence Closeout Review Indexes Foundation Implementation Slice

## Summary
Adds the remaining live plan aggregate indexes for initiative-local evidence, closeout, and review state, while reconciling requirements.md so environment_context is no longer treated as a required clean-endstate contract.

## Initial Work Breakdown
- `task.plan_live_evidence_closeout_review_indexes_foundation.reconcile_environment_context_scope`: Remove environment_context from the required clean-endstate surfaces and align supporting requirements rows.
- `task.plan_live_evidence_closeout_review_indexes_foundation.implement_live_indexes`: Add aggregate index contracts, rebuild logic, and query surfaces for initiative-local evidence, closeout, and review state.
- `task.plan_live_evidence_closeout_review_indexes_foundation.validate_rebuild_and_requirements_alignment`: Add coverage for the new aggregates, sync behavior, and updated requirements current-state rows.

## Planned Surfaces
- `plan/.wt/indexes/evidence_index.json`
- `plan/.wt/indexes/closeout_index.json`
- `plan/.wt/indexes/review_index.json`
- Query services and CLI lookups for those live plan aggregates
- Updated plan pack settings, schema catalog, validator registry, artifact-family registry, and requirements status tables

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
