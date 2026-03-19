# Plan Entrypoint Cutover Proof Decision Notes

## Summary
Capture the minimal choices that keep the plan authority entrypoint cutover bounded.

## Decisions
- Publish the plan-domain human start-here inside `plan/` now instead of waiting for the full workflow-root migration.
- Keep `core/workflows/ROUTING_TABLE.md` and `plan/workflows/ROUTING_TABLE.md` and the current workflow-module tree as the canonical routing backend for this slice; `plan/workflows/` is the human entrypoint, not yet a duplicate workflow engine.
- Update thin root router surfaces only enough to point humans at `plan/**` for live planning authority and current-state orientation.
