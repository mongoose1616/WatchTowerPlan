---
trace_id: trace.standard_runtime_and_route_explicitness
id: design.features.standard_runtime_and_route_explicitness
title: Standard, Runtime, and Route Explicitness Hardening Feature Design
summary: Defines the technical design boundary for Standard, Runtime, and Route Explicitness
  Hardening.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T06:44:04Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/src/watchtower_core/
- docs/commands/core_python/
- workflows/ROUTING_TABLE.md
---

# Standard, Runtime, and Route Explicitness Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.standard_runtime_and_route_explicitness`
- `Design ID`: `design.features.standard_runtime_and_route_explicitness`
- `Design Status`: `active`
- `Linked PRDs`: `prd.standard_runtime_and_route_explicitness`
- `Linked Decisions`: `decision.standard_runtime_and_route_explicitness_direction`
- `Linked Implementation Plans`: `design.implementation.standard_runtime_and_route_explicitness`
- `Updated At`: `2026-03-11T06:44:04Z`

## Summary
Defines the technical design boundary for Standard, Runtime, and Route Explicitness Hardening.

## Source Request
- User request to review the March 2026 external report set, verify each focus-area finding against the live repository, and carry every still-valid issue through planning, implementation, validation, status updates, and commit closeout.

## Scope and Feature Boundary
- Covers one authored operationalization shape for governed standards plus the derived standard-index, query, doc, and test changes that keep it machine-readable.
- Covers package-level README documentation for the major `watchtower_core` package boundaries plus workspace-level runtime navigation updates.
- Covers advisory route-preview matching improvements, command-doc updates, and tests for realistic free-form maintenance requests.
- Excludes a full semantic router, package extraction, domain-pack implementation, and the broader planning-document contract-unification program.

## Current-State Context
- `core/control_plane/indexes/standards/standard_index.v1.json` currently captures citation and reference usage, but it still has no owner or operationalization fields beyond what can be inferred from prose.
- `core/python/src/watchtower_core/` currently has no package-level README files, so runtime ownership and supported import expectations have to be inferred from code and older planning docs.
- `watchtower-core route preview --request "review /home/j/WatchTower/report and fix the valid issues with planning, tasks, validation, and commits"` currently returns no selected routes because the scoring model requires exact trigger-phrase matches before any token overlap matters.
- The March 2026 review concerns around foundation alignment, maintenance freshness loops, and layered health reporting no longer reproduce as open defects in the live repo, so this initiative should stay tightly scoped to the remaining explicitness gaps.
- `core/python/src/watchtower_core/repo_ops/planning_documents.py` already centralizes runtime planning-document validation, which means the earlier contract-duplication concern is not the bounded change target for this slice.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): authored operationalization metadata and package-boundary docs should strengthen explicit seams instead of adding hidden side registries.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the remaining report findings should be closed with fail-closed validation and durable lookup alignment rather than informal guidance alone.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): route-preview hardening should improve maintainability workflows without changing the repo's human-governed routing authority.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): standard documents stay the source of truth, so operationalization metadata belongs in the governed standard shape.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): package-boundary docs and route-scoring work should preserve stable contracts while reducing ambiguity.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the trace should join the planning chain, standards work, runtime docs, command docs, and acceptance evidence coherently.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): query and route-preview behavior changes must be reflected in the governed command surfaces.

## Design Goals and Constraints
- Make operationalization explicit in authored sources rather than inventing another hidden Python-only truth surface.
- Keep runtime boundary docs aligned with the current public package shape, including the compatibility guards already present in `query`, `sync`, and `validation`.
- Preserve the advisory nature of route preview; it must help routing, not silently replace human workflow authority.
- Keep the initiative small enough to validate and close in one bounded remediation cycle.

## Options Considered
### Option 1
- Add only narrative docs and leave the standard index plus route-preview scoring unchanged.
- Strength: minimal code churn.
- Tradeoff: leaves the most important machine-queryability and routing gaps unresolved.

### Option 2
- Add authored operationalization metadata to standard docs, derive it into the standard index and query surfaces, publish package READMEs, and harden route-preview scoring with deterministic token-aware matching.
- Strength: closes the reproduced gaps without creating a second authority surface or overbuilding a semantic router.
- Tradeoff: requires a broad but mechanical standards backfill and careful scoring thresholds to avoid noisy route matches.

### Option 3
- Add a new operationalization registry plus a stronger autonomous routing layer that tries to infer full workflow intent from free-form prompts.
- Strength: would maximize machine-first behavior.
- Tradeoff: oversteps the current authority model and creates too much new machinery for a bounded remediation slice.

## Recommended Design
### Architecture
- Add a required `Operationalization` section to governed standard documents and treat that section as the authored source for standard-operationalization metadata.
- Extend the standard-index sync path, schema, typed model, query service, and command payloads so the derived index publishes operationalization modes plus the linked workflows, validators, commands, templates, and implementation surfaces.
- Add package-level README files for the major `watchtower_core` packages and give each one a consistent boundary block with classification, supported imports, non-goals, and related surfaces.
- Keep route preview on the current route index, but expand the scoring model to account for normalized token matches across task types and trigger keywords even when the request does not contain exact routing-table phrases.

### Data and Interface Impacts
- Touched standard docs under `docs/standards/**` gain a new required section with structured operationalization bullets.
- `core/control_plane/schemas/artifacts/standard_index.v1.schema.json` and the live plus example standard-index artifacts gain operationalization fields.
- `watchtower-core query standards` gains richer output and matching over the new operationalization fields.
- `docs/commands/core_python/watchtower_core_query_standards.md` and `docs/commands/core_python/watchtower_core_route_preview.md` must reflect the new behavior.

### Execution Flow
1. Backfill a compact `Operationalization` section into every live standard using one consistent metadata shape.
2. Rebuild the standard index from those authored sections and expose the new fields through the typed model, query service, schema, examples, and tests.
3. Publish package-level runtime READMEs and update `core/python/README.md` to route maintainers toward the classified package boundaries and supported imports.
4. Harden route-preview scoring and tests so realistic broad maintenance requests produce the intended merged workflow set while the command remains advisory.

### Invariants and Failure Cases
- The standard document remains the normative authority. The standard index is still a derived lookup surface.
- Route preview must not claim certainty or execution authority; it must continue to report warnings and merged workflow sets only.
- Package READMEs must describe the current supported boundary, including compatibility shims, instead of promising future extraction work.
- Validation must fail when a live standard omits the required operationalization shape or when the derived standard index drifts from authored metadata.

## Affected Surfaces
- docs/standards/
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/src/watchtower_core/
- docs/commands/core_python/
- workflows/ROUTING_TABLE.md
- core/python/tests/
- core/control_plane/schemas/artifacts/standard_index.v1.schema.json
- core/control_plane/examples/valid/indexes/standard_index.v1.example.json
- core/control_plane/examples/invalid/indexes/standard_index_external_without_urls.v1.example.json

## Design Guardrails
- Do not move standard-operationalization authority into a new standalone registry when the standard docs themselves can carry the source metadata.
- Do not classify repo-local orchestration packages as reusable core just to satisfy next-phase aspirations.
- Do not relax route-preview matching so far that common single tokens like `review` or `task` match every route indiscriminately.

## Risks
- A full standards backfill may expose ambiguous operationalization ownership for a few standards and require explicit reviewer-only classification.
- Route scoring changes may surface multiple low-signal matches until thresholds are tuned against realistic requests.
- Package README docs can drift if future refactors change exports without same-change updates to the new boundary docs.

## References
- [standard_runtime_and_route_explicitness_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md)
- [workflow_operationalization_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/workflow_operationalization_direction.md)
- [core_export_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_hardening.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
