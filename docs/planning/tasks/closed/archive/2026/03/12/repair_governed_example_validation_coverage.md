---
id: task.control_plane_example_validation_hardening.implementation.001
trace_id: trace.control_plane_example_validation_hardening
title: Repair governed example validation coverage
summary: Fix invalid valid examples and expand repository validation coverage over
  the governed example corpus.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T14:46:57Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/examples/valid/indexes/
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/tests/integration/
- core/python/tests/unit/
related_ids:
- prd.control_plane_example_validation_hardening
- design.features.control_plane_example_validation_hardening
- design.implementation.control_plane_example_validation_hardening
- decision.control_plane_example_validation_hardening_direction
- contract.acceptance.control_plane_example_validation_hardening
---

# Repair governed example validation coverage

## Summary
Fix invalid valid examples and expand repository validation coverage over the governed example corpus.

## Scope
- Fix the broken valid foundation and traceability examples.
- Extend aggregate or test-driven validation coverage so the governed example corpus is checked exhaustively.
- Repair the applies_to canonicality audit so nested governed markdown surfaces are actually scanned.

## Done When
- The valid foundation and traceability examples satisfy their schemas.
- The governed example corpus has durable automated validation coverage in the repo baseline.
- The applies_to canonicality audit exercises governed markdown documents recursively and without dead code.
