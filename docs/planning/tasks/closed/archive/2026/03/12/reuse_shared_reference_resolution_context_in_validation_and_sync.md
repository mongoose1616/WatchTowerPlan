---
id: task.reference_resolution_reuse_hardening.shared_resolution_reuse.001
trace_id: trace.reference_resolution_reuse_hardening
title: Reuse shared reference-resolution context in validation and sync
summary: Eliminate repeated reference-index rebuilds by sharing reference-resolution
  context across workflow semantics validation and dependent sync families.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T15:14:07Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
related_ids:
- prd.reference_resolution_reuse_hardening
- design.features.reference_resolution_reuse_hardening
- design.implementation.reference_resolution_reuse_hardening
- decision.reference_resolution_reuse_hardening_direction
depends_on:
- task.reference_resolution_reuse_hardening.bootstrap.001
---

# Reuse shared reference-resolution context in validation and sync

## Summary
Eliminate repeated reference-index rebuilds by sharing reference-resolution context across workflow semantics validation and dependent sync families.

## Scope
- Add explicit shared reference-resolution helpers instead of rebuilding the reference index per workflow validation or per dependent sync service during sync-all orchestration.
- Keep workflow semantics, foundation-index, standard-index, workflow-index, and sync-all behavior unchanged apart from reuse of already-derived reference metadata.

## Done When
- Workflow semantics validation reuses one shared reference-resolution context per service run instead of rebuilding the reference index per workflow file.
- Sync-all orchestration reuses one reference-resolution context for reference-dependent sync targets without changing generated artifacts.
- Targeted regression tests prove the reuse behavior and the repository stays green on the normal validation baseline.
