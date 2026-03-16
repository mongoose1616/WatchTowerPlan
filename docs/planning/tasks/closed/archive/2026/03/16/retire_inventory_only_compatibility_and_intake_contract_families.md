---
id: task.post_rewrite_core_cleanup_and_surface_reduction.inventory_contract_retirement.006
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Retire inventory-only compatibility and intake contract families
summary: Remove the retained compatibility and intake contract families if they have
  no live runtime or workflow consumer and reconcile their remaining references.
type: task
status: active
task_status: done
task_kind: chore
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T07:07:33Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/contracts/
- core/control_plane/registries/
- core/control_plane/schemas/artifacts/
- core/python/tests/integration/test_control_plane_artifact_schema_contracts.py
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
depends_on:
- task.post_rewrite_core_cleanup_and_surface_reduction.inventory_manifest_retirement.004
---

# Retire inventory-only compatibility and intake contract families

## Summary
Remove the retained compatibility and intake contract families if they have no live runtime or workflow consumer and reconcile their remaining references.

## Scope
- Confirm the compatibility and intake contract families are inventory-only after the rewrite.
- Retire their contract, schema, validator, and registry surfaces when the consumer audit stays empty.
- Repair docs, tests, standards, and historical acceptance surfaces that still point at those families.

## Done When
- The compatibility and intake contract families are either removed cleanly or explicitly justified as still required by a live consumer.
- Full validation no longer treats those families as active governed surfaces without a runtime use case.
