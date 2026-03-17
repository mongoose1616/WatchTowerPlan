# Plan Event Stream Helper Foundation Design Record

## Summary
Extracts a reusable event-stream helper for initiative and task event records, then refactors initiative package event writes onto it so requirements.md and decisions.md no longer depend on ad hoc repo-local event recording.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_event_stream_helper_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
