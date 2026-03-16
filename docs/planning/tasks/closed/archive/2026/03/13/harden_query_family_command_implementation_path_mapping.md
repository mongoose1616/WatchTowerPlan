---
id: task.query_family_source_surface_alignment.introspection_mapping_hardening.001
trace_id: trace.query_family_source_surface_alignment
title: Harden query-family command implementation-path mapping
summary: Make parser-backed command metadata resolve query leaf commands to their
  owning split query family files without changing CLI behavior.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T22:04:28Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/introspection.py
- core/python/src/watchtower_core/cli/registry.py
- core/python/tests/unit/test_command_index_sync.py
- core/python/tests/unit/test_control_plane_loader.py
related_ids:
- prd.query_family_source_surface_alignment
- design.features.query_family_source_surface_alignment
- design.implementation.query_family_source_surface_alignment
- decision.query_family_source_surface_alignment_direction
---

# Harden query-family command implementation-path mapping

## Summary
Make parser-backed command metadata resolve query leaf commands to their owning split query family files without changing CLI behavior.

## Scope
- Add explicit query-subfamily implementation-path authority to CLI parser introspection.
- Keep command registration and runtime behavior unchanged while fixing the command-index source path.

## Done When
- Query leaf command specs resolve to the correct split query family implementation paths.
- Command-index sync and loader regressions pass against the updated source-path authority.
