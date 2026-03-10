---
id: task.unit_test_hardening_and_rebalancing.suite_rebalance.001
trace_id: trace.unit_test_hardening_and_rebalancing
title: Rebalance unit suite structure and docs
summary: Split the oversized CLI test surface, add shared fixture support, and update
  unit-suite documentation to match the suite's actual boundary and contributor patterns.
type: task
status: active
task_status: backlog
task_kind: documentation
priority: medium
owner: repository_maintainer
updated_at: '2026-03-10T23:36:39Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests
- core/python/tests/unit
- core/python/tests/fixtures
related_ids:
- prd.unit_test_hardening_and_rebalancing
- design.features.unit_test_hardening_and_rebalancing
- design.implementation.unit_test_hardening_and_rebalancing
depends_on:
- task.unit_test_hardening_and_rebalancing.bootstrap.001
---

# Rebalance unit suite structure and docs

## Summary
Split the oversized CLI test surface, add shared fixture support, and update unit-suite documentation to match the suite's actual boundary and contributor patterns.

## Scope
- Split CLI coverage into focused family-oriented test modules and keep only thin parser or smoke coverage at the top level.
- Add shared fixture helpers and a small conftest layer for repeated repo-subset and JSON-loading patterns.
- Update unit-suite documentation to describe the hybrid unit or contract boundary honestly.

## Done When
- The CLI suite is no longer centered in one expanding test file.
- Shared fixture support exists and the unit-test README reflects the implemented layout.
