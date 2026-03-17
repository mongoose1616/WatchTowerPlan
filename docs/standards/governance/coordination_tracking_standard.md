---
id: "std.governance.coordination_tracking"
title: "Coordination Tracking Standard"
summary: "This standard defines the repository's compact docs-backed coordination tracker so humans can browse the traced planning corpus without replacing the live `plan/**` authority surfaces."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "coordination_tracking"
owner: "repository_maintainer"
updated_at: "2026-03-17T06:08:09Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/coordination_tracking.md"
  - "docs/planning/README.md"
aliases:
  - "coordination tracker"
  - "planning start-here"
  - "human coordination view"
---

# Coordination Tracking Standard

## Summary
This standard defines the repository's compact docs-backed coordination tracker so humans can browse the traced planning corpus without replacing the live `plan/**` authority surfaces.

## Purpose
- Give humans one compact docs-backed planning surface for traced current state, next follow-up work, and retained backlog context after the live `plan/**` entrypoints route them into the planning corpus.
- Keep the human coordination view derived from the machine-readable coordination index rather than becoming a second planning authority.
- Preserve the deeper family trackers as companion views instead of forcing users to guess which tracker to open first.

## Scope
- Applies to `docs/planning/coordination_tracking.md`.
- Applies to the planning-root entrypoint guidance that routes humans to the coordination tracker for traced-planning corpus questions.
- Covers compactness, authority boundaries, and rebuild expectations for the human coordination byproduct.
- Does not replace initiative, task, PRD, design, or decision source artifacts.

## Use When
- A contributor needs a compact traced-planning view after the live `plan/**` surfaces point them to the docs-backed planning corpus.
- Updating human start-here guidance for planning entrypoints.
- Reviewing whether the repo-level human coordination surface is still proportional and useful.

## Related Standards and Sources
- [coordination_index_standard.md](/docs/standards/data_contracts/coordination_index_standard.md): defines the machine-readable coordination source that this tracker derives from.
- [initiative_tracking_standard.md](/docs/standards/governance/initiative_tracking_standard.md): defines the deeper initiative-family tracker that remains available beneath this root view.
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md): defines the deeper task-family tracker this view links to for full execution detail.
- [compact_document_authoring_standard.md](/docs/standards/documentation/compact_document_authoring_standard.md): defines the proportional-authoring constraints this tracker should follow.
- [README.md](/docs/planning/README.md): planning-root entrypoint guidance that should stay aligned with this standard.

## Guidance
- Treat `docs/planning/coordination_tracking.md` as the start-here surface for the retained docs-backed planning corpus, not as the live plan-workspace start-here surface.
- Route live plan-workspace state to `plan/plan_overview.md` and `plan/.wt/indexes/coordination_index.json`.
- Build the tracker from the coordination index rather than from ad hoc scans of family trackers.
- Treat the coordination tracker as the human start-here companion to the coordination index, not as the canonical deep-planning answer for one trace.
- Keep the tracker compact, scan-first, and capped:
  - current-state summary
  - small active-initiative preview
  - small actionable-task preview
  - small recent-closeout preview
- Link to family-specific trackers instead of duplicating their full content.
- Treat the `Active Initiatives` section as an active-only preview and route broader historical browsing to the initiative-family tracker or machine initiative query.
- Keep zero-state text short and explicit.
- Do not hand-edit `coordination_tracking.md` as an authored planning record.
- Keep the tracker smaller than the combined trackers it summarizes.
- Keep the tracker `_Updated At` value aligned with the latest effective initiative state change, including terminal closeout.
- Use the authority map when a contributor needs to confirm whether coordination or a deeper planning surface is canonical for the question at hand.

## Structure or Data Model
### Source-of-truth layers
| Layer | Role |
|---|---|
| `plan/.wt/indexes/coordination_index.json` and `plan/plan_overview.md` | Live plan-workspace start-here surfaces |
| Coordination index | Authoritative machine-readable docs-backed coordination source |
| `coordination_tracking.md` | Derived human-readable traced-planning tracker |
| Family trackers | Deeper human companion views for initiatives, tasks, PRDs, designs, and decisions |

### Required tracker sections
| Section | Requirement |
|---|---|
| `## Current State` | Required |
| `## Active Initiatives` | Required |
| `## Actionable Tasks` | Required |
| `## Recent Closeouts` | Required |

## Process or Workflow
1. Update the source planning artifacts, task records, or closeout state.
2. Rebuild the task, traceability, initiative, and coordination indexes in dependency order.
3. Rebuild `coordination_tracking.md` from the coordination index in the same change set.
4. Keep planning README and nearby agent or command entrypoint guidance aligned when the live-versus-traced start-here split changes.

## Operationalization
- `Modes`: `documentation`
- `Operational Surfaces`: `docs/planning/README.md`; `docs/planning/coordination_tracking.md`; `plan/plan_overview.md`

## Validation
- `coordination_tracking.md` should be regenerated, not hand-authored.
- The tracker should link to repo-local surfaces for deeper detail.
- The tracker should stay compact and should not grow into a second full tracker family.
- The `Active Initiatives` section should remain an active-only current-state preview while `Recent Closeouts` stays compact context.
- The tracker should remain useful even when no initiative is active.
- The tracker `_Updated At` value should not trail a later initiative closeout timestamp.

## Change Control
- Update this standard when the repository changes the docs-backed planning start-here experience or the compact coordination tracker structure.
- Update the coordination sync logic, planning README entrypoint guidance, and coordination-index companion standards in the same change set when this tracker changes structurally.

## References
- [coordination_index_standard.md](/docs/standards/data_contracts/coordination_index_standard.md)
- [initiative_tracking_standard.md](/docs/standards/governance/initiative_tracking_standard.md)
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md)
- [README.md](/docs/planning/README.md)

## Updated At
- `2026-03-17T06:08:09Z`
