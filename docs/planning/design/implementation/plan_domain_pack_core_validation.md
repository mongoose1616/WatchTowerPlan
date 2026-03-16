---
trace_id: trace.plan_domain_pack_core_validation
id: design.implementation.plan_domain_pack_core_validation
title: Plan Domain Pack Core Validation Implementation Plan
summary: Breaks Plan Domain Pack Core Validation into a bounded implementation slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-16T20:32:05Z'
audience: shared
authority: supporting
---

# Plan Domain Pack Core Validation Implementation Plan

## Record Metadata
- `Trace ID`: `trace.plan_domain_pack_core_validation`
- `Plan ID`: `design.implementation.plan_domain_pack_core_validation`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.plan_domain_pack_core_validation`
- `Linked Decisions`: `decision.plan_domain_pack_core_validation_direction`
- `Source Designs`: `design.features.plan_domain_pack_core_validation`
- `Linked Acceptance Contracts`: `contract.acceptance.plan_domain_pack_core_validation`
- `Updated At`: `2026-03-16T20:32:05Z`

## Summary
Breaks Plan Domain Pack Core Validation into a bounded implementation slice.

## Source Request or Design
- [plan_domain_pack_core_validation.md](/docs/planning/design/features/plan_domain_pack_core_validation.md)
- User request to make validation core-owned and generic for domain packs, using a `plan` domain-pack proof instead of leaving the work as repo-only validation.

## Scope Summary
- This plan covers the traced execution slices required to publish pack-aware reusable-core validation, a governed validation suite registry, a reusable pack-contract validator, a `plan` fixture pack, and the repo-local migration of `validate all`.
- This plan intentionally excludes live product-pack runtime ownership, pack-local query and sync features, and migration of WatchTowerPlan-specific semantic rules into reusable-core exports.

## Assumptions and Constraints
- `pack_settings` remains the load root for validation-facing pack surfaces, and new validation contracts must be declared there rather than discovered heuristically.
- The `plan` pack is a test fixture only; it will be materialized into temp repos as `domain_packs/plan/.wt/` and not checked in as a live product-pack runtime.
- `validate all` must remain useful for the current repository even though the runtime ownership moves into reusable core.

## Internal Standards and Canonical References Applied
- [repository_validation_standard.md](/docs/standards/validations/repository_validation_standard.md): The completed slice must end with sync, aggregate validation, pytest, mypy, and ruff.
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): New validation-facing governed artifacts require schemas and fail-closed validation.
- [core/python/README.md](/core/python/README.md): Export-safe reusable validation behavior belongs under `watchtower_core.validation`; repo-local behavior stays explicit.
- [validated_core_and_pack_data_shape_convergence.md](/docs/planning/design/features/validated_core_and_pack_data_shape_convergence.md): Pack settings and declared surfaces remain the canonical startup boundary.

## Proposed Technical Approach
- Extend `SchemaStore` and `ControlPlaneLoader` with pack-aware catalog and registry loading so reusable-core validation can resolve pack-declared schemas and validators.
- Publish a new `validation_suite_registry` governed artifact family with typed models, loader support, and pack-settings declaration.
- Add reusable-core validation services for pack-contract validation and suite execution, then route repo-local aggregate validation through those services.
- Keep WatchTowerPlan-specific document semantic rules and repo-baseline target enumeration under `repo_ops.validation`, but treat them as inputs to reusable-core orchestration instead of owners of the orchestration contract.

## Work Breakdown
1. Replace the bootstrap planning placeholders with the final traced PRD, decision, implementation plan, acceptance contract, planning-baseline evidence, and bounded task chain.
2. Implement pack-aware schema and validator loading in reusable core so a pack-selected validation context can merge core-owned and pack-local schema catalogs.
3. Publish the `validation_suite_registry` artifact family and reusable-core suite or pack-contract validation services, including the `validate suite` CLI path.
4. Add the `plan` fixture pack source under test fixtures, materialize it into temp repos as `domain_packs/plan/.wt/`, and add end-to-end suite coverage plus fail-closed negative tests.
5. Migrate WatchTowerPlan's aggregate validation entrypoint and docs onto the reusable-core suite runtime, then run the final sync and validation closeout stack.

## Risks
- Pack-aware catalog merging and loader caching may regress current validation performance if typed caches are not keyed carefully.
- The suite contract may invite future overreach unless step kinds stay constrained to validation-only responsibilities.
- The repo-local to reusable-core handoff could blur package boundaries unless the export guardrail tests are refreshed in the same slice.

## Validation Plan
- Add unit coverage for pack-aware schema-store construction, pack-declared validator and suite loading, pack-contract validation, CLI parsing, and reusable-core boundary exports.
- Add integration coverage that materializes the `plan` fixture pack into `domain_packs/plan/.wt/` inside a temp repo and runs `validate suite` end to end.
- Finish with `./.venv/bin/watchtower-core sync all --write`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/python -m pytest`, `./.venv/bin/python -m mypy src`, and `./.venv/bin/ruff check src tests/unit tests/integration`.

## References
- [plan_domain_pack_core_validation.md](/docs/planning/prds/plan_domain_pack_core_validation.md)
- [plan_domain_pack_core_validation_direction.md](/docs/planning/decisions/plan_domain_pack_core_validation_direction.md)
- [python_validator_execution.md](/docs/planning/design/features/python_validator_execution.md)
