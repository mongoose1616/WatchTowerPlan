---
id: "std.documentation.compact_document_authoring"
title: "Compact Document Authoring Standard"
summary: "This standard defines the repository rule that authored human-readable documents should default to the smallest useful shape that still preserves reviewability and machine-readable authority."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "compact_authoring"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:11:26Z"
audience: "shared"
authority: "authoritative"
---

# Compact Document Authoring Standard

## Summary
This standard defines the repository rule that authored human-readable documents should default to the smallest useful shape that still preserves reviewability and machine-readable authority.

## Purpose
Reduce low-value boilerplate in authored documents and generated human-readable outputs so maintainers and agents spend more context on real project decisions.

## Scope
- Applies to repository-authored templates under `docs/templates/`.
- Applies to governed planning and decision document families under `docs/planning/`.
- Applies to generic documentation and workflow guidance when that guidance materially shapes authored output size.
- Does not replace family-specific front matter, traceability, or schema requirements.

## Use When
- Creating or refreshing a repository template.
- Deciding whether a document section should be required, optional, or omitted by default.
- Reviewing whether a generated human-readable output is duplicating machine-readable authority without adding human value.

## Related Standards and Sources
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): compact authoring must preserve governed front matter where the document family requires machine-readable metadata.
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): workflow modules keep their structural sections, but their execution guidance should still prefer proportional repository output.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): human task tracking remains derived from authoritative task records and can therefore stay compact.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): initiative tracking remains a compact start-here view rather than a second planning authority layer.

## Guidance
- Default every authored template to the smallest section set that usually carries non-derivable value.
- Keep optional sections out of the default body scaffold unless they are needed in most real documents for that family.
- When a document family already has machine-readable front matter or a governed index, do not duplicate that machine detail in verbose body prose unless the duplication materially helps the human reader.
- Prefer concise required sections over long placeholder inventories of optional sections.
- Treat front matter as the primary machine surface for stable identity, lifecycle state, ownership, and timestamps when the document family uses governed front matter.
- A body `Updated At` section is optional when the family already carries `updated_at` in front matter and `Updated At` in record metadata.
- Generated human-readable trackers should prefer dense tables and brief zero-state text over placeholder `None` rows or repeated footer prose.
- Remove sections, bullets, or notes that restate obvious context without helping review, routing, or execution.

## Validation
- Reviewers should reject templates that normalize low-value optional sections into every new document.
- Reviewers should reject workflow guidance that encourages meta drafting records in repository artifacts when those records do not materially help the project.
- Generated human-readable outputs should stay scan-first and should not become the dense machine authority surface.

## Change Control
- Update this standard together with affected templates, family-specific documentation standards, workflow guidance, and sync renderers when compact-authoring rules change materially.
- Update validators or index builders in the same change set when a compact-authoring rule changes the required body shape for a governed family.

## References
- [docs/templates/README.md](/home/j/WatchTowerPlan/docs/templates/README.md)
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md)
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md)
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md)
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md)

## Updated At
- `2026-03-10T16:11:26Z`
