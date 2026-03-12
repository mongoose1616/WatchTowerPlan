---
trace_id: trace.foundations_docs_boundary_alignment
id: design.implementation.foundations_docs_boundary_alignment
title: Foundations Documentation Boundary Alignment Implementation Plan
summary: Breaks Foundations Documentation Boundary Alignment into a bounded implementation
  slice.
type: implementation_plan
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T22:05:00Z'
audience: shared
authority: supporting
---

# Foundations Documentation Boundary Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.foundations_docs_boundary_alignment`
- `Plan ID`: `design.implementation.foundations_docs_boundary_alignment`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.foundations_docs_boundary_alignment`
- `Linked Decisions`: `decision.foundations_docs_boundary_alignment_direction`
- `Source Designs`: `design.features.foundations_docs_boundary_alignment`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-12T22:05:00Z`

## Summary
Breaks Foundations Documentation Boundary Alignment into a bounded implementation slice.

## Source Request or Design
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Scope Summary
- Covers the current authoritative docs and tests needed to align foundations-adjacent command discovery and repo-local query or sync ownership guidance.
- Excludes runtime code refactors, CLI behavior changes, and historical planning-doc cleanup outside the current-authority set.

## Assumptions and Constraints
- Preserve the current runtime boundary: `watchtower_core.query` and `watchtower_core.sync` stay compatibility wrappers while `watchtower_core.repo_ops` remains the current authoritative repo-local implementation layer.
- Keep README inventory rows on existing concrete paths so the repository-path index rebuild continues to project them.
- Treat newly revealed drift from targeted or full validation as in-scope if it belongs to the same documentation-boundary theme.

## Internal Standards and Canonical References Applied
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): the command-doc README should stay compact while still covering the important entrypoints.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): command pages must publish the owning implementation surface clearly.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): workspace package-boundary guidance must match the live runtime layout.
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): GitHub sync docs must point to the authoritative repo-local sync owner.

## Proposed Technical Approach
- Update the slice planning docs and acceptance contract first so the governed closeout record matches the confirmed review findings.
- Repair the command-doc discovery layer by tightening the core Python README to anchor pages and foundations-specific leaves that use concrete repository paths.
- Sweep the affected query and sync command pages to replace compatibility-wrapper `Source Surface` references with the corresponding `repo_ops` owners.
- Align the workspace, engineering, governance, and reference docs that still publish the stale ownership model.
- Add regression tests that assert the README anchors and the current-authority source-surface contract directly.

## Work Breakdown
1. Update the PRD, design, implementation plan, direction decision, and acceptance contract to capture the confirmed findings and the chosen bounded remediation approach.
2. Edit the command-doc README, query and sync leaf pages, standards, and reference docs to align them with the live `repo_ops` boundary and foundations-relevant navigation needs.
3. Add regression coverage, run targeted checks, run the full validation suite, and close any same-theme issue surfaced by those checks before closeout.

## Risks
- The README fix can regress repository-path indexing if a new inventory row does not resolve to a real path.
- A broad command-doc sweep is prone to one stale file being missed unless the test coverage checks the affected family directly.

## Validation Plan
- Run targeted regression coverage for the documentation and command-doc artifacts.
- Run `watchtower-core sync all --write --format json` so the repository-path index and other affected derived surfaces refresh in the same slice.
- Run full repository validation, `pytest -q`, `python -m mypy src/watchtower_core`, and `ruff check .`.
- Finish with repeated documentation-boundary confirmation passes over the touched command docs, standards, reference docs, and adjacent package-boundary READMEs.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
