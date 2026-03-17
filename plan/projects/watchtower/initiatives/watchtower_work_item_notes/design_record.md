# WatchTower Work Item Notes Design Record

## Summary
Adds local-first note capture on work items so operators can preserve thread context and resume a bounded slice without external scratch notes.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/projects/watchtower/initiatives/watchtower_work_item_notes/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
- The project container must stay valid and current before a project-scoped initiative may execute.
- Work-item notes should append to the existing `.watchtower/work_items/<slug>.json` records instead of creating a second note store.
- Each note should capture stable local metadata at append time: a note id, timestamp, and message.
- Note capture should require that the target work item already exists and should fail clearly when it does not.
- `watchtower work show` should continue to expose the full record, including any captured notes, without inventing a separate rendering layer.
