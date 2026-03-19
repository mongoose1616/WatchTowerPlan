# Plan Routing Engine Export Foundation Design Record

## Summary
Publishes a reusable routing engine package so route selection is available through a stable runtime API instead of only query helpers and CLI handlers.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_routing_engine_export_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Design Notes
- The exported routing engine should wrap governed route-preview selection instead of duplicating route-scoring logic in another implementation branch.
- The new package should be reusable-core only and fail closed against repo-local routing handlers.
- This slice should treat request-text routing and explicit task-type routing as the stable exported selection modes.
