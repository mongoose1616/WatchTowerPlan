---
trace_id: "trace.preimplementation_repo_review_and_hardening"
id: "prd.preimplementation_repo_review_and_hardening"
title: "Pre-Implementation Repository Review and Hardening PRD"
summary: "Defines the review-driven work needed to streamline planning coordination, shrink low-value documentation entrypoints, and harden watchtower_core for future configurable external pack use before product implementation begins."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T17:55:24Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/"
  - "workflows/"
  - "core/control_plane/"
  - "core/python/"
aliases:
  - "preimplementation repo readiness"
  - "repo review and hardening"
---

# Pre-Implementation Repository Review and Hardening PRD

## Record Metadata
- `Trace ID`: `trace.preimplementation_repo_review_and_hardening`
- `PRD ID`: `prd.preimplementation_repo_review_and_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.preimplementation_machine_coordination_entrypoint`
- `Linked Designs`: `design.features.preimplementation_repo_readiness`
- `Linked Implementation Plans`: `design.implementation.preimplementation_repo_hardening_execution`
- `Updated At`: `2026-03-10T17:55:24Z`

## Summary
Defines the review-driven work needed to streamline planning coordination, shrink low-value documentation entrypoints, and harden `watchtower_core` for future configurable external pack use before product implementation begins.

## Problem Statement
The repository is green today, but a full pre-implementation review shows three structural readiness gaps. First, a few high-traffic README surfaces still act like directory dumps instead of compact entrypoints, which wastes tokens and duplicates machine lookup surfaces. Second, the planning system already has the right source-of-truth families, but the machine coordination entrypoint is not explicit enough for an LLM or agent-first workflow, so contributors still have to infer whether `initiative`, `traceability`, `prd`, `design`, or `task` lookup is the right starting surface. Third, the exported core still has large monolithic Python modules and no first-class way to merge supplemental schema sets for future external pack-owned artifacts such as CTF schemas.

## Goals
- Preserve the current repository's green baseline while tightening pre-implementation readiness.
- Reduce low-value documentation surface area in high-traffic README entrypoints.
- Make one machine coordination entrypoint explicit for traced work without collapsing the authored planning families.
- Make `watchtower_core` more modular and more configurable for future external schema and artifact consumers.

## Non-Goals
- Starting WatchTower product implementation.
- Adding CTF or domain-pack runtime behavior inside `WatchTowerPlan`.
- Collapsing PRDs, decisions, designs, implementation plans, and tasks into one authored planning family.
- Replacing the current traceability or task-authority model with a new ad hoc tracker.

## Target Users or Actors
- Maintainers and agents navigating repository state before implementation begins.
- Future `WatchTower` consumers that need configurable schema loading and clearer reusable package seams.
- Reviewers who need one machine coordination view for traced work without opening several planning families first.

## Key Scenarios
- An agent needs to determine the current state of a traced initiative and should be able to start from one machine coordination surface instead of guessing between several indexes.
- A maintainer needs to orient inside `docs/references/`, `docs/commands/core_python/`, or `core/python/` without reading a long file inventory that duplicates governed lookup surfaces.
- A future product repo needs to validate pack-owned schemas and artifacts through `watchtower_core` without moving those schemas into this repository's canonical control plane.

## Requirements
- `req.preimplementation_repo_review_and_hardening.001`: The initiative must publish a traced review and remediation chain with a PRD, feature design, implementation plan, decision record, acceptance contract, planning evidence, and bounded execution tasks.
- `req.preimplementation_repo_review_and_hardening.002`: High-traffic README entrypoints must become compact, high-signal orientation surfaces instead of full directory dumps, and the README standard must prevent that drift from recurring.
- `req.preimplementation_repo_review_and_hardening.003`: The repository must keep the current authored planning families but make one primary machine coordination entrypoint explicit for traced work.
- `req.preimplementation_repo_review_and_hardening.004`: `watchtower_core` must reduce monolithic package surfaces by splitting the largest coordination-facing modules into cleaner family modules with compatibility-preserving imports.
- `req.preimplementation_repo_review_and_hardening.005`: `watchtower_core` must support supplemental schema loading for future external pack-owned artifacts without treating `core/control_plane/` as the only schema source forever.
- `req.preimplementation_repo_review_and_hardening.006`: The repository must remain green on the current validation baseline throughout this initiative.

## Acceptance Criteria
- `ac.preimplementation_repo_review_and_hardening.001`: The planning corpus publishes the active PRD, decision record, feature design, implementation plan, bootstrap task, and open task set for this initiative.
- `ac.preimplementation_repo_review_and_hardening.002`: `docs/references/README.md`, `docs/commands/core_python/README.md`, and `core/python/README.md` become compact orientation surfaces, and the README standard plus template prevent future exhaustive directory-dump inventories where they add little value.
- `ac.preimplementation_repo_review_and_hardening.003`: The repository explicitly documents and exposes one primary machine coordination path for traced work, and that path is usable without reparsing multiple planning indexes manually.
- `ac.preimplementation_repo_review_and_hardening.004`: The largest core coordination-facing modules are split into more modular package surfaces, and future external schema sets can be merged into validation without modifying the local schema catalog.
- `ac.preimplementation_repo_review_and_hardening.005`: The repository passes the current `doctor`, `validate all`, `pytest`, `mypy`, and `ruff` baseline after the hardening work lands.

## Success Metrics
- High-traffic README entrypoints are short enough to scan quickly and no longer duplicate long file inventories.
- An agent can answer "what is active and what do I open next?" through one documented machine coordination path.
- Future external schema consumers can register supplemental schemas without patching this repo's canonical schema catalog.

## Risks and Dependencies
- Over-consolidating planning surfaces could destroy useful authored boundaries instead of clarifying entrypoints.
- Supplemental schema loading could accidentally blur the difference between this repo's canonical schema catalog and consumer-owned schema overlays if the boundary is not explicit.
- Compatibility-preserving module splits could leave stale imports behind unless tests and docs move in the same change sets.

## Open Questions
- Whether future external consumers should adopt a published overlay-catalog format or stay with programmatic schema registration until a second repo proves the need for a governed shared format.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the remediation should reduce ambiguity and coupling instead of adding ceremony-only layers.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable and machine-readable surfaces must stay synchronized as the coordination and README boundaries tighten.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): the repo should stop at shared substrate hardening and future-ready generic seams rather than starting product or pack implementation.

## References
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [template_and_output_efficiency.md](/home/j/WatchTowerPlan/docs/planning/prds/template_and_output_efficiency.md)
- [git_workflow_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_workflow_standard.md)

## Updated At
- `2026-03-10T17:55:24Z`
