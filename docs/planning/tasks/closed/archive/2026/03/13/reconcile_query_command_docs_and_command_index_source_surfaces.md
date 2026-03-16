---
id: task.query_family_source_surface_alignment.command_doc_and_index_reconciliation.002
trace_id: trace.query_family_source_surface_alignment
title: Reconcile query command docs and command index source surfaces
summary: Align query command docs, command index records, and adjacent discovery surfaces
  with the split query family ownership model.
type: task
status: active
task_status: done
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T22:04:28Z'
audience: shared
authority: authoritative
applies_to:
- docs/commands/core_python/
- core/control_plane/indexes/commands/command_index.v1.json
- core/python/tests/unit/test_route_and_query_handlers.py
related_ids:
- prd.query_family_source_surface_alignment
- design.features.query_family_source_surface_alignment
- design.implementation.query_family_source_surface_alignment
- decision.query_family_source_surface_alignment_direction
depends_on:
- task.query_family_source_surface_alignment.introspection_mapping_hardening.001
---

# Reconcile query command docs and command index source surfaces

## Summary
Align query command docs, command index records, and adjacent discovery surfaces with the split query family ownership model.

## Scope
- Update affected query command pages so command tables and source-surface sections point to the correct family and handler files.
- Refresh the command index and adjacent command discovery surfaces so machine-readable lookup matches the docs.

## Done When
- Affected query command docs no longer point at stale umbrella or main entrypoint files.
- Command discovery returns implementation paths that match the authored command pages and parser-backed metadata.
