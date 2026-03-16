---
id: task.core_split_compatibility_wrapper_retirement.wrapper_retirement.002
trace_id: trace.core_split_compatibility_wrapper_retirement
title: Retire repo-specific compatibility wrappers from export-safe namespaces
summary: Remove repo-specific query, sync, and aggregate-validation wrapper modules
  and move remaining callers to direct repo_ops or reusable imports.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T04:10:51Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/query/
- core/python/src/watchtower_core/sync/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/cli/
- core/python/tests/unit/test_repo_ops_boundary.py
related_ids:
- prd.core_split_compatibility_wrapper_retirement
- design.features.core_split_compatibility_wrapper_retirement
- design.implementation.core_split_compatibility_wrapper_retirement
- decision.core_split_compatibility_wrapper_retirement_direction
- contract.acceptance.core_split_compatibility_wrapper_retirement
---

# Retire repo-specific compatibility wrappers from export-safe namespaces

## Summary
Remove repo-specific query, sync, and aggregate-validation wrapper modules and move remaining callers to direct repo_ops or reusable imports.

## Scope
- Replace repo-local imports that still depend on `watchtower_core.query.<module>`, `watchtower_core.sync.<module>`, or `watchtower_core.validation.all`.
- Remove retired leaf wrapper modules or replace them with explicit boundary guardrails where only the package root should remain.
- Tighten regression coverage so the wrapper paths do not quietly reappear.

## Done When
- Repo-local code and tests no longer depend on the retired compatibility wrapper modules.
- The top-level query, sync, and aggregate-validation surfaces no longer forward repo-specific behavior through export-safe leaf modules.
- Targeted boundary coverage proves the wrapper retirement instead of preserving the legacy paths.
