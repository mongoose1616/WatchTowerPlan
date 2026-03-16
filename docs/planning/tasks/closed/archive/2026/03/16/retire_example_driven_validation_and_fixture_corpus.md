---
id: task.post_rewrite_core_cleanup_and_surface_reduction.example_validation_retirement.007
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Retire example-driven validation and fixture corpus
summary: Remove rewrite-era example-fixture validation from the active baseline and
  reconcile standards, tests, and historical references that still treat the corpus
  as authoritative.
type: task
status: active
task_status: done
task_kind: chore
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T08:12:00Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/tests/
- docs/standards/data_contracts/
- core/control_plane/contracts/acceptance/
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
depends_on:
- task.post_rewrite_core_cleanup_and_surface_reduction.inventory_contract_retirement.006
---

# Retire example-driven validation and fixture corpus

## Summary
Remove rewrite-era example-fixture validation from the active baseline and reconcile standards, tests, and historical references that still treat the corpus as authoritative.

## Scope
- Remove example-fixture coverage from `validate all`, schema-focused tests, and command or standards guidance where live artifacts or direct schema checks already cover the same contract.
- Retire the example helper code and the example corpus itself when the resulting validation model stays complete.
- Repair standards, acceptance contracts, and historical docs that currently point at example paths as active enforcement surfaces.

## Done When
- The active validation baseline no longer depends on `core/control_plane/examples/**`.
- Example-fixture references are reconciled across code, tests, standards, and acceptance surfaces in the same slice.
