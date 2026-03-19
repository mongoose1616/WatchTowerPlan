---
trace_id: "trace.local_task_tracking"
id: "design.features.local_task_tracking_and_github_sync"
title: "Local Task Tracking and GitHub Sync Design"
summary: "Defines the feature-level design for initiative-local live task state, a generated task tracker, a generated task index, and later GitHub sync support."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-18T23:58:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "plan/initiatives/"
  - "plan/projects/"
  - "plan/.wt/indexes/task_index.json"
  - "docs/planning/tasks/task_tracking.md"
  - "core/python/src/watchtower_core/repo_ops/task_lifecycle.py"
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
- `Updated At`: `2026-03-18T23:58:00Z`

## Summary
This document defines the feature-level design for initiative-local live task state, a generated task tracker, a generated task index, and later GitHub sync support.

## Source Request
- User request for a local task tracking system that can later sync to GitHub and reduce coordination drift across multiple engineers.

## Scope and Feature Boundary
- Covers initiative-local live task state under `plan/**/.wt/tasks/**`.
- Covers the generated human tracker and generated machine-readable task index.
- Covers Python task lifecycle, query, and sync commands for the live task surfaces.
- Covers optional GitHub foreign keys and the first push-only GitHub sync path for initiative-local live task state.
- Does not implement two-way GitHub reconciliation in this slice.

## Current-State Context
- The repository already has PRD, design, decision, and traceability tracking.
- The repository now has a first-class live task family under `plan/**/.wt/tasks/**`, with derived task and initiative views.
- `docs/planning/tasks/task_tracking.md` is the derived human tracker, while retained Markdown under `docs/planning/tasks/**` is historical only.
- Planning trackers are not appropriate as the live task board because they summarize document families, not execution state.

## Foundations References Applied
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): keep machine-readable authority explicit and reviewable in git.
- [product_direction.md](/docs/foundations/product_direction.md): keep repository-native execution support local and inspectable before introducing hosted dependencies.
- [engineering_stack_direction.md](/docs/foundations/engineering_stack_direction.md): use machine-readable live task state plus generated Markdown companions for human browsing.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): keep one source of truth per concern and derive secondary lookup surfaces.

## Internal Standards and Canonical References Applied
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md): initiative-local task state and the derived tracker should stay aligned under the hard-cutover task model.
- [task_md_standard.md](/docs/standards/documentation/task_md_standard.md): retained docs-backed task Markdown remains historical only and must not be mistaken for live authority.
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md): live task metadata needs a derived machine index for lookup and later hosted sync.
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md): live tasks must carry stable `trace_id` links back to PRDs, designs, and evidence.

## Design Goals and Constraints
- Keep live task state machine-readable, reviewable in git, and safe for deterministic mutation.
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
- Add a governed initiative-local task-state family under `plan/initiatives/**/.wt/tasks/**` and `plan/projects/**/initiatives/**/.wt/tasks/**`.
- Keep one machine-readable task document per task.
- Generate `docs/planning/tasks/task_tracking.md` as the human summary board from the live task state.
- Generate `plan/.wt/indexes/task_index.json` as the machine-readable task lookup surface.
- Extend the traceability index to carry task IDs for traced initiatives.
- Reserve optional GitHub foreign keys on live task state for later sync.

### Data and Interface Impacts
- Add a live task-state schema and a task-summary index schema.
- Add task tracking, task document, and task-index standards.
- Add Python lifecycle, query, and sync commands for task lookup and rebuild.
- Extend traceability joins to include task IDs when live tasks carry a `trace_id`.

### Execution Flow
1. An engineer creates or updates one initiative-local live task under `plan/**/.wt/tasks/**`.
2. Python rebuilds the human tracker and task index from the live task state.
3. Agents or humans query the task index instead of scanning the initiative trees manually.
4. Traced tasks are joined into the traceability index through `trace_id`.
5. A later sync surface can map the same task metadata to GitHub without changing the local task identity.

### Invariants and Failure Cases
- Initiative-local task documents remain the local source of truth.
- `docs/planning/tasks/task_tracking.md` and `plan/.wt/indexes/task_index.json` remain derived surfaces.
- Task execution state stays in `task_status`.
- Artifact lifecycle `status` stays distinct from task execution state.
- Task blockers and dependencies must point to existing task IDs.

## Affected Surfaces
- `plan/initiatives/`
- `plan/projects/`
- `docs/standards/governance/task_tracking_standard.md`
- `docs/standards/documentation/task_md_standard.md`
- `docs/standards/data_contracts/task_index_standard.md`
- `plan/.wt/schemas/artifacts/task_state.schema.json`
- `plan/.wt/schemas/artifacts/task_summary_index.schema.json`
- `plan/.wt/indexes/task_index.json`
- `docs/planning/tasks/task_tracking.md`
- `core/control_plane/indexes/traceability/traceability_index.json`

## Design Guardrails
- Keep the first task metadata set small and explicit.
- Treat GitHub identifiers as optional foreign keys, not as local identities.
- Do not allow task records to turn into mini-PRDs or design documents.
- Keep query and sync commands narrow and argument-driven.

## Implementation-Planning Handoff Notes
- The first implementation should add `task create`, `task update`, `task transition`, `query tasks`, and the derived tracker or index sync paths.
- The first implementation should seed at least one initiative-local task so the family is not purely theoretical.
- GitHub API sync should be a later phase once the local task model proves stable.

## Dependencies
- Existing front-matter validation and schema-catalog loading in `core/python/`.
- Existing traceability index rebuild flow.

## Risks
- If engineers edit `docs/planning/tasks/task_tracking.md` directly instead of the live task state, drift will return quickly.
- If tasks are created without trace links when planning sources exist, coordination will remain partially disconnected.
- If GitHub sync arrives before the local model stabilizes, the sync contract will thrash.

## Open Questions
- Should later GitHub sync stay push-only from local records, or eventually support two-way reconciliation?
- Should future task queries support dependency expansion and blocker graphs, or stay simple and list-oriented?

## References
- [core_python_workspace_and_harness.md](/docs/planning/design/features/core_python_workspace_and_harness.md)
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md)
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md)
- [task_index_standard.md](/docs/standards/data_contracts/task_index_standard.md)

## Updated At
- `2026-03-18T23:58:00Z`
