# WatchTower Work Item Bootstrap Decision Notes

## Summary
Capture the minimal choices that keep the work-item slice bounded.

## Decisions
- Require an initialized workspace manifest before creating work-item records.
- Keep work-item records in JSON under `.watchtower/work_items/` so the on-disk state remains inspectable and local-first.
- Start with a single `work start` command and one `planned` status instead of designing a full work-item lifecycle yet.
