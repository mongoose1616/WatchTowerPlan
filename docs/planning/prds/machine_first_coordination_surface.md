---
trace_id: "trace.machine_first_coordination_surface"
id: "prd.machine_first_coordination_surface"
title: "Machine-First Coordination Surface PRD"
summary: "Defines the work needed to publish one always-useful machine coordination surface, keep human planning entrypoints derived from it, and reduce planning-navigation sprawl before product implementation starts."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T18:54:43Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/"
  - "core/control_plane/indexes/"
  - "core/python/src/watchtower_core/repo_ops/"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "machine coordination surface"
  - "coordination index initiative"
---

# Machine-First Coordination Surface PRD

## Record Metadata
- `Trace ID`: `trace.machine_first_coordination_surface`
- `PRD ID`: `prd.machine_first_coordination_surface`
- `Status`: `active`
- `Linked Decisions`: `decision.machine_first_coordination_entry_surface`
- `Linked Designs`: `design.features.machine_first_coordination_surface`
- `Linked Implementation Plans`: `design.implementation.machine_first_coordination_execution`
- `Updated At`: `2026-03-10T18:54:43Z`

## Summary
Defines the work needed to publish one always-useful machine coordination surface, keep human planning entrypoints derived from it, and reduce planning-navigation sprawl before product implementation starts.

## Problem Statement
The repository now has clean planning families and an explicit `query coordination` command, but the machine start-here surface is still incomplete. It projects only active initiatives, so it returns an empty result when no initiative is active, and agents still have to infer whether `initiative`, `task`, `traceability`, or README guidance is the right next surface. The planning system needs one derived machine-readable coordination artifact that is always useful, keeps family-specific indexes authoritative, and can drive a thin human byproduct instead of asking humans and agents to stitch state together ad hoc.

## Goals
- Publish one derived machine-readable coordination surface that is useful whether work is active or the repo is ready for a new initiative.
- Keep initiative, task, traceability, PRD, design, and decision indexes authoritative for their own families.
- Expose a thin human coordination byproduct so humans and agents start from the same current-state projection.
- Reduce planning-entry ambiguity without collapsing authored planning families.

## Non-Goals
- Replacing the existing family-specific indexes.
- Moving authored planning truth out of PRDs, decisions, designs, plans, or tasks.
- Starting WatchTower product implementation or adding CTF/domain-pack runtime logic.
- Creating a second authored planning family.

## Target Users or Actors
- Agents that need one deterministic machine start-here surface before choosing a family-specific index.
- Maintainers who need a concise planning current-state view without scanning multiple trackers.
- Future product work that should begin from a stable machine coordination contract instead of informal repository heuristics.

## Key Scenarios
- An agent asks what to open next and the repo has no active initiative; the coordination surface should still return a useful ready-for-bootstrap answer.
- An agent asks what is active and which task is actionable; the coordination surface should answer without reopening multiple family indexes on the first pass.
- A maintainer wants one compact human view of current planning state and recent closeouts before starting a new initiative.

## Requirements
- `req.machine_first_coordination_surface.001`: The repository must publish a derived machine-readable coordination index as the primary machine start-here planning surface.
- `req.machine_first_coordination_surface.002`: The coordination index must remain useful when no initiative is active by projecting repo-ready bootstrap state and recent closeout context.
- `req.machine_first_coordination_surface.003`: `watchtower-core query coordination` must read from the coordination index rather than inferring coordination state ad hoc.
- `req.machine_first_coordination_surface.004`: A compact human coordination byproduct must be generated from the same derived coordination state.
- `req.machine_first_coordination_surface.005`: Planning README and agent entrypoint guidance must route humans and agents to the same coordination surfaces.
- `req.machine_first_coordination_surface.006`: The repository must remain green on the current validation baseline while this surface is introduced.

## Acceptance Criteria
- `ac.machine_first_coordination_surface.001`: The planning corpus publishes the PRD, decision record, feature design, implementation plan, acceptance contract, planning evidence, bootstrap task, and bounded execution tasks for this initiative.
- `ac.machine_first_coordination_surface.002`: A governed coordination index exists and projects active work, actionable tasks, recent closeouts, and bootstrap-ready state from existing authoritative family surfaces.
- `ac.machine_first_coordination_surface.003`: `watchtower-core query coordination` and coordination-oriented sync behavior use the coordination index, and the command docs stay aligned with that change.
- `ac.machine_first_coordination_surface.004`: A compact human coordination view exists as a derived byproduct, and planning entrypoint docs plus agent guidance route to it consistently.
- `ac.machine_first_coordination_surface.005`: The repo passes `doctor`, `validate all`, `pytest`, `mypy`, and `ruff` after the work lands.

## Success Metrics
- Agents can answer the first planning-navigation question from one machine-readable artifact.
- The default machine coordination surface remains useful even when there is no active initiative.
- Humans start from one compact current-state view instead of scanning initiative and task trackers separately.

## Risks and Dependencies
- The coordination index could become a second source of truth if it carries too much family-specific detail.
- A new human byproduct could worsen entrypoint sprawl if it is not clearly positioned as the top-level coordination view.
- The surface must stay compact enough that it improves, rather than recreates, context pressure for agents.

## Open Questions
- Whether a later planning control-pack overlay should route directly through the coordination index once product work begins.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the start-here surface should remove ambiguity rather than introduce another pseudo-authority.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable and machine-readable coordination surfaces must stay derived from the same authoritative state.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): core planning control should stay generic and future-ready for product work.

## References
- [preimplementation_repo_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/preimplementation_repo_review_and_hardening.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)

## Updated At
- `2026-03-10T18:54:43Z`
