---
id: task.post_rewrite_core_cleanup_and_surface_reduction.example_history_reconciliation.009
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Reconcile retired example corpus historical references
summary: Remove stale planning and derived-surface references that still name the
  retired control-plane example corpus as a live repository path.
type: task
status: active
task_status: done
task_kind: chore
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T09:02:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/
- core/control_plane/indexes/repository_paths/
- core/python/tests/
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
depends_on:
- task.post_rewrite_core_cleanup_and_surface_reduction.artifact_registry_retirement.008
---

# Reconcile retired example corpus historical references

## Summary
Remove stale planning and derived-surface references that still name the retired control-plane example corpus as a live repository path.

## Scope
- Reframe historical PRDs, designs, and decisions that still cite deleted `the retired control-plane example corpus` paths as if the corpus remains an active surface.
- Repair any derived repository-path metadata that still links current surfaces to the retired example corpus.
- Leave negative test assertions and clearly historical retirement notes intact when they no longer advertise the deleted paths as active repository structure.

## Done When
- Planning and repository-path surfaces no longer advertise `the retired control-plane example corpus` as a live path family.
- The remaining references to the retired example corpus are either removed or clearly historical without naming deleted paths as current canonical surfaces.

## Outcome
- Historical planning docs no longer advertise the deleted example corpus as a live repository path family.
- Repository-path sync now filters dead `related_paths`, so deleted surfaces do not persist indefinitely in the derived index.
- The only remaining exact example-corpus path literals are deliberate negative assertions in regression tests.
