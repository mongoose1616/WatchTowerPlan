---
id: "ref.github_collaboration"
title: "GitHub Collaboration Reference"
summary: "This document provides a working reference for the GitHub collaboration surfaces that this repository uses for issue intake, pull request templates, project fields, issue sync, and hosted execution visibility."
type: "reference"
status: "active"
tags:
  - "reference"
  - "github"
  - "collaboration"
owner: "repository_maintainer"
updated_at: "2026-03-12T22:05:00Z"
audience: "shared"
authority: "reference"
applies_to:
  - ".github/"
  - "docs/standards/governance/github_collaboration_standard.md"
  - "docs/standards/governance/github_task_sync_standard.md"
  - "core/python/src/watchtower_core/repo_ops/sync/github_tasks.py"
aliases:
  - "github collaboration"
  - "github issue forms"
  - "github pull request template"
  - "github projects fields"
---

# GitHub Collaboration Reference

## Summary
This document provides a working reference for the GitHub collaboration surfaces that this repository uses for issue intake, pull request templates, project fields, issue sync, and hosted execution visibility.

## Purpose
Provide one repo-native lookup surface for the GitHub capabilities that materially shape this repository's hosted collaboration layer.

## Scope
- Covers issue templates and forms, pull request templates, GitHub Projects custom fields, issue sync, and the API surfaces currently used by local task push sync.
- Does not turn GitHub into the authoritative planning or task source for this repository.

## Canonical Upstream
- `https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository` - verified 2026-03-09; issue forms and issue templates.
- `https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository` - verified 2026-03-09; pull request templates.
- `https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-custom-fields` - verified 2026-03-09; GitHub Projects custom fields.
- `https://docs.github.com/en/rest/issues/issues` - verified 2026-03-09; GitHub Issues REST API.
- `https://docs.github.com/en/graphql/guides/using-the-api-to-manage-projects` - verified 2026-03-09; GitHub Projects GraphQL API guidance.

## Related Standards and Sources
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)
- [github_collaboration_scaffolding.md](/home/j/WatchTowerPlan/docs/planning/design/features/github_collaboration_scaffolding.md)
- [github_task_push_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/github_task_push_sync.md)

## Quick Reference or Distilled Reference
### Hosted Surface Roles
| Surface | Use Here | Notes |
|---|---|---|
| Issue forms | Structured hosted intake | Keep intake bounded and route back to repo-local planning or tasks. |
| Pull request template | Hosted review checklist | Publish `trace_id`, task links, validation, and companion-surface updates. |
| GitHub Project fields | Hosted board view | Mirror local task state without replacing it. |
| Issues REST API | Issue create and update path | Good fit for push-only task sync and managed labels. |
| Projects GraphQL API | Project item and field updates | Needed when task sync also manages project placement or status. |

### Core Rules
- Keep repo-local planning docs, task records, and machine indexes authoritative.
- Use GitHub for hosted intake, discussion, review, and mirrored execution visibility.
- Keep the hosted status vocabulary aligned with local task status values rather than inventing a second incompatible board model.
- Treat issue numbers, node IDs, and project item IDs as foreign keys, not as local durable identities.

### Common Decision Points
| Question | Preferred Answer | Why |
|---|---|---|
| Where should task truth live? | In repo-local task records | Git-reviewed local state is inspectable and deterministic. |
| Should GitHub forms replace local planning docs? | No | Forms are intake, not durable planning authority. |
| Which API family should issue sync use? | REST for issues, GraphQL for projects | Matches GitHub's current API split and keeps each concern narrow. |

### Failure Modes and Pitfalls
- Letting GitHub issue edits silently override repo-local task metadata creates authority drift quickly.
- Treating GitHub Projects as the only task board breaks the local-first planning model and hides durable history outside git.
- Allowing unmanaged labels or free-form project statuses creates coordination drift between human and machine surfaces.

## Local Mapping in This Repository
### Current Repository Status
- Active support for current repository standards, design docs, `.github/` collaboration scaffolding, and push-only GitHub task sync.

### Current Touchpoints
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [README.md](/home/j/WatchTowerPlan/.github/README.md)
- [github_collaboration_scaffolding.md](/home/j/WatchTowerPlan/docs/planning/design/features/github_collaboration_scaffolding.md)
- [github_task_push_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/github_task_push_sync.md)
- `core/python/src/watchtower_core/repo_ops/sync/github_tasks.py`

### Why It Matters Here
- This reference is the repo-native lookup surface for GitHub collaboration assumptions that materially shape local standards and designs.
- Standards should cite this document when they depend on GitHub capabilities instead of duplicating the same raw external URLs repeatedly.

## References
- [github_collaboration_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_collaboration_standard.md)
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [github_collaboration_scaffolding.md](/home/j/WatchTowerPlan/docs/planning/design/features/github_collaboration_scaffolding.md)
- [github_task_push_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/github_task_push_sync.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` while normalizing GitHub-facing repository guidance through local references.

## Updated At
- `2026-03-12T22:05:00Z`
