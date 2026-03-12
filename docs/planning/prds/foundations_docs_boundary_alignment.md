---
trace_id: trace.foundations_docs_boundary_alignment
id: prd.foundations_docs_boundary_alignment
title: Foundations Documentation Boundary Alignment PRD
summary: Align foundations-adjacent documentation coverage, command source-surface
  attribution, and workspace standards with the current repo_ops ownership model.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T22:05:00Z'
audience: shared
authority: authoritative
---

# Foundations Documentation Boundary Alignment PRD

## Record Metadata
- `Trace ID`: `trace.foundations_docs_boundary_alignment`
- `PRD ID`: `prd.foundations_docs_boundary_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.foundations_docs_boundary_alignment_direction`
- `Linked Designs`: `design.features.foundations_docs_boundary_alignment`
- `Linked Implementation Plans`: `design.implementation.foundations_docs_boundary_alignment`
- `Updated At`: `2026-03-12T22:05:00Z`

## Summary
Align foundations-adjacent documentation coverage, command source-surface attribution, and workspace standards with the current repo_ops ownership model.

## Problem Statement
- The foundations-focused documentation review reproduced a discoverability gap in [docs/commands/core_python/README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md): the README claims to orient readers to the current durable subcommands but materially under-inventories the live query and sync corpus, including the foundations query and foundation-index sync pages.
- The current command pages for many repo-local query and sync leaf commands still cite compatibility wrappers under `watchtower_core.query` and `watchtower_core.sync` as the owning implementation surfaces, even though the current package boundary documentation says the authoritative owners now live under `watchtower_core.repo_ops.query` and `watchtower_core.repo_ops.sync`.
- The same stale ownership model remains in current authoritative standards and reference surfaces, so human guidance, command docs, and package-boundary docs no longer describe the same runtime architecture.

## Goals
- Restore foundations-adjacent command discovery so maintainers can reliably find the relevant query and sync pages without scanning the whole command-doc directory.
- Align current authoritative command docs, standards, and reference surfaces with the live `repo_ops` ownership boundary.
- Add validation coverage that fails closed if these documentation-boundary surfaces drift again.

## Non-Goals
- Redesign the runtime package layout again or remove the compatibility namespaces.
- Rewrite historical planning or closed-task artifacts whose purpose is to preserve prior state rather than act as current authority.
- Change CLI behavior, query semantics, or sync outputs beyond documentation and validation alignment.

## Requirements
- `req.foundations_docs_boundary_alignment.001`: The core Python command-doc README must expose the foundations-relevant query and sync entrypoints clearly enough to satisfy the README quick-reference contract without pretending to be an exhaustive directory dump.
- `req.foundations_docs_boundary_alignment.002`: Current authoritative query and sync command pages must point their `Source Surface` sections at the owning repo-local implementation modules rather than compatibility wrappers.
- `req.foundations_docs_boundary_alignment.003`: Current authoritative engineering, governance, and reference docs that describe query or sync ownership must match the live `repo_ops` boundary model.
- `req.foundations_docs_boundary_alignment.004`: The slice must add regression coverage that protects both the command-doc discoverability fix and the `repo_ops` ownership documentation contract.

## Acceptance Criteria
- `ac.foundations_docs_boundary_alignment.001`: [docs/commands/core_python/README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md) exposes [watchtower_core_query_foundations.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_foundations.md), [watchtower_core_sync_foundation_index.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_foundation_index.md), and the core command-group entrypoints without a misleading partial inventory.
- `ac.foundations_docs_boundary_alignment.002`: The affected query and sync command pages under [docs/commands/core_python](/home/j/WatchTowerPlan/docs/commands/core_python) cite the authoritative `repo_ops` modules in `Source Surface`.
- `ac.foundations_docs_boundary_alignment.003`: [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md), [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md), the GitHub collaboration standards, and [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md) describe the same current ownership model as [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md).
- `ac.foundations_docs_boundary_alignment.004`: Targeted regression coverage and full repository validation remain green after the documentation alignment lands.

## Risks and Dependencies
- The command-doc README fix must stay valid for the repository-path index generator, which only accepts real repository paths from README inventory tables.
- The slice depends on the current architecture boundary documented in [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md), [watchtower_core.query/README.md](/home/j/WatchTowerPlan/core/python/src/watchtower_core/query/README.md), [watchtower_core.sync/README.md](/home/j/WatchTowerPlan/core/python/src/watchtower_core/sync/README.md), and [watchtower_core.repo_ops/README.md](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/README.md) remaining authoritative.
- Broad source-surface edits across command pages create a review-surface risk if the change is not protected by a regression test that checks the current-authority contract directly.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
