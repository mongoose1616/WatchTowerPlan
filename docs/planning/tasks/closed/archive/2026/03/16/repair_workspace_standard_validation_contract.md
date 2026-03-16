---
id: task.post_rewrite_core_cleanup_and_surface_reduction.workspace_validation_contract.002
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
title: Repair workspace standard validation contract
summary: Reconcile the rewritten Python workspace standard with the integration assertion
  so full pytest passes again.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T06:40:30Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/engineering/python_workspace_standard.md
- core/python/tests/integration/test_control_plane_loader_and_foundation_contracts.py
related_ids:
- prd.post_rewrite_core_cleanup_and_surface_reduction
- design.features.post_rewrite_core_cleanup_and_surface_reduction
- design.implementation.post_rewrite_core_cleanup_and_surface_reduction
- decision.post_rewrite_core_cleanup_and_surface_reduction_direction
- contract.acceptance.post_rewrite_core_cleanup_and_surface_reduction
---

# Repair workspace standard validation contract

## Summary
Reconcile the rewritten Python workspace standard with the integration assertion so full pytest passes again.

## Scope
- Align the integration contract with the current guardrail-query and guardrail-sync wording.
- Preserve the intended repo_ops ownership boundary in both docs and tests.

## Done When
- core/python/.venv/bin/pytest -q passes the workspace standard integration assertion.
- The workspace standard and the integration test describe the same current package boundary.
