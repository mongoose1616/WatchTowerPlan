# Plan Event Stream Helper Foundation Implementation Slice

## Summary
Extracts a reusable event-stream helper for initiative and task event records, then refactors initiative package event writes onto it so requirements.md and decisions.md no longer depend on ad hoc repo-local event recording.

## Initial Work Breakdown
- `task.plan_event_stream_helper_foundation.publish_event_stream_helper_contracts`: Add a reusable helper for seeded event records, append-only event writes, and deterministic replay over plan pack initiative and task streams.
- `task.plan_event_stream_helper_foundation.refactor_initiative_package_event_writes_onto_helper`: Move initiative and task event creation in initiative_packages.py onto the reusable helper without changing current event contracts.
- `task.plan_event_stream_helper_foundation.validate_event_stream_helper_and_contracts`: Add tests proving seeded records, append behavior, replay ordering, and initiative package regressions stay aligned with requirements.md and decisions.md.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
