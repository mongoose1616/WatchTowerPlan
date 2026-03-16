---
trace_id: trace.plan_domain_pack_core_validation
id: decision.plan_domain_pack_core_validation_direction
title: Plan Domain Pack Core Validation Direction Decision
summary: Records the initial direction decision for Plan Domain Pack Core Validation.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T20:32:05Z'
audience: shared
authority: supporting
---

# Plan Domain Pack Core Validation Direction Decision

## Record Metadata
- `Trace ID`: `trace.plan_domain_pack_core_validation`
- `Decision ID`: `decision.plan_domain_pack_core_validation_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.plan_domain_pack_core_validation`
- `Linked Designs`: `design.features.plan_domain_pack_core_validation`
- `Linked Implementation Plans`: `design.implementation.plan_domain_pack_core_validation`
- `Updated At`: `2026-03-16T20:32:05Z`

## Summary
Records the initial direction decision for Plan Domain Pack Core Validation.

## Decision Statement
Generic validation orchestration, pack-aware schema and validator loading, and pack-declared suite execution will move into reusable core, while WatchTowerPlan-specific semantic-rule providers stay under `repo_ops.validation`, and the proof pack will be a `plan` test fixture rather than a live repo-owned domain pack.

## Trigger or Source Request
- User request to make validation core-owned because domain packs also need the same enforcement contract.
- Need to prove the design with a concrete pack shape instead of leaving the work at the level of an abstraction-only seam.

## Current Context and Constraints
- The repository already has `pack_settings`, generic pack-facing schemas, and `PackContext`, but validation still assumes the repository-default schema and validator registry set.
- Repository scope explicitly does not include a live external product-pack runtime yet, so the first proof must stay within test fixtures.

## Applied References and Implications
- [repository_scope.md](/docs/foundations/repository_scope.md): The `plan` pack proof must remain a test fixture and not become a live repository-owned product-pack runtime.
- [validated_core_and_pack_data_shape_convergence.md](/docs/planning/design/features/validated_core_and_pack_data_shape_convergence.md): `pack_settings` remains the load root and any new validation surface must be pack-declared there.
- [python_validator_execution.md](/docs/planning/design/features/python_validator_execution.md): Validator identity and selection remain governed by authored registries rather than hidden Python-only configuration.

## Affected Surfaces
- `docs/planning/prds/plan_domain_pack_core_validation.md`
- `docs/planning/design/features/plan_domain_pack_core_validation.md`
- `docs/planning/design/implementation/plan_domain_pack_core_validation.md`
- `core/control_plane/registries/`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/validation/`
- `core/python/src/watchtower_core/repo_ops/validation/`

## Options Considered
### Option 1
- Keep aggregate validation and pack-aware loading in `repo_ops.validation`.
- Minimizes immediate refactor cost.
- Leaves the reusable-core boundary incomplete for future domain packs.

### Option 2
- Move all validation behavior, including WatchTowerPlan-specific semantic rules, into reusable core.
- Produces one validation namespace.
- Violates the current core-versus-pack boundary by exporting repo-local semantics as reusable behavior.

### Option 3
- Move generic validation loading and suite execution into reusable core, keep repo-local semantic-rule providers under `repo_ops.validation`, and prove the design with a `plan` test fixture pack.
- Matches the current repository boundary while still delivering a real pack-facing proof.
- Requires a more explicit handoff between reusable-core services and repo-local wrappers.

## Chosen Outcome
Choose Option 3. Reusable core will own pack-aware validation loading, suite registry execution, and pack-contract enforcement. WatchTowerPlan will keep its semantic-rule implementations and current repo-baseline target enumeration under `repo_ops.validation`, but those repo-local pieces will flow through the reusable-core runtime. The `plan` proof pack will live under test fixtures and materialize into temp repos as `domain_packs/plan/.wt/`.

## Rationale and Tradeoffs
- This option satisfies the domain-pack requirement without turning the repository into a live product-pack host.
- It preserves the reusable-core versus repo-local boundary already established elsewhere in the repository.
- It adds more plumbing than a repo-local-only change, but that cost is the point of the initiative: make the validation contract truly reusable.

## Consequences and Follow-Up Impacts
- `validation_suite_registry` becomes a new governed control-plane family.
- Leaf validation commands need a pack-selection path.
- Boundary tests and README surfaces must be updated to reflect that suite orchestration is now reusable core behavior.

## Risks, Dependencies, and Assumptions
- The merged schema-catalog contract must fail closed on duplicates.
- The fixture-pack proof assumes the repository can keep pack source under test fixtures while still materializing the future-facing `domain_packs/plan/.wt/` layout in temp repos.
- Acceptance reconciliation remains unchanged in this initiative and must continue to work with the new validation runtime.

## References
- [plan_domain_pack_core_validation.md](/docs/planning/prds/plan_domain_pack_core_validation.md)
- [plan_domain_pack_core_validation.md](/docs/planning/design/features/plan_domain_pack_core_validation.md)
- [repository_scope.md](/docs/foundations/repository_scope.md)
