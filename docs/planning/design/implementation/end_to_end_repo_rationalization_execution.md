---
trace_id: "trace.end_to_end_repo_review_and_rationalization"
id: "design.implementation.end_to_end_repo_rationalization_execution"
title: "End-to-End Repository Rationalization Execution Plan"
summary: "Breaks the final pre-implementation review follow-up into bounded slices for documentation guardrails, derived metadata hardening, external pack validation seams, and query CLI modularity."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/"
  - "workflows/"
  - "core/control_plane/"
  - "core/python/src/watchtower_core/"
aliases:
  - "repo rationalization execution"
---

# End-to-End Repository Rationalization Execution Plan

## Record Metadata
- `Trace ID`: `trace.end_to_end_repo_review_and_rationalization`
- `Plan ID`: `design.implementation.end_to_end_repo_rationalization_execution`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.end_to_end_repo_review_and_rationalization`
- `Linked Decisions`: `decision.end_to_end_repo_rationalization_direction`
- `Source Designs`: `design.features.end_to_end_repo_rationalization`
- `Linked Acceptance Contracts`: `contract.acceptance.end_to_end_repo_review_and_rationalization`
- `Updated At`: `2026-03-10T19:43:34Z`

## Summary
Breaks the final pre-implementation review follow-up into bounded slices for documentation guardrails, derived metadata hardening, external pack validation seams, and query CLI modularity.

## Source Request or Design
- Feature design: [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
- PRD: [end_to_end_repo_review_and_rationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/end_to_end_repo_review_and_rationalization.md)
- Decision: [end_to_end_repo_rationalization_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/end_to_end_repo_rationalization_direction.md)

## Scope Summary
- Bootstrap the traced review-remediation initiative and publish the accepted direction.
- Add repo-local markdown-link validation and fix derived timestamp drift on coordination surfaces.
- Add file-system supplemental schema loading plus CLI support for external artifact validation.
- Split the query CLI into smaller family modules while preserving durable command behavior.

## Assumptions and Constraints
- Coordination surfaces remain the default start-here path and are not replaced in this initiative.
- Supplemental schema loading is bounded to schema files or directories and does not yet include supplemental validator registries.
- Query command behavior must stay stable from an operator perspective.
- Product implementation remains out of scope.

## Current-State Context
- The repository is green and currently has no active initiatives after the machine coordination closeout.
- The final review findings are narrow enough to land as three execution slices after bootstrap.
- README entrypoints and planning defaults are already lean enough that another README-only pass is not justified now.

## Internal Standards and Canonical References Applied
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): the new link rule must live in the governed semantics layer.
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/coordination_tracking_standard.md): tracker trust depends on timestamp correctness.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): supplemental schemas must stay outside the canonical catalog while validating fail closed.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): refactors should prefer smaller modules and stable contracts.

## Proposed Technical Approach
- Treat documentation guardrails and derived metadata as one trust-surface slice.
- Treat external pack validation as one extensibility slice centered on schema loading and `validate artifact`.
- Treat query modularity as one refactor slice with docs and tests in the same change set.

## Work Breakdown
1. Bootstrap the traced planning chain, accepted direction, acceptance contract, planning evidence, and bounded task set.
2. Add repo-local markdown-link validation and harden closeout-aware `updated_at` projections in traceability-derived initiative and coordination surfaces.
3. Add supplemental schema loading from files or directories and expose the seam through `watchtower-core validate artifact`.
4. Split query parser registration and runtime handlers into smaller family modules while keeping command docs and tests aligned.
5. Rebuild derived surfaces, rerun validation, close the remaining tasks, and close the initiative.

## Dependencies
- Existing document semantics validation and sync registry infrastructure.
- Existing programmatic supplemental schema support in `SchemaStore`.
- Existing command docs and command-index sync flow.

## Risks
- Metadata hardening could widen the diff footprint in derived surfaces, so tests and closeout expectations need to stay explicit.
- CLI extensibility could be underpowered if future packs need validator overlays immediately; that stays intentionally deferred.
- Query modularity can create import drift unless compatibility tests stay green.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json` after planning or governed-surface changes.
- Run `./.venv/bin/watchtower-core validate all --format json` after each slice.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/mypy src`, and `./.venv/bin/ruff check .` after code slices.
- Add targeted tests for repo-local link validation, closeout-aware timestamp projection, supplemental schema loading from files and directories, external artifact validation, and query family modularity regressions.

## Rollout or Migration Plan
- Land one planning bootstrap commit first.
- Land one commit for trust-surface guardrails and derived metadata hardening.
- Land one commit for external pack validation seams.
- Land one commit for query CLI modularity.
- Land a final closeout commit after the repo is green and the initiative tasks are terminal.

## References
- [end_to_end_repo_review_and_rationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/end_to_end_repo_review_and_rationalization.md)
- [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
- [end_to_end_repo_rationalization_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/end_to_end_repo_rationalization_direction.md)

## Updated At
- `2026-03-10T19:43:34Z`
