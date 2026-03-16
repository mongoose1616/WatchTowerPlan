---
id: task.plan_domain_pack_core_validation.core_suite_runtime.003
trace_id: trace.plan_domain_pack_core_validation
title: Add core validation suite runtime and pack contract validation
summary: Publishes the validation suite registry, reusable-core suite runtime, and
  pack-contract validator.
type: task
status: active
task_status: backlog
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T20:36:19Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/registries/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/cli/
related_ids:
- prd.plan_domain_pack_core_validation
- design.features.plan_domain_pack_core_validation
- design.implementation.plan_domain_pack_core_validation
- contract.acceptance.plan_domain_pack_core_validation
depends_on:
- task.plan_domain_pack_core_validation.pack_aware_loading.002
---

# Add core validation suite runtime and pack contract validation

## Summary
Publishes the validation suite registry, reusable-core suite runtime, and pack-contract validator.

## Scope
- Add the governed validation_suite_registry artifact family plus typed loader support.
- Implement reusable-core suite execution and pack-contract validation services.

## Done When
- Reusable core exposes suite and pack-contract validation services plus the validate suite CLI path.
- Suite execution supports pack_contract, artifact, front_matter, and document_semantics steps with fail-closed behavior.
