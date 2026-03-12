---
trace_id: trace.foundations_docs_boundary_alignment
id: design.features.foundations_docs_boundary_alignment
title: Foundations Documentation Boundary Alignment Feature Design
summary: Defines the technical design boundary for Foundations Documentation Boundary
  Alignment.
type: feature_design
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T22:05:00Z'
audience: shared
authority: authoritative
---

# Foundations Documentation Boundary Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.foundations_docs_boundary_alignment`
- `Design ID`: `design.features.foundations_docs_boundary_alignment`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.foundations_docs_boundary_alignment`
- `Linked Decisions`: `decision.foundations_docs_boundary_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.foundations_docs_boundary_alignment`
- `Updated At`: `2026-03-12T22:05:00Z`

## Summary
Defines the technical design boundary for Foundations Documentation Boundary Alignment.

## Source Request
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Scope and Feature Boundary
- Covers the current authoritative command docs, README navigation surface, standards, and reference docs that describe the foundations-adjacent query and sync boundaries.
- Covers regression tests that validate the current-authority documentation model.
- Does not change the runtime package topology or remove the compatibility wrapper namespaces.
- Does not rewrite historical planning records that are no longer current authority.

## Current-State Context
- [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md) classifies `watchtower_core.query` and `watchtower_core.sync` as boundary-layer compatibility namespaces and `watchtower_core.repo_ops` as the authoritative repo-local orchestration layer.
- Many current command pages under [docs/commands/core_python](/home/j/WatchTowerPlan/docs/commands/core_python) still cite `watchtower_core.query/*` or `watchtower_core.sync/*` compatibility wrappers in `Source Surface`.
- [docs/commands/core_python/README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md) under-inventories the live command-doc corpus and does not route readers to the foundations-specific query or sync pages.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md), [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md), and the GitHub collaboration docs still encode the pre-`repo_ops` ownership model for parts of the runtime surface.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the fix must stay inside `WatchTowerPlan`'s current owned documentation and governed-core surfaces rather than reopening future product scope.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the documentation fix should make authority seams more explicit and inspectable instead of leaving compatibility layers to masquerade as owners.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): current authoritative human-readable and machine-readable surfaces must agree in the same change set.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): the Python workspace guidance should reflect the real implementation boundary so maintainers do not route work to stale package locations.

## Internal Standards and Canonical References Applied
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): the command-doc README should stay compact and high-signal while still covering the important foundations-related entrypoints.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): command pages must identify the implementation surface that actually owns the command behavior.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the workspace standard must publish the current package-layout boundary correctly.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): authoritative docs must steer new repo-local query or sync work into the correct module families.
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): governance surfaces that describe GitHub sync must point at the authoritative sync owner.

## Design Goals and Constraints
- Keep the documentation changes bounded to current authoritative surfaces while fixing the whole reproduced ownership drift in one slice.
- Preserve the compatibility namespaces as compatibility namespaces; the fix is documentation alignment, not runtime extraction work.
- Keep README inventory rows on real repository paths so the repository-path index continues to rebuild deterministically.
- Add one regression seam that can catch both command-doc discovery drift and source-surface ownership drift without turning the test suite into a prose linter.

## Options Considered
### Option 1
- Patch only the foundations query page and foundations sync page.
- Smallest immediate diff.
- Rejected because the same ownership drift is reproduced across many current command docs and several authoritative standards.

### Option 2
- Update the bounded set of current authoritative command docs, README inventories, standards, and reference surfaces that still encode the stale ownership model.
- Fixes the reproduced drift systematically without reopening historical records or runtime structure.
- Chosen because it restores one coherent current-authority model across the docs that maintainers are expected to trust today.

## Recommended Design
### Architecture
- Treat [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md), package README boundaries, current command docs, current standards, and current reference docs as one documentation-authority slice.
- Align query and sync leaf command pages to the authoritative `repo_ops` owners while leaving group pages and CLI-family source surfaces unchanged when they are already correct.
- Narrow the core Python command-doc README to anchor entrypoints and foundations-relevant leaves instead of a misleading partial list of subcommands.

### Data and Interface Impacts
- README inventory edits will change the derived repository-path index after sync.
- Command-doc source-surface edits do not change the command index schema or CLI behavior, but they change current human authority about implementation ownership.
- Standards and reference updates change the documented package-layout and operationalization contract for future contributors.

### Execution Flow
1. Replace the placeholder planning records with the confirmed findings, design choice, and validation contract.
2. Update the current authoritative docs to route foundations-related navigation correctly and to point at the authoritative `repo_ops` owners.
3. Add regression coverage for the README discovery and source-surface boundary model, then rebuild and validate the affected derived surfaces.

### Invariants and Failure Cases
- The compatibility namespaces remain valid package surfaces, but current authoritative docs must not present them as the owning implementation layer for repo-local behavior.
- README inventory rows must resolve to real repository files or directories or the repository-path index rebuild will silently skip them.
- The fix must not weaken command-doc discoverability by collapsing the README into a generic pointer that omits the foundations-specific anchors again.

## Affected Surfaces
- `docs/commands/core_python/README.md`
- `docs/commands/core_python/watchtower_core_query_*.md`
- `docs/commands/core_python/watchtower_core_sync_*.md`
- `docs/standards/engineering/python_workspace_standard.md`
- `docs/standards/engineering/engineering_best_practices_standard.md`
- `docs/standards/governance/github_collaboration_standard.md`
- `docs/standards/governance/github_task_sync_standard.md`
- `docs/references/github_collaboration_reference.md`
- `core/python/tests/integration/test_control_plane_artifacts.py`

## Design Guardrails
- Do not rewrite closed planning history just to normalize old path references.
- Do not change CLI implementation paths in the command index; those remain parser-family ownership, not the human `Source Surface` for repo-local query or sync behavior.
- Do not introduce wildcard inventory rows that the repository-path index cannot materialize.

## Risks
- A broad command-doc sweep can miss one or two stale leaf pages unless the regression test checks the full affected family.
- The workspace standard update can create new drift if it fixes the package-layout table but leaves the examples or operationalization metadata on the old path model.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
