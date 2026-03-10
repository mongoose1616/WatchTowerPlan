---
trace_id: "trace.preimplementation_repo_review_and_hardening"
id: "design.implementation.preimplementation_repo_hardening_execution"
title: "Pre-Implementation Repository Hardening Execution Plan"
summary: "Breaks the repository review remediation into bounded slices for README entrypoints, machine coordination, and core modularity plus supplemental schema loading."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T17:55:24Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/"
  - "core/control_plane/"
  - "core/python/src/watchtower_core/"
aliases:
  - "preimplementation hardening plan"
---

# Pre-Implementation Repository Hardening Execution Plan

## Record Metadata
- `Trace ID`: `trace.preimplementation_repo_review_and_hardening`
- `Plan ID`: `design.implementation.preimplementation_repo_hardening_execution`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.preimplementation_repo_review_and_hardening`
- `Linked Decisions`: `decision.preimplementation_machine_coordination_entrypoint`
- `Source Designs`: `design.features.preimplementation_repo_readiness`
- `Linked Acceptance Contracts`: `contract.acceptance.preimplementation_repo_review_and_hardening`
- `Updated At`: `2026-03-10T17:55:24Z`

## Summary
Breaks the repository review remediation into bounded slices for README entrypoints, machine coordination, and core modularity plus supplemental schema loading.

## Source Request or Design
- Feature design: [preimplementation_repo_readiness.md](/home/j/WatchTowerPlan/docs/planning/design/features/preimplementation_repo_readiness.md)
- PRD: [preimplementation_repo_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/preimplementation_repo_review_and_hardening.md)
- Decision: [preimplementation_machine_coordination_entrypoint.md](/home/j/WatchTowerPlan/docs/planning/decisions/preimplementation_machine_coordination_entrypoint.md)

## Scope Summary
- Bootstrap the traced review initiative and open the bounded execution tasks.
- Compact the highest-traffic README entrypoints and tighten the README standard.
- Elevate the existing initiative index into the explicit machine coordination start-here surface for traced work.
- Split the largest core monoliths and add supplemental schema loading for future external pack-owned artifacts.

## Assumptions and Constraints
- Product implementation remains out of scope for this initiative.
- The initiative index stays derived from traceability, planning, and task sources.
- Supplemental schemas must extend validation without mutating this repo's authored schema catalog.
- Compatibility re-exports can be used during the refactor, but the final package shape should still be cleaner than the current one.

## Current-State Context
- The repository is currently green and has no active initiatives or open tasks.
- The current review findings are structural and localized enough to land in three bounded slices.
- The repo already has a deterministic coordination rebuild command, an initiative index, and query surfaces, so the work is refinement rather than a fresh subsystem bootstrap.

## Internal Standards and Canonical References Applied
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): README changes must preserve their quick-reference role.
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): coordination changes should strengthen the existing machine view instead of adding another family.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): core refactors should keep CLI entrypoints thin and behavior in package services.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): all code changes stay in the canonical Python workspace.

## Proposed Technical Approach
- Treat README compaction as a documentation-plus-standard slice.
- Treat machine coordination as an initiative-index and CLI-query slice rather than a new artifact-family slice.
- Treat modularity as one code-focused slice that splits handlers and models and adds supplemental schema registration to the schema store.

## Work Breakdown
1. Bootstrap the traced planning chain, acceptance contract, planning evidence, decision record, and bounded task set.
2. Compact README entrypoints and tighten the README standard and template so large directory dumps do not recur.
3. Enrich the initiative index with small active-task summaries, add `query coordination`, and update the planning guidance so this is the explicit machine start-here path for traced work.
4. Split the largest CLI-handler and control-plane-model modules into smaller family modules, add supplemental schema registration, update affected docs, and extend tests.
5. Rebuild derived surfaces, rerun validation, close the remaining tasks, and close the initiative.

## Dependencies
- Current command docs and command index infrastructure.
- Current initiative, task, and traceability indexes.
- Current schema store and workspace injection seams.

## Risks
- README compaction and coordination changes touch high-traffic guidance surfaces, so stale docs would be costly.
- Module splits can be mechanically noisy and must not obscure the logical change.
- Supplemental schema loading must fail closed when schema IDs collide or documents are invalid.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json` after planning or governed-surface changes.
- Run `./.venv/bin/watchtower-core validate all --format json` after each slice.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/mypy src`, and `./.venv/bin/ruff check .` after code slices.
- Add targeted tests for README-compaction assumptions only where validation can enforce them, for initiative coordination output, and for supplemental schema registration plus compatibility imports.

## Rollout or Migration Plan
- Land one planning bootstrap commit first.
- Land one commit for README compaction and standards.
- Land one commit for coordination entrypoint improvements.
- Land one or more coherent commits for modularity and supplemental schema loading depending on change-set size.
- Land a final closeout commit after the repo is green and the initiative tasks are terminal.

## References
- [preimplementation_repo_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/preimplementation_repo_review_and_hardening.md)
- [preimplementation_repo_readiness.md](/home/j/WatchTowerPlan/docs/planning/design/features/preimplementation_repo_readiness.md)
- [preimplementation_machine_coordination_entrypoint.md](/home/j/WatchTowerPlan/docs/planning/decisions/preimplementation_machine_coordination_entrypoint.md)

## Updated At
- `2026-03-10T17:55:24Z`
