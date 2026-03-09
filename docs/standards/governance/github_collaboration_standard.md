---
id: "std.governance.github_collaboration"
title: "GitHub Collaboration Standard"
summary: "This standard defines how GitHub issue forms, pull requests, labels, and project fields complement the repo-local planning and task model."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "github"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - ".github/"
  - "docs/planning/tasks/"
  - "core/python/src/watchtower_core/sync/github_tasks.py"
aliases:
  - "github collaboration"
  - "github project field model"
---

# GitHub Collaboration Standard

## Summary
This standard defines how GitHub issue forms, pull requests, labels, and project fields complement the repo-local planning and task model.

## Purpose
- Provide a hosted collaboration layer for multiple engineers without making GitHub the primary source of truth.
- Standardize issue intake, pull request review expectations, and the expected GitHub Project field model.
- Keep the repo-local planning and task artifacts authoritative while still supporting GitHub-native execution visibility.

## Scope
- Applies to `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`, and the GitHub collaboration rules referenced by task sync.
- Applies to the human process for issue intake and pull request closeout on GitHub.
- Applies to the expected GitHub Project v2 custom-field model when a team uses GitHub Projects with this repository.
- Does not make GitHub the authoritative task, planning, or traceability surface.

## Use When
- Standing up the repository for multi-engineer collaboration on GitHub.
- Reviewing whether a GitHub issue or pull request is missing required local planning or task linkage.
- Configuring a GitHub Project for this repository.

## Related Standards and Sources
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md): local reference surface for the external or canonical guidance this standard depends on.
## Guidance
- Treat GitHub issues as hosted intake or hosted execution mirrors, not as the sole authoritative task record.
- Keep repo-local PRDs, decisions, designs, tasks, contracts, evidence, and traceability surfaces authoritative.
- Use GitHub issue forms for structured intake only.
- Before merge, accepted GitHub work should link or create the corresponding repo-local planning or task artifact.
- Every pull request should publish:
  - the primary `trace_id`
  - the local task ID or IDs when task tracking applies
  - the validation commands or checks actually run
  - whether human and machine companion surfaces were updated
- Use the managed GitHub labels created by `watchtower-core sync github-tasks` for mirrored execution metadata:
  - `source:watchtower`
  - `kind:<task_kind>`
  - `status:<task_status>`
  - `priority:<priority>`
  - `blocked` when the task currently declares blockers

## Structure or Data Model
### GitHub role boundaries
| Surface | Role |
|---|---|
| GitHub issue forms | Hosted intake |
| GitHub issues | Hosted execution mirror or discussion surface |
| GitHub pull requests | Hosted code-review and merge surface |
| GitHub Project | Hosted portfolio or board view |
| Repo-local planning and task docs | Authoritative durable planning and execution source |

### Recommended GitHub Project fields
| Field | Type | Notes |
|---|---|---|
| `Status` | Single select | Use `Backlog`, `Ready`, `In Progress`, `Blocked`, `In Review`, `Done`, `Cancelled`. |
| `Priority` | Single select | Use `Critical`, `High`, `Medium`, `Low` if the team needs a hosted priority view. |
| `Owner` | Text or assignee mirror | Mirrors the repo-local task owner when helpful. |
| `Trace ID` | Text | Stable trace link back to the planning corpus. |
| `Area` | Single select or text | Optional high-level repo area such as `core/python` or `docs/planning`. |
| `Size` | Single select | Optional team-specific sizing field. |
| `Iteration` | Iteration | Optional cadence field when the team uses GitHub iterations. |

## Process or Workflow
1. Capture hosted intake through an issue form when the work does not yet have a repo-local artifact.
2. Triage the issue and decide whether to link or create a repo-local PRD, design, or task record.
3. Use pull requests to reference the relevant `trace_id`, local task IDs, and validation results.
4. If GitHub task sync is in use, let the repo-local task record push the mirrored issue and project metadata outward.
5. Keep repo-local status and GitHub-hosted state aligned instead of letting them drift independently.

## Validation
- GitHub issue forms should ask for enough information to create or link the corresponding repo-local artifact.
- Pull requests should not merge without a clear `trace_id` and a summarized validation record when the change is non-trivial.
- Hosted GitHub labels should remain bounded and deterministic rather than turning into free-form taxonomy sprawl.
- GitHub Project fields should not redefine the task status vocabulary differently from the repo-local task model.

## Change Control
- Update this standard when the repository changes how GitHub intake, pull request review, or project field mapping works.
- Update `.github/`, `github_task_sync_standard.md`, and the GitHub sync command docs in the same change set when the collaboration contract changes materially.

## References
- [github_task_sync_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/github_task_sync_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [github_collaboration_reference.md](/home/j/WatchTowerPlan/docs/references/github_collaboration_reference.md)
- [README.md](/home/j/WatchTowerPlan/.github/README.md)

## Updated At
- `2026-03-09T23:02:08Z`
