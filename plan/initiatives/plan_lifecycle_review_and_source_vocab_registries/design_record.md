# Plan Lifecycle Review And Source Vocab Registries Design Record

## Summary
Adds the missing lifecycle-stage, review-status, and source-type registries plus typed helper coverage so plan-pack workflow semantics stop living only in scattered schema enums and runtime string literals.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_lifecycle_review_and_source_vocab_registries/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
