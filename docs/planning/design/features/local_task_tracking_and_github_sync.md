---
trace_id: "trace.local_task_tracking"
id: "design.features.local_task_tracking_and_github_sync"
title: "Local Task Tracking and GitHub Sync Design"
summary: "Defines the feature-level design for local-first task records, a generated task tracker, a generated task index, and later GitHub sync support."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T18:25:06Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/tasks/"
  - "core/control_plane/indexes/tasks/task_index.v1.json"
  - "core/python/src/watchtower_core/query/"
  - "core/python/src/watchtower_core/sync/"
aliases:
  - "task tracking design"
  - "github sync design"
---

# Local Task Tracking and GitHub Sync Design

## Record Metadata
- `Trace ID`: `trace.local_task_tracking`
- `Design ID`: `design.features.local_task_tracking_and_github_sync`
- `Design Status`: `active`
- `Linked PRDs`: `None`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `2026-03-09T18:25:06Z`

## Summary
This document defines the feature-level design for local-first task records, a generated task tracker, a generated task index, and later GitHub sync support.

## Source Request
- User request for a local task tracking system that can later sync to GitHub and reduce coordination drift across multiple engineers.

## Scope and Feature Boundary
- Covers task records under `docs/planning/tasks/`.
- Covers the generated human tracker and generated machine-readable task index.
- Covers Python query and sync commands for the local task surfaces.
- Reserves optional GitHub foreign keys for later sync.
- Does not implement live GitHub API sync in this initial slice.

## Current-State Context
- The repository already has PRD, design, decision, and traceability tracking.
- The repository does not yet have a first-class task family for active execution work.
- Planning trackers are not appropriate as the live task board because they summarize document families, not execution state.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keep machine-readable authority explicit and reviewable in git.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): keep repository-native execution support local and inspectable before introducing hosted dependencies.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): use Markdown for human task records and JSON for machine-readable task lookup.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep one source of truth per concern and derive secondary lookup surfaces.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): one task per file and local-first authority should shape the tracking model.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): task documents need a stable front matter and section shape so sync and query remain deterministic.
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md): task metadata needs a derived machine index for lookup and later hosted sync.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): task records must carry stable `trace_id` links back to PRDs, designs, and evidence.
- [task_template.md](/home/j/WatchTowerPlan/docs/templates/task_template.md): task authoring should stay consistent enough to support automation and shared review.

## Design Goals and Constraints
- Keep task authoring human-readable and easy to review in git.
- Avoid one giant tracker file as the local source of truth.
- Make tasks queryable by Python and agents without parsing every Markdown file each time.
- Keep the local model compatible with later GitHub issue and project sync.
- Avoid overloading artifact lifecycle `status` with task execution state.

## Options Considered
### Option 1
- Use only one shared Markdown tracker table.
- Strengths: minimal setup and easy to browse.
- Tradeoffs or reasons not chosen: high merge-conflict risk, weak machine lookup, and poor modularity for concurrent work.

### Option 2
- Use one task record per file plus generated tracker and index.
- Strengths: low merge-conflict risk, clean human and machine surfaces, and easy future sync mapping.
- Tradeoffs or reasons not chosen: requires new standards, templates, schemas, and Python sync logic.

### Option 3
- Skip local task records and rely on GitHub Issues as the only system.
- Strengths: strong hosted collaboration tooling and native board views.
- Tradeoffs or reasons not chosen: loses local-first reviewability and makes task coordination unavailable when GitHub sync is not yet implemented.

## Recommended Design
### Architecture
- Add a governed task-document family under `docs/planning/tasks/`.
- Keep one task per file under `open/` or `closed/`.
- Generate `task_tracking.md` as the human summary board from the task files.
- Generate `task_index.v1.json` as the machine-readable task lookup surface.
- Extend the traceability index to carry task IDs for traced initiatives.
- Reserve optional GitHub foreign keys in task front matter for later sync.

### Data and Interface Impacts
- Add a task front-matter profile and a task-index artifact schema.
- Add task tracking, task document, and task-index standards.
- Add Python query and sync commands for task lookup and rebuild.
- Extend traceability joins to include task IDs when tasks carry a `trace_id`.

### Execution Flow
1. An engineer creates or updates one task record under `docs/planning/tasks/`.
2. Python rebuilds the human tracker and task index from the task records.
3. Agents or humans query the task index instead of scanning the Markdown tree manually.
4. Traced tasks are joined into the traceability index through `trace_id`.
5. A later sync surface can map the same task metadata to GitHub without changing the local task identity.

### Invariants and Failure Cases
- Task records remain the local source of truth.
- `task_tracking.md` and `task_index.v1.json` remain derived surfaces.
- Task execution state stays in `task_status`.
- Open and closed directory placement must agree with task-status class.
- Task blockers and dependencies must point to existing task IDs.

## Affected Surfaces
- `docs/planning/tasks/`
- `docs/standards/governance/task_tracking_standard.md`
- `docs/standards/documentation/task_md_standard.md`
- `docs/standards/data_contracts/task_index_standard.md`
- `docs/templates/task_template.md`
- `core/control_plane/schemas/interfaces/documentation/task_front_matter.v1.schema.json`
- `core/control_plane/schemas/artifacts/task_index.v1.schema.json`
- `core/control_plane/indexes/tasks/task_index.v1.json`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`

## Design Guardrails
- Keep the first task metadata set small and explicit.
- Treat GitHub identifiers as optional foreign keys, not as local identities.
- Do not allow task records to turn into mini-PRDs or design documents.
- Keep query and sync commands narrow and argument-driven.

## Implementation-Planning Handoff Notes
- The first implementation should add `query tasks`, `sync task-index`, and `sync task-tracking`.
- The first implementation should seed at least one open and one closed task record so the family is not purely theoretical.
- GitHub API sync should be a later phase once the local task model proves stable.

## Dependencies
- Existing front-matter validation and schema-catalog loading in `core/python/`.
- Existing traceability index rebuild flow.

## Risks
- If engineers edit `task_tracking.md` directly instead of the source task files, drift will return quickly.
- If tasks are created without trace links when planning sources exist, coordination will remain partially disconnected.
- If GitHub sync arrives before the local model stabilizes, the sync contract will thrash.

## Open Questions
- Should later GitHub sync stay push-only from local records, or eventually support two-way reconciliation?
- Should future task queries support dependency expansion and blocker graphs, or stay simple and list-oriented?

## References
- [core_python_workspace_and_harness.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_python_workspace_and_harness.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md)

## Updated At
- `2026-03-09T18:25:06Z`
