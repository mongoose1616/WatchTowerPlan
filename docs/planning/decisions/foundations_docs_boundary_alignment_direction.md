---
trace_id: trace.foundations_docs_boundary_alignment
id: decision.foundations_docs_boundary_alignment_direction
title: Foundations Documentation Boundary Alignment Direction Decision
summary: Records the initial direction decision for Foundations Documentation Boundary
  Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T22:05:00Z'
audience: shared
authority: supporting
---

# Foundations Documentation Boundary Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.foundations_docs_boundary_alignment`
- `Decision ID`: `decision.foundations_docs_boundary_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.foundations_docs_boundary_alignment`
- `Linked Designs`: `design.features.foundations_docs_boundary_alignment`
- `Linked Implementation Plans`: `design.implementation.foundations_docs_boundary_alignment`
- `Updated At`: `2026-03-12T22:05:00Z`

## Summary
Records the initial direction decision for Foundations Documentation Boundary Alignment.

## Decision Statement
Update the current authoritative command docs, README navigation surface, standards, and reference docs to publish the live `repo_ops` ownership boundary consistently, while leaving compatibility namespaces in place and treating historical planning records as out of scope.

## Trigger or Source Request
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Current Context and Constraints
- The current foundations-focused review reproduced three real issues: the core Python command-doc README under-inventories the live foundations-relevant entrypoints; many command pages still cite compatibility wrappers as owning source surfaces; and several current authoritative standards or references still describe the pre-`repo_ops` package layout.
- The package-boundary READMEs and [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md) already document the intended current model, so the repair should align the stale surfaces to that published authority rather than redefining the architecture again.
- README inventory rows must continue to resolve to real repository paths so the repository-path index rebuild stays valid.

## Applied References and Implications
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the change stays inside current repository-owned documentation and governance surfaces.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the chosen path makes authority boundaries explicit instead of relying on compatibility shims as implied owners.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): command docs, standards, references, tests, and derived indexes should move together in one bounded slice.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): workspace guidance should steer contributors to the real implementation boundary for query and sync work.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): command pages must point to the implementation surface that actually owns the behavior.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): the command-doc README should stay compact and concrete rather than pretending to be an exhaustive live dump.

## Affected Surfaces
- [foundations_docs_boundary_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/foundations_docs_boundary_alignment.md)
- [foundations_docs_boundary_alignment.md](/home/j/WatchTowerPlan/docs/planning/design/features/foundations_docs_boundary_alignment.md)
- [foundations_docs_boundary_alignment.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/foundations_docs_boundary_alignment.md)
- [README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md)
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md)
- [test_control_plane_artifacts.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_control_plane_artifacts.py)

## Options Considered
### Option 1
- Fix only the foundations query and foundation-index command pages.
- Smallest possible diff.
- Rejected because the same ownership drift remains across other current authoritative query or sync command pages and standards.

### Option 2
- Align the full bounded current-authority set: the command-doc README, affected query and sync leaf pages, the active standards and reference surfaces that still encode the stale ownership model, and a regression test.
- Restores one coherent current documentation model without reopening historical records or runtime package structure.
- Chosen because it closes the reproduced drift comprehensively inside one documentation-boundary slice.

## Chosen Outcome
Apply a bounded current-authority alignment across command discovery, command source-surface attribution, and standards/reference package-boundary guidance, then lock the result in with targeted regression coverage and full validation.

## Rationale and Tradeoffs
- This path fixes the full reproduced drift without expanding the change into a new architecture refactor.
- It keeps compatibility wrappers available for imports while making current authoritative docs honest about where repo-local behavior is actually owned.
- The main tradeoff is a wider documentation diff across command pages, but that is preferable to leaving current authoritative surfaces in contradictory states.

## Consequences and Follow-Up Impacts
- The command-doc README will become a tighter anchor-based quick reference that explicitly routes foundations-related readers to the right leaf pages.
- Current command pages will cite `repo_ops` owners where those are the authoritative repo-local modules.
- Workspace, engineering, and GitHub collaboration standards will steer future work to the correct package locations.
- The post-fix validation passes will include a confirmation sweep over adjacent command, standards, and reference surfaces to catch any missed current-authority drift.

## Risks, Dependencies, and Assumptions
- Assumes the package-boundary READMEs and [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md) remain the authoritative description of the current runtime ownership model.
- Risks missing one stale command page unless regression coverage checks the family directly.
- Depends on derived path-index refresh after the README inventory changes.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
