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
updated_at: "2026-03-10T16:11:26Z"
audience: "shared"
authority: "authoritative"
---

# PRD Document Standard

## Summary
This standard defines the role, structure, placement, and quality expectations for product requirements documents (PRDs) in this repository.

## Purpose
Keep PRDs reviewable, scoped, and decision-ready without forcing low-value boilerplate into small repository initiatives.

## Scope
- Applies to PRD documents stored under `docs/planning/prds/`.
- Covers placement, required structure, traceability anchors, and the quality bar for a usable PRD.
- Does not define the full execution workflow for PRD generation and does not replace implementation plans, feature designs, or ADRs.

## Use When
- Creating a new PRD.
- Refreshing an existing PRD after product, scope, or requirements changes.
- Reviewing whether a planning document is actually structured as a PRD rather than as a design doc or implementation plan.

## Related Standards and Sources
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [prd_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/prd_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [prd_generation.md](/home/j/WatchTowerPlan/workflows/modules/prd_generation.md): workflow surface that operationalizes or depends on this standard.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): companion standard that constrains this standard's default section density and compact-authoring expectations.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): foundation intent this standard must remain aligned with.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): foundation intent this standard must remain aligned with.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): foundation intent this standard must remain aligned with.
- [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md): authoring scaffold that should stay aligned with this standard.
- [README.md](/home/j/WatchTowerPlan/docs/planning/prds/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Store PRDs under `docs/planning/prds/`.
- Use governed front matter on PRDs and keep it aligned with the shared record metadata at the top of the document.
- A PRD should define product intent, scope, and validation expectations before implementation details dominate the conversation.
- A PRD should stay focused on one feature, initiative, or product change boundary.
- A PRD should make goals and non-goals explicit.
- A PRD should express requirements in a way that can later be planned, designed, and validated.
- A PRD should include acceptance criteria, and should add success metrics when they materially improve review or later validation.
- A PRD should record important risks, dependencies, assumptions, and open questions rather than burying them in prose.
- Add `Target Users or Actors` only when the affected actors are not already obvious from the problem and requirements.
- Add `Key Scenarios` only when scenarios materially reduce ambiguity.
- Add `Foundations References Applied` only when a foundation document materially changes local scope or direction. When present, each bullet should explain the implication rather than listing the path alone.
- A PRD should include a `References` section that makes internal or external source use explicit when it informed the document.
- A PRD should include a compact metadata section near the top with a shared `Trace ID`, stable `PRD ID`, lifecycle `Status`, and `Updated At` RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`.
- A body `Updated At` section is optional; front matter `updated_at` and the `Record Metadata` value remain the required machine and human anchors.
- When a PRD has durable requirements or acceptance criteria, assign stable IDs to them so downstream planning and validation work can point back explicitly.
- Update the PRD tracker and the machine-readable PRD index in the same change set when a PRD is added, renamed, removed, or materially retargeted.
- A PRD should not become a detailed implementation plan, architecture design, or task breakdown. Those belong in later companion artifacts.

## Structure or Data Model
- Title
- governed front matter
- `Record Metadata`
- `Summary`
- Problem statement
- Goals
- Non-goals
- Requirements
- Acceptance criteria
- Risks and dependencies
- `Target Users or Actors` when needed
- `Key Scenarios` when needed
- `Success Metrics` when needed
- `Open Questions` when needed
- `Foundations References Applied` when relevant
- `References`

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
- Stable `PRD ID` and `Updated At` values should be easy to find in front matter and record metadata.
- The PRD should include a `References` section, and that section should make relevant internal or external source use explicit rather than leaving it implicit in prose.
- Optional sections should be omitted when they do not add non-derivable information.
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
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)

## Notes
- A PRD is a planning authority artifact, not a complete solution design.
- If implementation structure becomes the dominant content, the material should move into a feature design or implementation plan.

## Updated At
- `2026-03-10T16:11:26Z`
