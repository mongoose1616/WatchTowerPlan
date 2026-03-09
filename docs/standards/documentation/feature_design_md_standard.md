# Feature Design Document Standard

## Summary
This standard defines the structure, placement, and boundary rules for feature-level technical design documents stored under `docs/design/features/`.

## Purpose
Keep feature designs consistent enough to review, compare, and hand off into implementation planning without turning them into PRDs, workflow modules, or commit-level plans.

## Scope
- Applies to feature design documents stored under `docs/design/features/`.
- Covers placement, required sections, optional sections, and the relationship between feature designs and later implementation plans.
- Does not define PRD shape, workflow procedure, or implementation-plan breakdown format.

## Use When
- Creating a new technical design for a repository feature or capability.
- Reviewing whether a proposed design is specific enough for implementation planning.
- Refreshing a feature design after standards, control-plane artifacts, or architecture decisions change materially.

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)
- [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md)
- [README.md](/home/j/WatchTowerPlan/docs/design/features/README.md)

## Guidance
- Store feature designs under `docs/design/features/`.
- Keep one primary feature or tightly related capability cluster per design.
- Use feature designs to explain why a solution should be built a certain way before work is broken into implementation tasks.
- Feature designs should identify current-state constraints, options considered, the recommended design, and the implementation guardrails that later work must preserve.
- Do not use feature designs as workflow modules, changelogs, or commit-by-commit execution notes.
- Do not move normative repository rules into a feature design when they belong in `docs/standards/**`.
- Include only the external sources that materially shaped the design. Omit that section when none were needed.
- Use `Last Synced` to record the last meaningful content update date.

## Structure or Data Model
### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Feature design | `docs/design/features/<feature_name>.md` | Use stable snake_case filenames derived from the design topic. |
| Feature-design directory README | `docs/design/features/README.md` | Directory orientation and inventory only. |

### Required sections for feature designs
| Section | Requirement | Notes |
|---|---|---|
| `Summary` | Required | One short explanation of the design and intended outcome. |
| `Source Request` | Required | Record the request, issue, or planning input that triggered the design. |
| `Scope and Feature Boundary` | Required | Define what the design covers and excludes. |
| `Current-State Context` | Required | Describe current repository surfaces, constraints, or gaps that matter. |
| `Foundations References Applied` | Required | Map relevant foundations docs to design implications. |
| `Internal Standards and Canonical References Applied` | Required | Record the internal authorities that shaped the design. |
| `Design Goals and Constraints` | Required | State the main goals, non-goals, and invariants. |
| `Options Considered` | Required | Compare at least two meaningful approaches when tradeoffs exist. |
| `Recommended Design` | Required | Describe the chosen architecture, flow, and failure behavior. |
| `Affected Surfaces` | Required | List the repo surfaces likely to change. |
| `Design Guardrails` | Required | Call out rules implementation planning must preserve. |
| `Implementation-Planning Handoff Notes` | Required | State what the implementation plan should do next. |
| `Dependencies` | Required | Record meaningful internal or external dependencies. |
| `Risks` | Required | Record concrete risks or uncertainties. |
| `References` | Required | Link companion docs or artifacts. |
| `Last Synced` | Required | Record the last meaningful content update date. |

### Optional sections for feature designs
| Section | Use When |
|---|---|
| `External Sources Consulted` | An external primary source materially shaped the design. |
| `Open Questions` | Real design questions remain unresolved. |

## Process or Workflow
1. Place the design under `docs/design/features/` with a stable snake_case filename.
2. Draft the document using the feature design template and required section order.
3. Link the design to the standards, control-plane artifacts, or current repository surfaces that constrain the solution.
4. Record a recommended design and explicit guardrails before creating or updating the implementation plan.
5. Update companion READMEs or related design docs when the feature family or naming changes.

## Examples
- `docs/design/features/core_python_workspace_and_harness.md` is a feature design because it defines package boundaries, tool expectations, and future capability areas.
- `docs/design/features/schema_resolution_and_index_search.md` is a feature design because it compares options and recommends an architecture before implementation work is broken down.
- A commit checklist for one change set does not belong here; it belongs in an implementation plan, workflow, or task tracking surface.

## Validation
- Feature designs should contain the required sections in the documented order.
- The recommended design should be specific enough that an implementation plan can break it into concrete work without re-deciding the architecture.
- The document should cite the internal standards and canonical surfaces that constrain the design.
- Reviewers should reject feature designs that are only requirements capture, only task checklists, or missing the reasoning behind the recommendation.

## Change Control
- Update this standard and the feature design template in the same change set when the expected feature-design structure changes.
- Update the feature-design directory README when feature-design placement or family boundaries change.
- Refresh affected implementation plans when a feature design changes in a way that invalidates their assumptions or work breakdown.

## References
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)
- [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md)
- [README.md](/home/j/WatchTowerPlan/docs/design/features/README.md)

## Notes
- Feature designs are the design-authority layer for a capability until a later standard or control-plane artifact takes over a narrower concern.
- A good feature design reduces rework in implementation planning by making tradeoffs and guardrails explicit.

## Last Synced
- `2026-03-09`
