---
trace_id: "trace.foundation_scope_and_entrypoint_realignment"
id: "prd.foundation_scope_and_entrypoint_realignment"
title: "Foundation Scope and EntryPoint Realignment PRD"
summary: "Clarify current repository scope versus future WatchTower product narrative, tighten root entrypoints, and align foundation language with the export-ready core boundary."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-11T01:27:13Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/foundations/"
  - "README.md"
  - "docs/planning/README.md"
aliases:
  - "foundation scope"
  - "entrypoint realignment"
---

# Foundation Scope and EntryPoint Realignment PRD

## Record Metadata
- `Trace ID`: `trace.foundation_scope_and_entrypoint_realignment`
- `PRD ID`: `prd.foundation_scope_and_entrypoint_realignment`
- `Status`: `active`
- `Linked Decisions`: `decision.foundation_scope_boundary`
- `Linked Designs`: `design.features.foundation_scope_and_entrypoint_realignment`
- `Linked Implementation Plans`: `design.implementation.foundation_scope_and_entrypoint_realignment`
- `Updated At`: `2026-03-11T01:27:13Z`

## Summary
Clarify current repository scope versus future WatchTower product narrative, tighten root entrypoints, and align foundation language with the export-ready core boundary.

## Problem Statement
The foundation layer currently mixes two kinds of truth. Some foundation documents describe current `WatchTowerPlan` repository behavior and ownership boundaries, while others describe the future `WatchTower` product shape and customer narrative. That was workable while the repository was still mostly exploratory, but it is now a concrete coherence problem. The repo has an export-ready core boundary, real machine-readable planning and control-plane authority, and a validated maintenance workflow. At the same time, the foundation stack still allows future product language to read like current repository scope, and the root entrypoints do not explicitly route contributors through one clear repository charter. The result is avoidable ambiguity for human reviewers and agents: what this repository owns today, what belongs to future product implementation, and which root surfaces should remain thin routers versus broad explanation layers.

## Goals
- Publish one authoritative repository-scope foundation that states what `WatchTowerPlan` currently owns and what it intentionally does not own yet.
- Realign the existing foundation layer so current repository-operating truth and future product narrative no longer compete as co-equal local guidance.
- Clarify the root and nearby planning entrypoints so they route readers to current scope and coordination without turning root documents into encyclopedic overviews.
- Keep the export-ready core boundary visible in the design-principles, stack-direction, and standards-posture foundations.
- Keep the repo green while the foundation and entrypoint alignment work lands.

## Non-Goals
- Replacing the current planning model, family trackers, or traceability joins with a new planning graph in this initiative.
- Adding root-document validators or changing root-document governance behavior in this initiative.
- Starting product implementation work in `/home/j/WatchTower` or adding external pack runtime support in this initiative.
- Expanding the root README into a large repository handbook.

## Target Users or Actors
- Repository maintainers using the foundation layer to scope future work.
- Agents that need one reliable statement of current repository ownership before routing deeper.
- Product and design stakeholders who need the future WatchTower direction without confusing it with current repo scope.
- Reviewers reading the root entrypoints to orient quickly before opening deeper docs.

## Key Scenarios
- A contributor wants to know whether this repository currently owns only the reusable core and planning substrate or whether it also owns the first domain-pack implementation.
- An agent starts at the root and needs to understand which document defines current repository scope before loading product-direction or customer-narrative context.
- A maintainer updates a foundation document and needs the foundation layer to distinguish current operating rules from future product framing cleanly.

## Requirements
- `req.foundation_scope_and_entrypoint_realignment.001`: The foundation layer must publish one authoritative repository-scope document that states what `WatchTowerPlan` owns today and what remains future WatchTower product work.
- `req.foundation_scope_and_entrypoint_realignment.002`: `product_direction.md` and `customer_story.md` must clearly distinguish future product direction and narrative from current repository-operating scope.
- `req.foundation_scope_and_entrypoint_realignment.003`: `engineering_design_principles.md`, `engineering_stack_direction.md`, and `repository_standards_posture.md` must reflect the current export-ready core boundary, compactness expectations, and current runtime/tooling reality.
- `req.foundation_scope_and_entrypoint_realignment.004`: Root and adjacent planning entrypoints must stay thin and route readers to the correct scope and coordination surfaces instead of duplicating deeper narrative context.
- `req.foundation_scope_and_entrypoint_realignment.005`: The initiative must publish an acceptance baseline, keep the planning chain traceable, and preserve the current validation baseline.

## Acceptance Criteria
- `ac.foundation_scope_and_entrypoint_realignment.001`: The planning corpus publishes an active PRD, feature design, implementation plan, accepted decision, closed bootstrap task, and bounded task set for `trace.foundation_scope_and_entrypoint_realignment`.
- `ac.foundation_scope_and_entrypoint_realignment.002`: The foundations layer includes an authoritative repository-scope statement and distinguishes current repository-operating truth from future WatchTower product direction and narrative.
- `ac.foundation_scope_and_entrypoint_realignment.003`: The current-scope clarifications are reflected in `product_direction.md`, `customer_story.md`, `engineering_design_principles.md`, `engineering_stack_direction.md`, and `repository_standards_posture.md`.
- `ac.foundation_scope_and_entrypoint_realignment.004`: Root and nearby planning entrypoints stay thin and explicitly route humans and agents to current scope and coordination rather than broad root narrative.
- `ac.foundation_scope_and_entrypoint_realignment.005`: The repository remains green on the current validation baseline while the initiative lands and closes.

## Success Metrics
- Contributors can answer "what does this repository own today?" from one explicit foundation doc instead of inferring it from several documents.
- Root entrypoints stay small while still pointing readers at the correct scope and coordination surfaces.
- Future product narrative remains available without being mistaken for current repository-operating policy.

## Risks and Dependencies
- If the repository-scope statement is too weak, future product language will keep leaking into current repo behavior decisions.
- If the root entrypoint cleanup overreaches, it could create new duplication instead of reducing ambiguity.
- The initiative depends on the existing foundation layer, current root README strategy, and current planning coordination entrypoint remaining stable enough to realign in place.

## Open Questions
- Whether a later initiative should bring root Markdown into an explicit root-document validation contract after the scope and routing model is stabilized.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the repo must keep a clear boundary between reusable core, repo-specific operations, and future operator-facing product layers.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): root and foundation surfaces should stay coherent, thin where possible, and explicit about authority.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): future product structure remains important, but it should not blur the current repository boundary.

## References
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
- [README.md](/home/j/WatchTowerPlan/README.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)

## Updated At
- `2026-03-11T01:27:13Z`
