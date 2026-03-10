---
trace_id: "trace.core_export_hardening_followup"
id: "prd.core_export_hardening_followup"
title: "Core Export Hardening Follow-Up PRD"
summary: "Defines the follow-up work needed to make export-oriented sync snapshots dependency-correct, repair command implementation metadata, and harden the public boundary around repo-specific services."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T15:24:07Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/"
  - "core/control_plane/"
  - "docs/planning/design/"
aliases:
  - "core export hardening"
  - "post review export follow-up"
---

# Core Export Hardening Follow-Up PRD

## Record Metadata
- `Trace ID`: `trace.core_export_hardening_followup`
- `PRD ID`: `prd.core_export_hardening_followup`
- `Status`: `active`
- `Linked Decisions`: `None`
- `Linked Designs`: `design.features.core_export_hardening`
- `Linked Implementation Plans`: `design.implementation.core_export_hardening_execution`
- `Updated At`: `2026-03-10T15:24:07Z`

## Summary
Defines the follow-up work needed to make export-oriented sync snapshots dependency-correct, repair command implementation metadata, and harden the public boundary around repo-specific services.

## Problem Statement
The prior export-readiness initiative landed the main architecture split and closed cleanly, but the review surfaced three follow-up issues that still weaken the package as an export-ready core. Output-directory sync runs can materialize internally inconsistent snapshots, the command index now points every command at the thin root CLI entrypoint instead of the real command-family implementation surface, and the public `watchtower_core` namespace still advertises repo-specific query, sync, and aggregate validation services as if they were export-safe.

## Goals
- Make `sync all --output-dir` and `sync coordination --output-dir` dependency-correct.
- Restore useful command implementation metadata after the CLI split.
- Make the repo-specific boundary explicit in the public Python API so future extraction does not preserve the wrong top-level contract.
- Keep the repo green and traced while the fixes land.

## Non-Goals
- Reopening the closed `trace.core_export_readiness_and_optimization` initiative.
- Adding new product features, new domain-pack behavior, or CTF implementation work.
- Redesigning the control-plane schemas beyond what the review findings require.

## Target Users or Actors
- Maintainers materializing sync snapshots for review, release prep, or derived-surface inspection.
- Engineers using command metadata to navigate CLI implementation surfaces.
- Future `WatchTower` consumers that need a stable reusable public boundary instead of repo-specific convenience exports.

## Key Scenarios
- An engineer runs `watchtower-core sync all --output-dir /tmp/snapshot` and expects later derived artifacts to reflect earlier generated outputs from that snapshot, not stale canonical repo files.
- A contributor queries the command index and needs the implementation path to point at the actual command-family source surface instead of the thin root entrypoint.
- A future consumer imports `watchtower_core` and should not be steered toward `WatchTowerPlan`-specific query, sync, or aggregate validation APIs from top-level modules.

## Requirements
- `req.core_export_hardening_followup.001`: Output-directory sync orchestration must read earlier generated artifacts from the materialized snapshot when later targets depend on them.
- `req.core_export_hardening_followup.002`: Command metadata must publish implementation paths that reflect the actual command-family surface instead of the thin root CLI entrypoint for every command.
- `req.core_export_hardening_followup.003`: Top-level export-safe Python namespaces must stop advertising repo-specific query, sync, and aggregate validation services as first-class reusable APIs.
- `req.core_export_hardening_followup.004`: The follow-up initiative must preserve current repo behavior, traceability, and validation posture while the hardening work lands.

## Acceptance Criteria
- `ac.core_export_hardening_followup.001`: The planning corpus publishes an active PRD, feature design, implementation plan, closed bootstrap task, and durable task set for `trace.core_export_hardening_followup`.
- `ac.core_export_hardening_followup.002`: Output-directory sync runs produce dependency-correct coordination artifacts and have regression coverage for stale-canonical-index scenarios.
- `ac.core_export_hardening_followup.003`: Command index entries publish useful command-family implementation paths rather than reporting `cli/main.py` for every command.
- `ac.core_export_hardening_followup.004`: Top-level export-safe Python surfaces no longer advertise repo-specific query, sync, or aggregate validation services as reusable APIs, and repo-specific consumers import them from `repo_ops`.
- `ac.core_export_hardening_followup.005`: The repository remains green on the current validation baseline while the hardening work lands and closes.

## Success Metrics
- `sync all --output-dir` can be trusted to materialize a self-consistent derived snapshot.
- Command-index consumers can navigate from command metadata to the right command-family source file without manual guesswork.
- The remaining public API surface aligns with the intended reusable-versus-repo-specific boundary.

## Risks and Dependencies
- If the output-directory overlay is implemented too narrowly, some later sync targets may still read stale canonical artifacts.
- Tightening the top-level public boundary will require coordinated internal import updates and could expose hidden assumptions in tests or CLI code.
- The initiative depends on the current export-readiness refactor and its existing repo-ops split.

## Open Questions
- Whether a later extraction should keep compatibility shims for one release cycle once the reusable package boundary is published outside this repo.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the hardening work should make the package more deterministic and boundary-explicit rather than relying on convenience indirection.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable and machine-readable companion surfaces must remain aligned while the boundary and sync behavior tighten.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): follow-up hardening should improve the shared substrate without starting product implementation work.

## References
- [core_export_readiness_and_optimization.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_readiness_and_optimization.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_export_readiness_execution.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_export_readiness_execution.md)

## Updated At
- `2026-03-10T15:24:07Z`
