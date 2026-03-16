---
id: task.core_split_compatibility_wrapper_retirement.boundary_proof.003
trace_id: trace.core_split_compatibility_wrapper_retirement
title: Prove core boundary after wrapper retirement
summary: Align runtime package docs and boundary-proof tests with the smaller split-ready
  surface after compatibility wrapper retirement.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T04:11:09Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/README.md
- core/python/src/watchtower_core/query/README.md
- core/python/src/watchtower_core/sync/README.md
- core/python/src/watchtower_core/validation/README.md
- core/python/README.md
- core/python/tests/unit/test_repo_ops_boundary.py
related_ids:
- prd.core_split_compatibility_wrapper_retirement
- design.features.core_split_compatibility_wrapper_retirement
- design.implementation.core_split_compatibility_wrapper_retirement
- decision.core_split_compatibility_wrapper_retirement_direction
- contract.acceptance.core_split_compatibility_wrapper_retirement
---

# Prove core boundary after wrapper retirement

## Summary
Align runtime package docs and boundary-proof tests with the smaller split-ready surface after compatibility wrapper retirement.

## Scope
- Update runtime package READMEs and workspace guidance so supported imports match the retired wrapper surface.
- Replace compatibility-preservation assertions with explicit boundary-proof tests.
- Keep any remaining top-level reusable validation exports clearly documented and tested.

## Done When
- Package README guidance matches the post-retirement import boundary.
- Boundary-proof tests fail if repo-specific wrapper modules or re-exports return.
- The split-ready surface is explicit enough that future extraction work does not need to rediscover the package boundary.
