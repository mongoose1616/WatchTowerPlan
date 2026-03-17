# WatchTower Work Item Notes Decision Notes

## Summary
Capture the minimal choices that keep the work-item notes slice bounded.

## Decisions
- Keep work-item notes inside the existing work-item JSON document instead of creating a separate note ledger.
- Treat notes as append-only entries with timestamped metadata rather than editable rich text.
- Reuse `watchtower work show` as the retrieval surface instead of adding a dedicated note view in this slice.
