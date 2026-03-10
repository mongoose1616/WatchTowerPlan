---
trace_id: "trace.end_to_end_repo_review_and_rationalization"
id: "design.features.end_to_end_repo_rationalization"
title: "End-to-End Repository Rationalization Design"
summary: "Defines the review-backed design for documentation link guardrails, closeout-consistent derived metadata, external pack validation seams, and smaller query CLI modules."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/"
  - "workflows/"
  - "core/control_plane/"
  - "core/python/src/watchtower_core/"
aliases:
  - "repo rationalization design"
  - "final review remediation design"
---

# End-to-End Repository Rationalization Design

## Record Metadata
- `Trace ID`: `trace.end_to_end_repo_review_and_rationalization`
- `Design ID`: `design.features.end_to_end_repo_rationalization`
- `Design Status`: `active`
- `Linked PRDs`: `prd.end_to_end_repo_review_and_rationalization`
- `Linked Decisions`: `decision.end_to_end_repo_rationalization_direction`
- `Linked Implementation Plans`: `design.implementation.end_to_end_repo_rationalization_execution`
- `Updated At`: `2026-03-10T19:43:34Z`

## Summary
Defines the review-backed design for documentation link guardrails, closeout-consistent derived metadata, external pack validation seams, and smaller query CLI modules.

## Source Request
- User request to conduct a full end-to-end repository review before WatchTower implementation and complete the resulting planning, tasking, implementation, validation, and closeout work.

## Scope and Feature Boundary
- Covers fail-closed repo-local markdown link validation for docs and workflow modules.
- Covers timestamp semantics for traceability-driven initiative and coordination views.
- Covers supplemental schema loading from files or directories and CLI-level external artifact validation.
- Covers internal query CLI modularity.
- Does not create a new planning artifact family or reopen README compaction work that is already in acceptable shape.
- Does not implement pack-owned runtime workflows, CTF orchestration, or external validator-engine overlays.

## Current-State Context
- Root and planning entrypoint READMEs are now compact enough for their role; the review did not justify another README-only initiative.
- Repo-local markdown links appear clean today, but there is no dedicated validation rule preventing future broken absolute repo links.
- `initiative_tracking.md` and `coordination_tracking.md` can change on closeout while still showing `_Updated At` values that trail the effective closeout timestamp.
- `SchemaStore` and `ControlPlaneLoader` accept programmatic supplemental schema documents, but future external pack consumers still lack a first-class file-system-driven loading path and CLI affordance.
- The largest remaining Python hotspots are [query_handlers.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/query_handlers.py) and [query_family.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/query_family.py), which are materially larger than the rest of the CLI workspace.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): new seams should be explicit, small, and deterministic.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): guardrails should fail closed and derived surfaces should not drift from their authoritative inputs.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): pack-oriented extensibility should remain generic and configurable inside shared core.

## Internal Standards and Canonical References Applied
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): semantic validation is the right home for repo-local markdown-link enforcement.
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/coordination_tracking_standard.md): the human coordination tracker remains the default start-here surface and should stay trustworthy after closeout.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): the initiative layer remains the deeper family-specific coordination view rather than being replaced again.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): supplemental schemas must stay outside the canonical catalog boundary while still validating fail closed.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): the refactor should prefer smaller modules and thin orchestration layers.

## Design Goals and Constraints
- Add the smallest useful documentation guardrail rather than a broad external-link crawler.
- Fix closeout timestamp drift without turning every sync run into needless timestamp churn.
- Make external pack validation practical without pretending those pack artifacts are owned by this repo.
- Reduce the size and maintenance cost of the query CLI while preserving the durable CLI contract and command docs.

## Options Considered
### Option 1
- Add another planning-graph artifact family and route both humans and machines through it.
- Strength: one more obvious planning entrypoint.
- Tradeoff: duplicates the role already played by the coordination index plus traceability join and adds more surface area instead of less.

### Option 2
- Keep the current planning-family model and coordination start-here path, add validation and metadata guardrails, expose external schema loading ergonomically, and shrink the query CLI into smaller family modules.
- Strength: addresses the concrete review findings without reopening already-stable boundaries.
- Tradeoff: keeps multiple specialized planning indexes in place rather than collapsing them.

### Option 3
- Limit the work to a review report and defer all code changes to later product work.
- Strength: lowest immediate implementation cost.
- Tradeoff: leaves known correctness and extensibility gaps unresolved immediately before product implementation.

## Recommended Design
### Planning Surface Direction
- Keep the authored planning families, the traceability index, and the coordination index as the current model.
- Keep `watchtower-core query coordination --format json` plus `docs/planning/coordination_tracking.md` as the default start-here surfaces.
- Record this choice explicitly so the review closes the “should we collapse planning families again?” question for the current pre-implementation phase.

### Documentation Guardrails
- Extend repo-local document semantics validation to check absolute markdown links that point back into `/home/j/WatchTowerPlan/`.
- Treat missing repo-local targets as validation failures.
- Keep the rule narrow to repo-local file links and do not attempt full external-link validation.

### Derived Metadata Hardening
- Treat closeout timestamps as effective state changes for traceability-derived initiative and coordination surfaces.
- Update root `updated_at` projections and tracker `_Updated At` values to consider `closed_at` where that is later than source-document timestamps.
- Keep the behavior source-driven rather than rebuild-time driven.

### External Pack Validation
- Add a helper that loads supplemental schema documents from explicit files or directories.
- Expose that helper in `SchemaStore` and `ControlPlaneLoader` construction paths.
- Extend `watchtower-core validate artifact` with file-system schema-loading options so external artifacts can be validated directly against pack-owned schemas.
- Document the pattern as a future WatchTower pack seam rather than a repo-owned artifact family.

### Query CLI Modularity
- Split parser registration and runtime handlers into family-focused query modules.
- Preserve the top-level `query` command family and current subcommand names.
- Keep query payload shapes stable and move only internal orchestration structure.

## Affected Surfaces
- `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`
- `core/python/src/watchtower_core/repo_ops/sync/traceability.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_tracking.py`
- `core/python/src/watchtower_core/repo_ops/sync/coordination_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/coordination_tracking.py`
- `core/python/src/watchtower_core/control_plane/schemas.py`
- `core/python/src/watchtower_core/control_plane/loader.py`
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_handlers.py`
- `core/python/src/watchtower_core/cli/validate_family.py`
- `core/python/src/watchtower_core/cli/validation_handlers.py`
- `docs/commands/core_python/`
- `docs/standards/`
- `core/python/tests/`

## Design Guardrails
- Do not add another planning entrypoint family while the coordination surfaces are already working.
- Do not make external pack schemas part of this repo's canonical schema catalog.
- Do not broaden doc semantics validation into network-dependent link checking.
- Do not change query command names, filter semantics, or output shapes in the modularity refactor.

## Implementation-Planning Handoff Notes
- Land the planning bootstrap and direction-setting decision first.
- Fix documentation guardrails and derived metadata in the same initiative because both affect trust in human and machine current-state surfaces.
- Land external pack validation before product implementation starts so the seam is available when WatchTower begins consuming core.
- Keep the query modularity slice separate enough that docs and tests can be validated cleanly after the refactor.

## Dependencies
- Existing document semantics validation and sync architecture.
- Existing supplemental-schema programmatic seam in the schema store.
- Existing command docs and command index sync behavior.

## Risks
- Narrow repo-local link validation may still miss other forms of stale references; that is acceptable for this bounded phase.
- External schema loading options could confuse canonical-vs-supplemental ownership if docs are not explicit.
- Query-family refactors are mechanically noisy and require strong regression tests.

## References
- [end_to_end_repo_review_and_rationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/end_to_end_repo_review_and_rationalization.md)
- [preimplementation_repo_readiness.md](/home/j/WatchTowerPlan/docs/planning/design/features/preimplementation_repo_readiness.md)
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/design/features/machine_first_coordination_surface.md)

## Updated At
- `2026-03-10T19:43:34Z`
