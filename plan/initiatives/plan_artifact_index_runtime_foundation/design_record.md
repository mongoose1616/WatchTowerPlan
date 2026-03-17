# Plan Artifact Index Runtime Foundation Design Record

## Summary
Publishes the missing live plan artifact index, removes legacy artifact-index field leakage, and exposes the cross-family query surface required by requirements.md and decisions.md.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_artifact_index_runtime_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The new artifact index must be a live `plan/.wt/` aggregate sourced from current plan-owned machine artifacts rather than frozen `docs/planning/**` history.
- The generic artifact-index contract must stop leaking legacy `challenge` and source-platform vocabulary and instead carry plan-safe provenance fields that can be reused by other packs.
- The first runtime slice should cover current plan artifact families and aggregate indexes without inventing a second authority path outside the live plan workspace.
