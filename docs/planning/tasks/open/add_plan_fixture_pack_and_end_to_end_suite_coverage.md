---
id: task.plan_domain_pack_core_validation.plan_fixture_pack.004
trace_id: trace.plan_domain_pack_core_validation
title: Add plan fixture pack and end-to-end suite coverage
summary: Adds the plan pack test fixture, temp-repo materialization, and end-to-end
  suite validation coverage.
type: task
status: active
task_status: backlog
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T20:36:31Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/fixtures/
- core/python/tests/
related_ids:
- prd.plan_domain_pack_core_validation
- design.features.plan_domain_pack_core_validation
- design.implementation.plan_domain_pack_core_validation
- contract.acceptance.plan_domain_pack_core_validation
depends_on:
- task.plan_domain_pack_core_validation.core_suite_runtime.003
---

# Add plan fixture pack and end-to-end suite coverage

## Summary
Adds the plan pack test fixture, temp-repo materialization, and end-to-end suite validation coverage.

## Scope
- Add the plan fixture pack source under Python test fixtures.
- Materialize the fixture into domain_packs/plan/.wt/ during tests and cover fail-closed validation paths.

## Done When
- The plan fixture pack validates end to end through validate suite in tests.
- Negative tests cover invalid schema, validator, and suite references.
