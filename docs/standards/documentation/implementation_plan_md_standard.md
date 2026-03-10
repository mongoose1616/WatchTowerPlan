---
id: "std.documentation.implementation_plan_md"
title: "Implementation Plan Document Standard"
summary: "This standard defines the structure, placement, and boundary rules for implementation-plan documents stored under `docs/planning/design/implementation/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "implementation_plan_md"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:11:26Z"
audience: "shared"
authority: "authoritative"
---

# Implementation Plan Document Standard

## Summary
This standard defines the structure, placement, and boundary rules for implementation-plan documents stored under `docs/planning/design/implementation/`.

## Purpose
Keep implementation plans concrete enough to guide engineering work while preserving a clean boundary between approved design direction, workflow execution procedure, and direct code changes.

## Scope
- Applies to implementation-plan documents stored under `docs/planning/design/implementation/`.
- Covers placement, required sections, and the handoff relationship between feature designs and executable implementation work.
- Does not define workflow procedure, commit-message rules, or PRD structure.

## Use When
- Breaking an approved feature design into concrete engineering work.
- Planning a multi-step implementation slice before code changes begin.
- Refreshing a plan after the design, standards, or control-plane artifacts it depends on have changed materially.

## Related Standards and Sources
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): companion standard that constrains this standard's default section density and compact-authoring expectations.
- [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md): authoring scaffold that should stay aligned with this standard.
- [README.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/README.md): family entrypoint and inventory surface this standard should stay aligned with.
## Guidance
- Store implementation plans under `docs/planning/design/implementation/`.
- Keep one primary execution slice or tightly related engineering plan per document.
- Use governed front matter on implementation-plan documents and validate it against the published implementation-plan front matter profile.
- Use implementation plans to translate an approved feature design into technical approach, work breakdown, validation, and rollout expectations.
- Anchor each plan to the feature design, PRD, or direct user request that justified the work.
- Keep implementation plans above commit-by-commit notes; they should guide execution, not replace code review or workflow procedure.
- When an external topic already has a governed local reference under `docs/references/**`, cite that local reference as the repo-native lookup surface instead of scattering raw external URLs through the plan body.
- Include `Internal Standards and Canonical References Applied` only when a cited authority materially constrains the implementation details. When present, it must explain the local implication of each cited authority. Bare link lists are insufficient.
- Add `Current-State Context`, `Dependencies`, `Rollout or Migration Plan`, and `Open Questions` only when they materially improve execution clarity.
- A body `Updated At` section is optional; front matter `updated_at` and the `Record Metadata` value remain the required anchors.

## Structure or Data Model
### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Implementation plan | `docs/planning/design/implementation/<plan_name>.md` | Use stable snake_case filenames derived from the implementation slice. |
| Implementation-plan directory README | `docs/planning/design/implementation/README.md` | Directory orientation and inventory only. |

### Required sections for implementation plans
| Section | Requirement | Notes |
|---|---|---|
| `Record Metadata` | Required | Record the `trace_id`, plan `id`, lifecycle status, linked planning surfaces, and the same `updated_at` value carried in front matter. |
| `Summary` | Required | One short explanation of the plan and intended execution slice. |
| `Source Request or Design` | Required | Record the driving feature design, PRD, or user request. |
| `Scope Summary` | Required | State what the plan covers and excludes. |
| `Assumptions and Constraints` | Required | Record the assumptions or hard constraints that shape the work. |
| `Proposed Technical Approach` | Required | Describe the intended implementation structure and module boundaries. |
| `Work Breakdown` | Required | Break the work into concrete steps or slices. |
| `Risks` | Required | Record concrete risks or uncertainties. |
| `Validation Plan` | Required | State how the implementation will be verified. |
| `References` | Required | Link the design, standards, and companion artifacts that matter. |

### Optional sections for implementation plans
| Section | Use When |
|---|---|
| `Current-State Context` | Current repository surfaces or constraints matter and are not already obvious from the source design or request. |
| `Internal Standards and Canonical References Applied` | A cited internal authority materially constrains the implementation. Each bullet should record `source: implication`. |
| `Dependencies` | Real dependencies materially affect sequencing or feasibility. |
| `Rollout or Migration Plan` | Rollout, migration, or staged delivery expectations materially affect implementation. |
| `Open Questions` | Real planning questions remain unresolved. |

## Process or Workflow
1. Place the plan under `docs/planning/design/implementation/` with a stable snake_case filename.
2. Add governed front matter using the implementation-plan profile before the Markdown body.
3. Start from the implementation-plan template and keep the required sections in order.
4. Tie the plan back to the approved design, request, or PRD that justifies it.
5. Break the work into concrete technical slices and explicit validation steps before implementation begins.
6. Keep front matter, `Record Metadata`, and the `Updated At` section aligned in the same change set.
7. Refresh the plan when related standards, designs, or control-plane artifacts change enough to invalidate the work breakdown.

## Examples
- `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` is an implementation plan because it turns approved design direction into concrete module boundaries, work breakdown, and validation steps.
- A long-running operational runbook does not belong here; it belongs in a workflow or other operational documentation surface.

## Validation
- Implementation plans should contain the required sections in the documented order.
- Implementation-plan front matter should validate against `implementation_plan_front_matter.v1.schema.json`.
- The work breakdown should be concrete enough to guide coding, testing, and review.
- The plan should clearly state how success will be validated.
- The `Internal Standards and Canonical References Applied` section should explain the implication of each cited source when the section is present.
- `updated_at` in front matter and `Record Metadata` should match.
- Reviewers should reject plans that restate a feature design without introducing a real technical approach or execution breakdown.

## Change Control
- Update this standard and the implementation-plan template in the same change set when the expected implementation-plan structure changes.
- Update the implementation-plan directory README when placement or family boundaries change.
- Refresh affected implementation plans when an upstream feature design or standard changes their assumptions materially.

## References
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md)
- [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/README.md)

## Notes
- A good implementation plan narrows ambiguity before coding starts without duplicating workflow execution steps.
- Plans should stay modular so later capability areas can reuse the same planning shape.

## Updated At
- `2026-03-10T16:11:26Z`
