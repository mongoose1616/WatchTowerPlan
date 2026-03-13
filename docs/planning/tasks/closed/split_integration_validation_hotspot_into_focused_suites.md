---
id: task.validation_test_hotspot_rebalancing.integration_suite_split.002
trace_id: trace.validation_test_hotspot_rebalancing
title: Split integration validation hotspot into focused suites
summary: Replace the remaining mixed-family integration validation hotspot with focused
  suites, small helpers, and aligned integration-suite inventory coverage.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T19:10:03Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/integration/README.md
- core/python/src/watchtower_core/control_plane/loader.py
- core/python/src/watchtower_core/validation/artifact.py
- core/python/src/watchtower_core/repo_ops/validation/example_artifacts.py
- core/python/src/watchtower_core/repo_ops/validation/all.py
related_ids:
- prd.validation_test_hotspot_rebalancing
- design.features.validation_test_hotspot_rebalancing
- design.implementation.validation_test_hotspot_rebalancing
- decision.validation_test_hotspot_rebalancing_direction
- contract.acceptance.validation_test_hotspot_rebalancing
---

# Split integration validation hotspot into focused suites

## Summary
Replace the remaining mixed-family integration validation hotspot with focused suites, small helpers, and aligned integration-suite inventory coverage.

## Scope
- Split the integration hotspot along real validation-family boundaries.
- Keep repository-aware loader, schema, example, front-matter, and authored-contract assertions live.
- Refresh integration README inventory coverage for the focused suite layout and compatibility marker.

## Done When
- The old integration hotspot is replaced by focused suites plus one small shared helper.
- Current loader, schema, example, front-matter, and authored-contract coverage still runs against live repository surfaces.
- The integration README describes the new suite family and the compatibility marker path.
