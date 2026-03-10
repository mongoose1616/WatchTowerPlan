---
id: "std.governance.coordination_tracking"
title: "Coordination Tracking Standard"
summary: "This standard defines the repository's compact human coordination tracker so humans can start from one derived current-state view without replacing family-specific planning artifacts."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "coordination_tracking"
owner: "repository_maintainer"
updated_at: "2026-03-10T21:18:00Z"
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
This standard defines the repository's compact human coordination tracker so humans can start from one derived current-state view without replacing family-specific planning artifacts.

## Purpose
- Give humans one start-here planning surface for current state, next action, and the most relevant active work.
- Keep the human coordination view derived from the machine-readable coordination index rather than becoming a second planning authority.
- Preserve the deeper family trackers as companion views instead of forcing users to guess which tracker to open first.

## Scope
- Applies to `docs/planning/coordination_tracking.md`.
- Applies to the planning-root entrypoint guidance that routes humans to the coordination tracker first.
- Covers compactness, authority boundaries, and rebuild expectations for the human coordination byproduct.
- Does not replace initiative, task, PRD, design, or decision source artifacts.

## Use When
- A contributor needs a compact current-state planning view before opening deeper planning families.
- Updating human start-here guidance for planning entrypoints.
- Reviewing whether the repo-level human coordination surface is still proportional and useful.

## Related Standards and Sources
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): defines the machine-readable coordination source that this tracker derives from.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): defines the deeper initiative-family tracker that remains available beneath this root view.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): defines the deeper task-family tracker this view links to for full execution detail.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): defines the proportional-authoring constraints this tracker should follow.
- [README.md](/home/j/WatchTowerPlan/docs/planning/README.md): planning-root entrypoint guidance that should stay aligned with this standard.

## Guidance
- Treat `docs/planning/coordination_tracking.md` as the default human start-here planning surface.
- Build the tracker from the coordination index rather than from ad hoc scans of family trackers.
- Keep the tracker compact, scan-first, and capped:
  - current-state summary
  - small active-initiative preview
  - small actionable-task preview
  - small recent-closeout preview
- Link to family-specific trackers instead of duplicating their full content.
- Keep zero-state text short and explicit.
- Do not hand-edit `coordination_tracking.md` as an authored planning record.
- Keep the tracker smaller than the combined trackers it summarizes.
- Keep the tracker `_Updated At` value aligned with the latest effective initiative state change, including terminal closeout.

## Structure or Data Model
### Source-of-truth layers
| Layer | Role |
|---|---|
| Coordination index | Authoritative machine-readable coordination source |
| `coordination_tracking.md` | Derived human-readable current-state tracker |
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
4. Keep planning README and nearby agent or command entrypoint guidance aligned when the start-here experience changes.

## Validation
- `coordination_tracking.md` should be regenerated, not hand-authored.
- The tracker should link to repo-local surfaces for deeper detail.
- The tracker should stay compact and should not grow into a second full tracker family.
- The tracker should remain useful even when no initiative is active.
- The tracker `_Updated At` value should not trail a later initiative closeout timestamp.

## Change Control
- Update this standard when the repository changes the human planning start-here experience or the compact coordination tracker structure.
- Update the coordination sync logic, planning README entrypoint guidance, and coordination-index companion standards in the same change set when this tracker changes structurally.

## References
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md)
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/README.md)

## Updated At
- `2026-03-10T21:18:00Z`
