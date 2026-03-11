---
id: "std.documentation.feature_design_md"
title: "Feature Design Document Standard"
summary: "This standard defines the structure, placement, and boundary rules for feature-level technical design documents stored under `docs/planning/design/features/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "feature_design_md"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
---

# Feature Design Document Standard

## Summary
This standard defines the structure, placement, and boundary rules for feature-level technical design documents stored under `docs/planning/design/features/`.

## Purpose
Keep feature designs consistent enough to review, compare, and hand off into implementation planning without turning them into PRDs, workflow modules, or commit-level plans.

## Scope
- Applies to feature design documents stored under `docs/planning/design/features/`.
- Covers placement, required sections, optional sections, and the relationship between feature designs and later implementation plans.
- Does not define PRD shape, workflow procedure, or implementation-plan breakdown format.

## Use When
- Creating a new technical design for a repository feature or capability.
- Reviewing whether a proposed design is specific enough for implementation planning.
- Refreshing a feature design after standards, control-plane artifacts, or architecture decisions change materially.

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): companion standard that constrains this standard's default section density and compact-authoring expectations.
- [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md): authoring scaffold that should stay aligned with this standard.
- [README.md](/home/j/WatchTowerPlan/docs/planning/design/features/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Store feature designs under `docs/planning/design/features/`.
- Keep one primary feature or tightly related capability cluster per design.
- Use governed front matter on feature-design documents and validate it against the published feature-design front matter profile.
- Use feature designs to explain why a solution should be built a certain way before work is broken into implementation tasks.
- Feature designs should identify current-state constraints, options considered, the recommended design, and the implementation guardrails that later work must preserve.
- Do not use feature designs as workflow modules, changelogs, or commit-by-commit execution notes.
- Do not move normative repository rules into a feature design when they belong in `docs/standards/**`.
- When an external topic already has a governed local reference under `docs/references/**`, cite that local reference as the repo-native lookup surface instead of scattering raw external URLs through the design body.
- Include only the external sources that materially shaped the design. Omit that section when none were needed.
- `Foundations References Applied` and `Internal Standards and Canonical References Applied` are optional, but when present they must explain the local implication of each cited source. Bare link lists are insufficient.
- `Implementation-Planning Handoff Notes`, `Dependencies`, and `Open Questions` are optional and should be omitted when they add no new information.
- A body `Updated At` section is optional; front matter `updated_at` and the `Record Metadata` value remain the required anchors.

## Structure or Data Model
### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Feature design | `docs/planning/design/features/<feature_name>.md` | Use stable snake_case filenames derived from the design topic. |
| Feature-design directory README | `docs/planning/design/features/README.md` | Directory orientation and inventory only. |

### Required sections for feature designs
| Section | Requirement | Notes |
|---|---|---|
| `Record Metadata` | Required | Record the `trace_id`, design `id`, lifecycle status, linked planning surfaces, and the same `updated_at` value carried in front matter. |
| `Summary` | Required | One short explanation of the design and intended outcome. |
| `Source Request` | Required | Record the request, issue, or planning input that triggered the design. |
| `Scope and Feature Boundary` | Required | Define what the design covers and excludes. |
| `Current-State Context` | Required | Describe current repository surfaces, constraints, or gaps that matter. |
| `Design Goals and Constraints` | Required | State the main goals, non-goals, and invariants. |
| `Options Considered` | Required | Compare at least two meaningful approaches when tradeoffs exist. |
| `Recommended Design` | Required | Describe the chosen architecture, flow, and failure behavior. |
| `Affected Surfaces` | Required | List the repo surfaces likely to change. |
| `Design Guardrails` | Required | Call out rules implementation planning must preserve. |
| `Risks` | Required | Record concrete risks or uncertainties. |
| `References` | Required | Link companion docs or artifacts. |

### Optional sections for feature designs
| Section | Use When |
|---|---|
| `Foundations References Applied` | A foundations document materially changes the local design direction. Each bullet should record `source: implication`. |
| `Internal Standards and Canonical References Applied` | An internal standard, schema, registry, or canonical repo surface materially constrains the design. Each bullet should record `source: implication`. |
| `External Sources Consulted` | An external primary source materially shaped the design. Each bullet should record what the source clarified, constrained, or justified. |
| `Implementation-Planning Handoff Notes` | The implementation plan needs explicit follow-up notes beyond what the design already makes obvious. |
| `Dependencies` | Real dependencies materially affect sequencing or feasibility. |
| `Open Questions` | Real design questions remain unresolved. |

## Process or Workflow
1. Place the design under `docs/planning/design/features/` with a stable snake_case filename.
2. Add governed front matter using the feature-design profile before the Markdown body.
3. Draft the document using the feature design template and required section order.
4. Link the design to the standards, control-plane artifacts, or current repository surfaces that constrain the solution.
5. Record a recommended design and explicit guardrails before creating or updating the implementation plan.
6. Keep front matter, `Record Metadata`, and the `Updated At` section aligned in the same change set.
7. Update companion READMEs or related design docs when the feature family or naming changes.

## Examples
- `docs/planning/design/features/core_python_workspace_and_harness.md` is a feature design because it defines package boundaries, tool expectations, and future capability areas.
- `docs/planning/design/features/schema_resolution_and_index_search.md` is a feature design because it compares options and recommends an architecture before implementation work is broken down.
- A commit checklist for one change set does not belong here; it belongs in an implementation plan, workflow, or task tracking surface.

## Operationalization
- `Modes`: `documentation`
- `Operational Surfaces`: `docs/templates/feature_design_template.md`; `docs/planning/design/features/`; `docs/planning/design/features/README.md`; `docs/planning/design/features/core_python_workspace_and_harness.md`

## Validation
- Feature designs should contain the required sections in the documented order.
- Feature-design front matter should validate against `feature_design_front_matter.v1.schema.json`.
- The recommended design should be specific enough that an implementation plan can break it into concrete work without re-deciding the architecture.
- Optional applied-reference sections should explain the implication of each cited source when present.
- `updated_at` in front matter and `Record Metadata` should match.
- Reviewers should reject feature designs that are only requirements capture, only task checklists, or missing the reasoning behind the recommendation.

## Change Control
- Update this standard and the feature design template in the same change set when the expected feature-design structure changes.
- Update the feature-design directory README when feature-design placement or family boundaries change.
- Refresh affected implementation plans when a feature design changes in a way that invalidates their assumptions or work breakdown.

## References
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)
- [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/design/features/README.md)

## Notes
- Feature designs are the design-authority layer for a capability until a later standard or control-plane artifact takes over a narrower concern.
- A good feature design reduces rework in implementation planning by making tradeoffs and guardrails explicit.

## Updated At
- `2026-03-11T06:00:00Z`
