---
trace_id: trace.plan_domain_pack_core_validation
id: design.features.plan_domain_pack_core_validation
title: Plan Domain Pack Core Validation Feature Design
summary: Defines the technical design boundary for Plan Domain Pack Core Validation.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-16T20:32:05Z'
audience: shared
authority: authoritative
---

# Plan Domain Pack Core Validation Feature Design

## Record Metadata
- `Trace ID`: `trace.plan_domain_pack_core_validation`
- `Design ID`: `design.features.plan_domain_pack_core_validation`
- `Design Status`: `active`
- `Linked PRDs`: `prd.plan_domain_pack_core_validation`
- `Linked Decisions`: `decision.plan_domain_pack_core_validation_direction`
- `Linked Implementation Plans`: `design.implementation.plan_domain_pack_core_validation`
- `Updated At`: `2026-03-16T20:32:05Z`

## Summary
Defines the technical design boundary for Plan Domain Pack Core Validation.

## Source Request
- User request to move validation out of `repo_ops` and into reusable core because domain packs also need the same validation contract.
- Domain-pack direction requiring generic validation, pack-owned schemas, and pack-declared contracts proved through a `plan` domain-pack pilot.

## Scope and Feature Boundary
- This design covers pack-aware schema loading, pack-declared validator and suite loading, reusable-core suite execution, a reusable pack-contract validator, and the repo-local migration of `validate all` onto that reusable-core runtime.
- This design also covers a test-fixture `plan` domain pack whose artifacts are materialized into `domain_packs/plan/.wt/` inside temp repos to prove the new contract end to end.
- This design intentionally excludes live product-pack runtime ownership under a top-level `domain_packs/` tree, pack-local sync or query behavior, and migration of WatchTowerPlan-specific Markdown semantic rules out of `repo_ops.validation`.

## Current-State Context
- `SchemaStore` already supports supplemental schemas, and `ControlPlaneLoader` already materializes `PackContext` through `pack_settings`, but validation still resolves schemas and validators from the repository-default control plane only.
- `watchtower_core.validation` currently exports schema-backed artifact validation, front-matter validation, and acceptance reconciliation, while `watchtower_core.repo_ops.validation` still owns aggregate validation and document-semantics execution.
- `watchtower-core validate artifact` can validate one external artifact through `--schema-id` plus `--supplemental-schema-path`, but there is no pack-declared validator registry or suite contract that turns those pieces into a reusable baseline for a future domain pack.

## Foundations References Applied
- [repository_scope.md](/docs/foundations/repository_scope.md): The proof pack must stay a test fixture instead of becoming a live product-pack subtree in this repository.
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): The runtime must remain deterministic, fail closed, and schema-first.

## Internal Standards and Canonical References Applied
- [core/python/README.md](/core/python/README.md): Export-safe reusable behavior belongs under `watchtower_core.validation`, while repo-local orchestration stays explicit under `repo_ops`.
- [repository_validation_standard.md](/docs/standards/validations/repository_validation_standard.md): The migration must preserve a practical repo-baseline validation path and finish with the normal sync, validation, test, typecheck, and lint checks.
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): New governed artifact families need published schemas and fail-closed validation behavior.
- [validated_core_and_pack_data_shape_convergence.md](/docs/planning/design/features/validated_core_and_pack_data_shape_convergence.md): Pack settings remain the canonical load root and must declare any new validation-facing governed surfaces.

## Design Goals and Constraints
- Make pack-facing validation load paths generic enough that a future pack can publish its own schema catalog, validator registry, and suite registry without patching the repository-owned registry set.
- Preserve the current WatchTowerPlan boundary by keeping repo-specific semantic rule providers and repo-baseline target enumeration explicit under `repo_ops.validation`.
- Keep acceptance reconciliation unchanged in this slice.
- Preserve the current `watchtower-core validate all` user experience even though its runtime moves under reusable core.

## Options Considered
### Option 1
- Keep suite orchestration and pack selection logic in `repo_ops.validation`.
- Smallest change to current code paths.
- Fails the domain-pack requirement because reusable core would still not own the generic validation contract.

### Option 2
- Move all validation behavior, including WatchTowerPlan-specific document semantic rules and repo target enumeration, into reusable core.
- Produces one seemingly simple validation namespace.
- Overreaches the current repository boundary by embedding repo-local semantics into exported core behavior.

### Option 3
- Move pack-aware schema, validator, suite, and pack-contract validation into reusable core, while keeping WatchTowerPlan-specific semantic providers and repo target enumeration under `repo_ops.validation`.
- Aligns with the current core-versus-pack boundary and gives future packs a reusable validation contract.
- Requires a little more plumbing between reusable-core services and repo-local wrappers.

## Recommended Design
### Architecture
- Add a governed `validation_suite_registry` artifact family under `core/control_plane/registries/`, with a schema, typed model, and loader support declared in `pack_settings`.
- Add a reusable-core `PackValidationContext` that loads pack settings, resolves a merged schema store, loads the pack-declared validator registry and validation suite registry, and makes those surfaces available to reusable validation services.
- Add reusable-core `ValidationSuiteService` and `PackContractValidationService` under `watchtower_core.validation`.
- Update leaf validation services so `artifact`, `front-matter`, and `document-semantics` can resolve validators from an optional `pack_settings_path`, falling back to the repository-default registry when no pack path is provided.
- Keep repo-local semantic rule implementations and repo-baseline target enumeration under `watchtower_core.repo_ops.validation`, but make `validate all` call into the reusable-core suite runner instead of maintaining its own aggregate runtime contract.

### Data and Interface Impacts
- New governed schema and registry family: `validation_suite_registry`.
- `pack_settings` gains one declared `validation_suite_registry` surface.
- `ControlPlaneLoader` and `SchemaStore` gain pack-aware loading paths for merged schema catalogs and pack-selected validator or suite registries.
- `watchtower-core validate suite --suite-id ... --pack-settings-path ...` becomes the new reusable-core suite CLI surface.
- `watchtower-core validate artifact|front-matter|document-semantics` gain optional `--pack-settings-path`.

### Execution Flow
1. A caller selects a pack through `pack_settings_path` or falls back to the repository-default core validation context.
2. Reusable core builds a `PackValidationContext` by loading pack settings, merging the repository core schema catalog with any pack-local catalog, and loading the declared validator and suite registries.
3. Leaf validation services resolve validators from that active context instead of assuming the repository-default validator registry.
4. `ValidationSuiteService` loads the requested suite, executes its declared steps in order, and returns a structured suite result with per-step records.
5. `PackContractValidationService` validates the pack-declared startup surfaces and registry coherence before artifact- or document-level validation proceeds.
6. WatchTowerPlan's `validate all` wrapper builds the repo baseline suite inputs and delegates execution to the reusable-core suite runtime.

### Invariants and Failure Cases
- Duplicate schema IDs between the repository core catalog and a pack-local catalog must fail closed.
- Unknown pack-declared validator IDs, suite IDs, or suite step kinds must fail closed.
- A pack contract is invalid when required pack-declared surfaces are missing, mis-typed, or declare unresolved schema or validator references.
- The repository-default validation path must still work when no `pack_settings_path` is supplied.

## Affected Surfaces
- `core/control_plane/schemas/artifacts/`
- `core/control_plane/registries/`
- `core/control_plane/manifests/pack_settings.json`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/validation/`
- `core/python/src/watchtower_core/repo_ops/validation/`
- `core/python/src/watchtower_core/cli/`
- `core/python/tests/`
- `docs/commands/core_python/`
- `docs/planning/`

## Design Guardrails
- Do not create a live repo-owned `domain_packs/plan/` runtime tree outside test fixtures in this initiative.
- Do not move WatchTowerPlan-specific semantic rule implementations into reusable-core exports.
- Do not treat supplemental schemas as a replacement for pack-declared schema catalogs; both seams must remain distinct.

## Risks
- The merged schema-catalog contract could create cache invalidation or duplicate-schema edge cases if loader reuse is not handled carefully.
- The first suite contract could become a dumping ground for repo-local behavior if the step kinds are not kept narrow.
- Boundary tests must stay explicit so reusable-core exports do not silently regress back into repo-local wrappers later.

## References
- [plan_domain_pack_core_validation.md](/docs/planning/prds/plan_domain_pack_core_validation.md)
- [python_validator_execution.md](/docs/planning/design/features/python_validator_execution.md)
- [validated_core_and_pack_data_shape_convergence.md](/docs/planning/design/features/validated_core_and_pack_data_shape_convergence.md)
