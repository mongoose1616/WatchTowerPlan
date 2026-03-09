---
id: "std.documentation.prd_md"
title: "PRD Document Standard"
summary: "This standard defines the role, structure, placement, and quality expectations for product requirements documents (PRDs) in this repository."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "prd_md"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:23:35Z"
audience: "shared"
authority: "authoritative"
---

# PRD Document Standard

## Summary
This standard defines the role, structure, placement, and quality expectations for product requirements documents (PRDs) in this repository.

## Purpose
Keep PRDs reviewable, scoped, and decision-ready so product intent is clear before implementation planning or code changes begin.

## Scope
- Applies to PRD documents stored under `docs/planning/prds/`.
- Covers placement, required structure, traceability anchors, and the quality bar for a usable PRD.
- Does not define the full execution workflow for PRD generation and does not replace implementation plans, feature designs, or ADRs.

## Use When
- Creating a new PRD.
- Refreshing an existing PRD after product, scope, or requirements changes.
- Reviewing whether a planning document is actually structured as a PRD rather than as a design doc or implementation plan.

## Related Standards and Sources
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [prd_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/prd_index_standard.md)
- [prd_generation.md](/home/j/WatchTowerPlan/workflows/modules/prd_generation.md)
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md)
- [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/prds/README.md)

## Guidance
- Store PRDs under `docs/planning/prds/`.
- A PRD should define product intent, scope, and validation expectations before implementation details dominate the conversation.
- A PRD should stay focused on one feature, initiative, or product change boundary.
- A PRD should make goals and non-goals explicit.
- A PRD should identify the target users, operators, or stakeholders affected by the change.
- A PRD should describe the key user scenarios or flows the change must support.
- A PRD should express requirements in a way that can later be planned, designed, and validated.
- A PRD should include acceptance criteria and success metrics when those can be made concrete.
- A PRD should record important risks, dependencies, assumptions, and open questions rather than burying them in prose.
- A PRD should reference the applicable foundation documents when those documents materially shape the product direction or scope.
- A PRD should include a compact metadata section near the top with a shared `Trace ID`, stable `PRD ID`, lifecycle `Status`, and `Updated At` RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`.
- When a PRD has durable requirements or acceptance criteria, assign stable IDs to them so downstream planning and validation work can point back explicitly.
- Update the PRD tracker and the machine-readable PRD index in the same change set when a PRD is added, renamed, removed, or materially retargeted.
- A PRD should not become a detailed implementation plan, architecture design, or task breakdown. Those belong in later companion artifacts.

## Structure or Data Model
- Title
- `Record Metadata`
- `Summary`
- Problem statement
- Goals
- Non-goals
- Target users or actors
- Key scenarios or user stories
- Requirements
- Acceptance criteria
- Success metrics
- Risks and dependencies
- Open questions
- Foundations references applied when relevant

### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| PRD | `docs/planning/prds/<prd_name>.md` | Use stable snake_case filenames derived from the PRD topic. |
| PRD tracker | `docs/planning/prds/prd_tracking.md` | Human-readable tracker for the current PRD corpus. |
| PRD directory README | `docs/planning/prds/README.md` | Directory orientation and inventory only. |

## Validation
- The PRD should make the problem, scope, and intended outcomes understandable without verbal backfill.
- The PRD should distinguish product requirements from implementation choices.
- The PRD should include enough structure that later design and implementation planning can trace back to it.
- Requirements and acceptance criteria should be concrete enough to test or review later.
- Stable `PRD ID` and `Updated At` values should be easy to find.
- When requirement or acceptance IDs are used, they should be stable and unique within the PRD.
- The PRD should not sprawl across multiple unrelated initiatives.

## Change Control
- Update this standard when the repository changes how PRDs are structured or reviewed.
- Update the PRD-generation workflow, the PRD template, and the PRD index surfaces in the same change set when structural expectations change.
- Update affected feature designs, implementation plans, or companion docs in the same change set when a PRD change materially alters scope or product intent.

## References
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [prd_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/prd_index_standard.md)
- [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md)
- [prd_generation.md](/home/j/WatchTowerPlan/workflows/modules/prd_generation.md)
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)

## Notes
- A PRD is a planning authority artifact, not a complete solution design.
- If implementation structure becomes the dominant content, the material should move into a feature design or implementation plan.

## Updated At
- `2026-03-09T05:23:35Z`
