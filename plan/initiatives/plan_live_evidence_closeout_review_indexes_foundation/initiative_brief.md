# Plan Live Evidence Closeout Review Indexes Foundation

## Summary
Adds the remaining live plan aggregate indexes for initiative-local evidence, closeout, and review state, while reconciling requirements.md so environment_context is no longer treated as a required clean-endstate contract.

## Scope
- Add pack-level `evidence_index`, `closeout_index`, and `review_index` surfaces under `plan/.wt/indexes/`.
- Extend plan-workspace rebuilds, query services, artifact taxonomy, and validation coverage so those indexes are first-class machine surfaces.
- Reconcile `requirements.md` so `environment_context` is explicitly optional and out of scope for the current clean endstate.

## Non-Goals
- Do not add a durable `environment_context` artifact family or helper.
- Do not add a generic workflow-execution runtime in this slice.
- Do not broaden the evidence model beyond the existing initiative-local validation bundles already required by the live plan workspace.

## Identity
- `initiative_id`: `initiative.plan_live_evidence_closeout_review_indexes_foundation`
- `trace_id`: `trace.plan_live_evidence_closeout_review_indexes_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_live_evidence_closeout_review_indexes_foundation.reconcile_environment_context_scope`: Remove environment_context from the required clean-endstate surfaces and align supporting requirements rows.
- `task.plan_live_evidence_closeout_review_indexes_foundation.implement_live_indexes`: Add aggregate index contracts, rebuild logic, and query surfaces for initiative-local evidence, closeout, and review state.
- `task.plan_live_evidence_closeout_review_indexes_foundation.validate_rebuild_and_requirements_alignment`: Add coverage for the new aggregates, sync behavior, and updated requirements current-state rows.
