# WatchTower Work Item Begin Flow Decision Notes

## Summary
Capture the minimal choices that keep the begin-flow slice bounded.

## Decisions
- Use `watchtower work begin` for the first explicit active-work transition and keep `watchtower work start` as the record-creation command.
- Treat repeated begin requests on an already active work item as a no-op instead of creating a second lifecycle status or extra event log.
- Keep the work-item concept intact while still treating the exact `watchtower work ...` CLI surface as bootstrap-stage and provisional.
- Defer pause, reassignment, and richer lifecycle policy to later slices.
