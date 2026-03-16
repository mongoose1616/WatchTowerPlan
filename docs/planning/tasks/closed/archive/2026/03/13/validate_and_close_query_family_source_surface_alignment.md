---
id: task.query_family_source_surface_alignment.validation_and_confirmation.003
trace_id: trace.query_family_source_surface_alignment
title: Validate and confirm query-family source-surface alignment
summary: Run targeted validation, full-repo validation, and repeated confirmation
  passes to prove the query-family source-surface slice is clean.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T22:08:31Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/unit/
- docs/commands/core_python/
- core/control_plane/indexes/commands/
related_ids:
- prd.query_family_source_surface_alignment
- design.features.query_family_source_surface_alignment
- design.implementation.query_family_source_surface_alignment
- decision.query_family_source_surface_alignment_direction
depends_on:
- task.query_family_source_surface_alignment.introspection_mapping_hardening.001
- task.query_family_source_surface_alignment.command_doc_and_index_reconciliation.002
---

# Validate and confirm query-family source-surface alignment

## Summary
Run targeted validation, full-repo validation, and repeated confirmation passes to prove the query-family source-surface slice is clean.

## Scope
- Run targeted parser, loader, command-doc, and command-discovery validation for the slice.
- Run full validation, then second-angle and adversarial confirmation probes across adjacent query-family surfaces.

## Done When
- Targeted and full validation passes are green on the final tree.
- Repeated confirmation passes find no new actionable issue under the same query-family source-surface theme.
