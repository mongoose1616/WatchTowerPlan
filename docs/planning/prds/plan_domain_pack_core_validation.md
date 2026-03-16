---
trace_id: trace.plan_domain_pack_core_validation
id: prd.plan_domain_pack_core_validation
title: Plan Domain Pack Core Validation PRD
summary: Move validation into reusable core with pack-aware schema, validator, and
  suite loading, then prove it end to end with a plan domain-pack fixture.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-16T20:32:05Z'
audience: shared
authority: authoritative
---

# Plan Domain Pack Core Validation PRD

## Record Metadata
- `Trace ID`: `trace.plan_domain_pack_core_validation`
- `PRD ID`: `prd.plan_domain_pack_core_validation`
- `Status`: `active`
- `Linked Decisions`: `decision.plan_domain_pack_core_validation_direction`
- `Linked Designs`: `design.features.plan_domain_pack_core_validation`
- `Linked Implementation Plans`: `design.implementation.plan_domain_pack_core_validation`
- `Updated At`: `2026-03-16T20:32:05Z`

## Summary
Move validation into reusable core with pack-aware schema, validator, and suite loading, then prove it end to end with a plan domain-pack fixture.

## Problem Statement
- `watchtower_core.validation` already exposes reusable schema-backed validators, but suite orchestration and repo-baseline execution still live under `watchtower_core.repo_ops.validation`.
- The current exported validation path can validate one external artifact through supplemental schemas, but it cannot load a pack-declared schema catalog, validator registry, and validation suite as one coherent reusable-core contract.
- The domain-pack direction captured in the Step 1 workbook requires validation to become reusable core behavior that enforces pack-owned schemas and cross-surface contracts without hard-coding WatchTowerPlan assumptions into shared runtime code.

## Goals
- Make validation selection, suite loading, and suite execution pack-aware reusable-core behavior.
- Keep WatchTowerPlan-specific Markdown semantic rules in `repo_ops`, while moving generic validation orchestration and pack contract enforcement into `watchtower_core.validation`.
- Prove the generic seam with a `plan` domain-pack fixture that materializes into `domain_packs/plan/.wt/` during tests.

## Non-Goals
- Introduce a live top-level `domain_packs/plan/` runtime owned by this repository.
- Move current WatchTowerPlan-specific document semantic rule implementations out of `watchtower_core.repo_ops.validation`.
- Change acceptance reconciliation semantics or the current evidence-writing contract beyond the updates required to support the new initiative.

## Requirements
- `req.plan_domain_pack_core_validation.001`: Reusable core must resolve validation through pack-declared startup surfaces so schema lookup, validator selection, and suite selection can come from a `pack_settings` load root rather than only the repository-default control-plane registry set.
- `req.plan_domain_pack_core_validation.002`: Reusable core must publish a governed `validation_suite_registry` contract, typed models, loader support, and runtime services that execute declared suite steps with fail-closed behavior.
- `req.plan_domain_pack_core_validation.003`: Reusable core must expose `watchtower-core validate suite --suite-id ... --pack-settings-path ...` and allow `validate artifact`, `validate front-matter`, and `validate document-semantics` to opt into pack-declared validator selection through `--pack-settings-path`.
- `req.plan_domain_pack_core_validation.004`: WatchTowerPlan must migrate its current aggregate validation entrypoint onto the reusable-core suite runtime while leaving repo-local semantic-rule providers and target enumeration explicit under `repo_ops.validation`.
- `req.plan_domain_pack_core_validation.005`: The repository must prove the design with a `plan` fixture pack under test fixtures that carries a pack-local schema catalog, validator registry, validation suite registry, and pack-owned artifacts, and the repository must remain green on the current sync, validation, test, typecheck, and lint baseline.

## Acceptance Criteria
- `ac.plan_domain_pack_core_validation.001`: The traced planning chain, decision, acceptance contract, planning-baseline evidence, and bounded task set define the initiative as reusable-core validation hardening plus one test-fixture `plan` domain pack.
- `ac.plan_domain_pack_core_validation.002`: Pack-aware validation can load a pack-declared schema catalog, validator registry, and validation suite registry through `pack_settings` without replacing the repository-default core schema catalog.
- `ac.plan_domain_pack_core_validation.003`: Reusable core publishes generic suite and pack-contract validation services, and `watchtower-core validate suite` executes declared `pack_contract`, `artifact`, `front_matter`, and `document_semantics` step kinds with fail-closed behavior.
- `ac.plan_domain_pack_core_validation.004`: A `plan` fixture pack materialized into `domain_packs/plan/.wt/` validates end to end through the reusable-core suite runner, and invalid schema, validator, or suite references fail closed in tests.
- `ac.plan_domain_pack_core_validation.005`: `watchtower-core validate all` remains practical for WatchTowerPlan by wrapping the reusable-core suite runtime, and the repository passes sync, aggregate validation, pytest, mypy, and ruff after the migration lands.

## Risks and Dependencies
- Pack-aware schema loading could overfit to the current repository if the merged-catalog contract is implemented as another repo-specific shortcut instead of a real pack-facing seam.
- Suite orchestration could become too abstract if the first version tries to solve pack-local sync or query behavior in the same slice; this initiative must stay focused on validation.
- The fixture pack must remain a test-only proof surface so the repository does not quietly cross its current scope boundary into hosting a live product pack.

## References
- [repository_scope.md](/docs/foundations/repository_scope.md)
- [validated_core_and_pack_data_shape_convergence.md](/docs/planning/design/features/validated_core_and_pack_data_shape_convergence.md)
- [python_validator_execution.md](/docs/planning/design/features/python_validator_execution.md)
- [repository_validation_standard.md](/docs/standards/validations/repository_validation_standard.md)
