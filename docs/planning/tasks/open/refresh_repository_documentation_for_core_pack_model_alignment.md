---
id: task.documentation_surface_alignment_for_core_pack_model.refresh.002
trace_id: trace.documentation_surface_alignment_for_core_pack_model
title: Refresh repository documentation for core and pack model alignment
summary: Audit and refresh the documentation corpus so repository guidance matches
  the current reusable-core plus plan-domain-pack boundary.
type: task
status: active
task_status: ready
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T05:57:19Z'
audience: shared
authority: authoritative
related_ids:
- prd.documentation_surface_alignment_for_core_pack_model
- design.features.documentation_surface_alignment_for_core_pack_model
depends_on:
- task.documentation_surface_alignment_for_core_pack_model.bootstrap.001
---

# Refresh repository documentation for core and pack model alignment

## Summary
Audit and refresh the documentation corpus so repository guidance matches the current reusable-core plus plan-domain-pack boundary.

## Scope
- Update start-here docs, standards, command pages, and adjacent README surfaces that still point at retired repository shapes.
- Align wording around pack-settings startup, flat registries, derived pack projections, and transitional support surfaces.
- Repair any same-change command, tracking, or lookup drift the refresh exposes.

## Done When
- The bounded documentation set reflects the live repository shape consistently.
- No touched doc still presents deleted policy or retired bridge surfaces as live.
