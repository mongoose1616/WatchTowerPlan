---
trace_id: "trace.github_collaboration"
id: "design.features.github_collaboration_scaffolding"
title: "GitHub Collaboration Scaffolding"
summary: "Defines the hosted GitHub intake, pull request, and project-field scaffolding that complements the repo-local planning and task model."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T00:13:52Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - ".github/"
  - "docs/planning/tasks/"
  - "core/python/src/watchtower_core/sync/github_tasks.py"
aliases:
  - "github collaboration scaffolding"
  - "github repository collaboration"
---

# GitHub Collaboration Scaffolding

## Record Metadata
- `Trace ID`: `trace.github_collaboration`
- `Design ID`: `design.features.github_collaboration_scaffolding`
- `Design Status`: `active`
- `Linked PRDs`: `None`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `2026-03-10T00:13:52Z`

## Summary
This document defines the hosted GitHub intake, pull request, and project-field scaffolding that complements the repo-local planning and task model.

## Source Request
- User request to make the repository workable for multiple engineers while preserving repo-local task and planning authority.

## Scope and Feature Boundary
- Covers GitHub issue forms for hosted intake, a pull request template for traceability and validation discipline, and the recommended GitHub Project field model.
- Covers how this hosted collaboration layer aligns with local-first task tracking and push-only GitHub issue sync.
- Does not make GitHub the primary planning or task source of truth.
- Does not implement two-way GitHub reconciliation.

## Current-State Context
- The repo now has a local-first task system, push-only GitHub task sync, and initiative closeout.
- There is still no GitHub-native scaffolding for intake or PR review.
- Multiple engineers need a predictable hosted layer for intake and review even when the authoritative planning state stays in git.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): preserve deterministic, inspectable authority boundaries rather than hiding planning state in an external tool.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): support maintainers and automated workflows with reusable structured surfaces.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep human-facing and machine-facing collaboration surfaces aligned in the same change set when they depend on each other.

## Internal Standards and Canonical References Applied
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md): GitHub should remain a hosted collaboration layer that complements repo-local authority instead of replacing it.
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): issue labels, mirrored status, and project fields need to stay aligned with the sync contract.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): hosted intake and PR review still need clear links back to local task records.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): `.github/`, sync code, and companion docs should be updated together.
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md): use the repo-native GitHub reference as the shared local summary of the hosted collaboration surfaces and APIs.

## External Sources Consulted
- [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository): shaped the issue-form structure and bounded intake expectations.
- [Creating a pull request template for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository): shaped the hosted pull-request checklist boundary.
- [About custom fields for issues and pull requests](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-custom-fields): shaped the bounded GitHub Project field model.

## Design Goals and Constraints
- Keep GitHub useful for humans without letting it silently outrank repo-local task and planning surfaces.
- Make intake and PR review consistent enough that engineers do not invent their own ad hoc issue or PR formats.
- Keep GitHub Project configuration bounded and aligned with the repo-local status vocabulary.

## Options Considered
### Option 1: Minimal hosted scaffolding plus repo-local authority
- Add issue forms, a PR template, and a bounded Project field model while keeping PRDs, designs, tasks, and traceability authoritative in the repo.
- Preserves the repo's deterministic planning and control-plane model.
- Requires engineers to learn the boundary between intake and authoritative planning surfaces.

### Option 2: Treat GitHub Issues and Projects as the primary planning system
- Would centralize more human workflow in the hosted tool and reduce repo-local planning friction for casual contributors.
- Simplifies hosted visibility for teams already operating in GitHub every day.
- Was not chosen because it would hide authoritative planning state outside git and weaken the repo's local-first traceability model.

## Recommended Design
### Architecture
- Add `.github/ISSUE_TEMPLATE/` for structured intake.
- Add `.github/pull_request_template.md` for traceability, validation, and governed-surface review.
- Keep issue forms focused on intake and routing, not on authoritative task status.
- Let `watchtower-core sync github-tasks` mirror repo-local task metadata, labels, and issue body structure outward when local tasks are ready for hosted visibility.

### Data and Interface Impacts
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/governance_chore.yml`
- `.github/pull_request_template.md`
- A small bounded label set created or reused by GitHub task sync

### Execution Flow
1. A human opens a GitHub issue through a structured issue form.
2. Triage determines whether a repo-local PRD, design, or task record already exists or must be created.
3. Active work happens against the repo-local artifact, with optional GitHub sync for hosted visibility.
4. Pull requests use the standard template to publish the `trace_id`, local task IDs, validation record, and governed-surface updates.
5. If the work is mirrored to GitHub issues or a project, the synced issue labels and project status stay bounded and deterministic.

## Affected Surfaces
- `.github/`
- `docs/planning/tasks/`
- `core/python/src/watchtower_core/sync/github_tasks.py`
- `docs/commands/core_python/watchtower_core_sync_github_tasks.md`

## Design Guardrails
- Do not treat issue forms as a substitute for repo-local PRDs, designs, or tasks.
- Do not let GitHub Project status invent a second incompatible task status vocabulary.
- Keep the GitHub label set small, deterministic, and managed.

## Implementation-Planning Handoff Notes
- Add the `.github/` scaffolding in the same change set as the sync command, standards, and command-doc updates that describe how engineers should use it.
- Keep GitHub status, labels, and trace/task links aligned with the local task and sync contracts instead of introducing GitHub-only semantics.

## Dependencies
- GitHub repository permissions must allow issue templates, pull-request templates, labels, and Projects configuration.
- The local task model and `watchtower-core sync github-tasks` contract must remain stable enough to mirror outward without manual translation.

## Risks
- Engineers may over-trust hosted issue or Project state unless the local-first boundary is made explicit in docs and command help.
- GitHub field or label drift can create confusing mismatches between hosted visibility and repo-local task state if sync assumptions change without companion updates.

## References
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md)
- [README.md](/home/j/WatchTowerPlan/.github/README.md)
- [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [Creating a pull request template for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [About custom fields for issues and pull requests](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-custom-fields)

## Updated At
- `2026-03-10T00:13:52Z`
