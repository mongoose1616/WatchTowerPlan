# Plan Generic Query Harness Export Foundation Design Record

## Summary
Exports a reusable generic query surface from watchtower_core.query and refactors export-safe query services onto that public boundary so requirements.md and decisions.md no longer depend on a guardrail-only query root.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_generic_query_harness_export_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
