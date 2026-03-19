# Plan Live Evidence Closeout Review Indexes Foundation Design Record

## Summary
Adds the remaining live plan aggregate indexes for initiative-local evidence, closeout, and review state, while reconciling requirements.md so environment_context is no longer treated as a required clean-endstate contract.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_live_evidence_closeout_review_indexes_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Design Direction
- Build the new indexes inside `PlanWorkspaceService` so the existing authoritative rebuild path remains single-source.
- Keep the new entries derived entirely from initiative-local `.wt/` artifacts that already exist: validation bundles, closeout recaps, initiative review state, and promotion records.
- Keep review aggregation lightweight: summarize initiative review readiness and promotion approval state without introducing a separate `review_record` family.
- Treat `environment_context` as explicitly optional. Requirements should describe it as a demand-driven extension rather than a missing clean-endstate dependency.
