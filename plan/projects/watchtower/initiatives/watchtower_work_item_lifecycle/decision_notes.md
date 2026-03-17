# WatchTower Work Item Lifecycle Decision Notes

## Summary
Capture the minimal choices that keep the work-item lifecycle slice bounded.

## Decisions
- Keep work-item inspection and completion on the same local JSON records created by `watchtower work start`.
- Use one terminal `completed` status with optional closeout summary text instead of designing a larger lifecycle or review system yet.
- Keep `watchtower work list` and `watchtower work show` read-only; no editing or deletion commands land in this slice.
