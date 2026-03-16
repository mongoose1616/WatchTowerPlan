---
id: task.plan_domain_pack_core_validation.repo_migration.005
trace_id: trace.plan_domain_pack_core_validation
title: Migrate repo validation onto core suite runtime
summary: Routes the WatchTowerPlan validation entrypoints and docs through the reusable-core
  suite runtime.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T21:40:56Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/cli/
- docs/commands/core_python/
related_ids:
- prd.plan_domain_pack_core_validation
- design.features.plan_domain_pack_core_validation
- design.implementation.plan_domain_pack_core_validation
- contract.acceptance.plan_domain_pack_core_validation
depends_on:
- task.plan_domain_pack_core_validation.core_suite_runtime.003
---

# Migrate repo validation onto core suite runtime

## Summary
Routes the WatchTowerPlan validation entrypoints and docs through the reusable-core suite runtime.

## Scope
- Refactor validate all so repo-baseline execution delegates to reusable-core suite services.
- Refresh docs, README surfaces, and boundary tests for the new core-versus-repo split.

## Done When
- validate all uses the reusable-core suite runtime without changing acceptance reconciliation behavior.
- Docs and boundary tests describe suite orchestration as reusable core behavior.
