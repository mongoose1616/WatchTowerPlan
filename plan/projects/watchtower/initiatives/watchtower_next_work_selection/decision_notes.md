# WatchTower Next Work Selection Decision Notes

## Summary
Capture the minimal choices that keep the next-work slice bounded.

## Decisions
- Keep next-work selection local-first and deterministic over the existing work-item records.
- Surface the latest note inline with the selected work item instead of creating a separate resume artifact.
- Keep the `work item` concept, but treat the exact `watchtower work ...` CLI surface as bootstrap-stage and provisional until a later slice hardens the downstream product contract.
- Defer any richer prioritization or scheduling policy to a later slice.
