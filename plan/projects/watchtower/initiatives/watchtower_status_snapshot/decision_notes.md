# WatchTower Status Snapshot Decision Notes

## Summary
Capture the minimal choices that keep the status snapshot slice bounded.

## Decisions
- Keep `watchtower doctor` as the bootstrap diagnostics surface and add `watchtower status` as the operator-facing workspace summary.
- Report compact counts and recent work summaries instead of introducing a new rendered artifact family inside the product repo.
- Keep the status command read-only and local-first in this slice.
