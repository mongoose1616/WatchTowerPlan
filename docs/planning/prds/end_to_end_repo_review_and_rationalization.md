---
trace_id: "trace.end_to_end_repo_review_and_rationalization"
id: "prd.end_to_end_repo_review_and_rationalization"
title: "End-to-End Repository Review and Rationalization PRD"
summary: "Defines the final pre-implementation review follow-up needed to harden documentation guardrails, derived coordination metadata, external pack validation seams, and CLI modularity before WatchTower product implementation begins."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/"
  - "workflows/"
  - "core/control_plane/"
  - "core/python/"
aliases:
  - "end to end repo review"
  - "final preimplementation hardening"
---

# End-to-End Repository Review and Rationalization PRD

## Record Metadata
- `Trace ID`: `trace.end_to_end_repo_review_and_rationalization`
- `PRD ID`: `prd.end_to_end_repo_review_and_rationalization`
- `Status`: `active`
- `Linked Decisions`: `decision.end_to_end_repo_rationalization_direction`
- `Linked Designs`: `design.features.end_to_end_repo_rationalization`
- `Linked Implementation Plans`: `design.implementation.end_to_end_repo_rationalization_execution`
- `Updated At`: `2026-03-10T19:43:34Z`

## Summary
Defines the final pre-implementation review follow-up needed to harden documentation guardrails, derived coordination metadata, external pack validation seams, and CLI modularity before WatchTower product implementation begins.

## Problem Statement
The repository is substantially healthier than the earlier pre-implementation baseline, but the final end-to-end review still exposes four gaps that matter before product work starts. First, documentation links are currently clean, but link integrity is not fail-closed in repo validation, so drift can recur silently. Second, closeout state can materially change initiative and coordination surfaces while `updated_at` values remain behind the effective closeout timestamp, which weakens trust in current-state trackers for humans and agents. Third, exportable extensibility currently stops at programmatic supplemental schema objects; there is no first-class file or directory loading path for future external pack-owned artifacts such as CTF work-item notes or extraction outputs. Fourth, the query CLI still concentrates too much behavior in oversized parser and handler modules, which raises maintenance cost just before product-oriented expansion.

## Goals
- Keep the repository green while converting the highest-value review findings into durable guardrails and smaller code seams.
- Preserve the existing machine-first coordination path rather than reopening the planning-family model again.
- Make external pack validation practical without moving future pack-owned schemas into this repository's canonical control plane.
- Reduce maintenance risk in the highest-traffic CLI query surfaces before WatchTower implementation starts.

## Non-Goals
- Starting WatchTower product implementation or building the CTF pack itself.
- Replacing the existing coordination index and coordination tracker with another start-here artifact family.
- Collapsing PRDs, decisions, designs, plans, and tasks into one authored planning surface.
- Publishing a full external pack plugin system beyond the bounded schema-loading and artifact-validation seams needed now.

## Target Users or Actors
- Maintainers and agents relying on repo-local documentation links and current-state trackers.
- Future WatchTower consumers that need to validate pack-owned artifacts against pack-owned schemas without modifying `core/control_plane/`.
- Contributors maintaining the `watchtower-core` CLI as it grows beyond the current planning-only foundations.

## Key Scenarios
- A contributor adds or edits repo-local links in standards, workflow modules, or planning docs; validation should fail before a broken internal link lands.
- An initiative is closed and the coordination surfaces change immediately; `updated_at` should not imply stale current state after closeout.
- A future WatchTower pack owns schemas for CTF notes, extraction outputs, or promoted knowledge and needs `watchtower-core validate artifact` to work against those schemas directly from the pack.
- A maintainer needs to change one query subcommand without reopening a nearly thousand-line parser module and a thousand-line handler module.

## Requirements
- `req.end_to_end_repo_review_and_rationalization.001`: The initiative must publish a traced review-remediation chain with a PRD, decision record, feature design, implementation plan, acceptance contract, planning evidence, and bounded execution tasks.
- `req.end_to_end_repo_review_and_rationalization.002`: Repo-local markdown links must be validated fail-closed through the repository validation surface.
- `req.end_to_end_repo_review_and_rationalization.003`: Initiative, coordination, and derived planning trackers must keep `updated_at` semantics aligned with closeout-driven state changes.
- `req.end_to_end_repo_review_and_rationalization.004`: `watchtower_core` must support loading supplemental schema documents from explicit files or directories for future external pack-owned artifacts.
- `req.end_to_end_repo_review_and_rationalization.005`: The external artifact-validation path must be exposed through the CLI and documented for future pack use.
- `req.end_to_end_repo_review_and_rationalization.006`: The query CLI family must be split into smaller family-focused modules without changing the durable command contract.
- `req.end_to_end_repo_review_and_rationalization.007`: The repository must remain green on the current validation baseline throughout the initiative.

## Acceptance Criteria
- `ac.end_to_end_repo_review_and_rationalization.001`: The planning corpus publishes the PRD, decision record, feature design, implementation plan, acceptance contract, planning evidence, bootstrap task, and bounded execution tasks for this initiative.
- `ac.end_to_end_repo_review_and_rationalization.002`: Documentation semantics validation rejects broken repo-local links, and the current doc corpus passes the stronger rule.
- `ac.end_to_end_repo_review_and_rationalization.003`: Closeout-driven initiative and coordination surfaces publish timestamps that are consistent with the latest effective state change rather than stale pre-closeout values.
- `ac.end_to_end_repo_review_and_rationalization.004`: External supplemental schemas can be loaded from files or directories, and external artifacts can be validated through `watchtower-core validate artifact` without editing the canonical schema catalog.
- `ac.end_to_end_repo_review_and_rationalization.005`: Query parser registration and runtime handlers are split into smaller family modules, and command docs plus tests remain aligned.
- `ac.end_to_end_repo_review_and_rationalization.006`: The repository passes `doctor`, `validate all`, `pytest`, `mypy`, and `ruff` after the work lands.

## Success Metrics
- Broken repo-local links are prevented by automation instead of periodic manual review.
- Coordination and initiative start-here surfaces remain trustworthy after initiative closeout.
- A future WatchTower pack can validate pack-owned artifacts through core without patching this repo's schema catalog.
- The largest query CLI modules no longer dominate the Python workspace size profile.

## Risks and Dependencies
- Link validation can become noisy if it treats non-repo or intentionally non-file targets as hard failures.
- Timestamp-hardening work could create unnecessary churn if build-time timestamps replace source-driven timestamps indiscriminately.
- File and directory schema loading must preserve fail-closed behavior on duplicate schema IDs or invalid schema documents.
- Query-family refactors must keep command behavior stable even while internal modules move.

## Open Questions
- Whether future external pack validation should also accept supplemental validator-registry overlays after one second repository proves the need.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the follow-up work should remove ambiguity and coupling rather than add another navigation layer.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable and machine-readable surfaces must stay aligned as guardrails and extensibility seams evolve.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): core should stop at shared substrate hardening and future-ready pack seams rather than starting product behavior here.
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md): future pack-owned artifacts should be supportable by shared core without leaking domain-specific authority into this repo.

## References
- [preimplementation_repo_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/preimplementation_repo_review_and_hardening.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [machine_first_coordination_surface.md](/home/j/WatchTowerPlan/docs/planning/prds/machine_first_coordination_surface.md)

## Updated At
- `2026-03-10T19:43:34Z`
