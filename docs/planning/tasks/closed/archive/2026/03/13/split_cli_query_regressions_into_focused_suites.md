---
id: task.typed_query_surface_modularity_hardening.query_suite_modularity.003
trace_id: trace.typed_query_surface_modularity_hardening
title: Split CLI query regressions into focused suites
summary: Replace the broad CLI query regression hotspot with narrower family-specific
  suites and shared command helpers while preserving real command coverage and JSON
  assertions.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T18:21:56Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/unit/
- core/python/src/watchtower_core/cli/
- core/python/src/watchtower_core/control_plane/README.md
related_ids:
- prd.typed_query_surface_modularity_hardening
- design.features.typed_query_surface_modularity_hardening
- design.implementation.typed_query_surface_modularity_hardening
- decision.typed_query_surface_modularity_hardening_direction
- contract.acceptance.typed_query_surface_modularity_hardening
depends_on:
- task.typed_query_surface_modularity_hardening.model_modularity.002
---

# Split CLI query regressions into focused suites

## Summary
Replace the broad CLI query regression hotspot with narrower family-specific suites and shared command helpers while preserving real command coverage and JSON assertions.

## Scope
- Split the mixed-family CLI query regression suite into focused files with better failure locality.
- Keep route-preview, dry-run planning, and query command coverage on real CLI entrypoints.

## Done When
- The monolithic CLI query hotspot is replaced with focused suites and one small shared helper.
- Coverage for current command families and JSON payload expectations is preserved by targeted regressions.
