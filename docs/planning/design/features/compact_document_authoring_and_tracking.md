---
trace_id: "trace.template_and_output_efficiency"
id: "design.features.compact_document_authoring_and_tracking"
title: "Compact Document Authoring and Tracking Design"
summary: "Defines the design for making authored templates and generated planning trackers compact by default while preserving governed machine-readable authority."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:00:54Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/templates/"
  - "docs/standards/documentation/"
  - "workflows/modules/"
  - "core/python/src/watchtower_core/repo_ops/"
aliases:
  - "compact authoring design"
---

# Compact Document Authoring and Tracking Design

## Record Metadata
- `Trace ID`: `trace.template_and_output_efficiency`
- `Design ID`: `design.features.compact_document_authoring_and_tracking`
- `Design Status`: `active`
- `Linked PRDs`: `prd.template_and_output_efficiency`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `design.implementation.template_and_output_efficiency_execution`
- `Updated At`: `2026-03-10T16:00:54Z`

## Summary
Defines the design for making authored templates and generated planning trackers compact by default while preserving governed machine-readable authority.

## Source Request
- User request to review templates and their outputs, remove low-value boilerplate, tighten verbose instructions, and complete the work through a new initiative.

## Scope and Feature Boundary
- Covers document templates, workflow-module instructions, planning-document validation rules, and generated human-readable planning trackers.
- Covers the relationship between those human surfaces and their machine-readable front matter and index companions.
- Does not redesign the machine-readable artifact families or rewrite unrelated documentation just for style alignment.

## Current-State Context
- [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md) and [decision_record_template.md](/home/j/WatchTowerPlan/docs/templates/decision_record_template.md) do not include the governed front matter their live output families actually require.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md), [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md), and [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md) still normalize more required body structure than many small repository changes need.
- The tracker sync services under [repo_ops/sync](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync) spend lines on repeated summary, update-rule, and reference scaffolding plus placeholder `None` rows.
- Documentation and planning workflow modules still describe outputs and data structures in ways that can encourage meta content rather than the smallest useful repository artifact.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): reduce ceremony where it does not materially improve correctness.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): machine-readable authority should absorb machine detail so human docs can stay focused on operator value.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): preserve context efficiency so future product work can spend more tokens on implementation and less on repeating scaffolding.

## Internal Standards and Canonical References Applied
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): governed document families still need stable front matter even when the body gets leaner.
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): workflow modules keep their structural sections but should stop implying that every output must include meta records of the work.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task records remain the authority while the task tracker becomes more compact.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): initiative tracking remains a derived start-here view and can be compacted without moving authority out of indexes and task records.

## External Sources Consulted
- None. The problem is repository-local alignment between templates, validators, sync renderers, and workflow guidance.

## Design Goals and Constraints
- Keep compactness changes bounded to surfaces that directly affect authored output or generated human tracking output.
- Preserve machine-readable authority in front matter, schemas, indexes, and validators.
- Prefer allowing optional sections to disappear entirely over replacing them with placeholder prose.
- Avoid forcing a broad migration across existing documents just to satisfy the new compact defaults.

## Options Considered
### Option 1
- Tighten template wording only.
- Low implementation cost.
- Rejected because validators and sync renderers would still force verbose output patterns and stale template-machine misalignment.

### Option 2
- Remove large amounts of structure and rely mostly on freeform prose plus indexes.
- Would aggressively reduce document size.
- Rejected because it would weaken reviewability and break the repository's governed-document model.

### Option 3
- Keep governed machine structure, but shift optional detail out of default templates, relax low-value required sections, and compact the generated trackers.
- Chosen because it reduces noise while preserving the repo's existing validation and traceability model.

## Recommended Design
### Compact Authored Documents
- Add one compact-authoring standard that makes proportional output an explicit repository rule.
- Update planning and decision validators so genuinely optional sections are validated only when present instead of being required everywhere.
- Align templates with their governed families by adding missing front matter where required and by moving optional sections out of the default body scaffold.

### Compact Generated Trackers
- Keep the machine-readable indexes as the dense authority surfaces.
- Rebuild planning trackers as compact scan-first views with short zero-state text instead of placeholder rows.
- Drop or conditionally suppress low-signal columns such as notes columns when they contain no real data.
- Remove repeated summary, update-rule, and reference scaffolding from generated trackers when that information is already governed elsewhere.

### Compact Workflow Guidance
- Keep workflow-module structure stable, but tighten planning and documentation modules so they explicitly prefer the smallest useful artifact.
- Remove workflow language that implies every task should emit meta records of the drafting process.
- Make templates and workflows agree that optional sections should be added only when they carry non-derivable information.

### Invariants and Failure Cases
- Front matter and machine indexes remain authoritative for IDs, lifecycle state, and machine lookup.
- If a compacted document still includes an optional applied-reference section, it must keep the current explained-bullet semantics.
- Tracker compaction must not remove fields needed to route a human to the next relevant surface.

## Affected Surfaces
- `docs/templates/`
- `docs/standards/documentation/`
- `docs/standards/governance/`
- `workflows/modules/`
- `core/python/src/watchtower_core/repo_ops/planning_documents.py`
- `core/python/src/watchtower_core/repo_ops/task_documents.py`
- `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`
- `core/python/src/watchtower_core/repo_ops/sync/*tracking.py`
- `core/python/tests/`

## Design Guardrails
- Do not move machine-readable contract detail out of front matter or indexes into tracker prose.
- Do not require broad document rewrites when validator changes can preserve backward compatibility.
- Do not compact trackers so far that a maintainer loses the first relevant file to open next.

## Implementation-Planning Handoff Notes
- Land compact authoring rules, template alignment, and validator relaxation first because those changes define the durable shape.
- Land tracker compaction next because it depends on a clear rule about what belongs in human surfaces versus machine surfaces.
- Land workflow guidance tightening last so the guidance reflects the new durable template and tracker shape.

## Dependencies
- Current governed front matter schemas and planning-document loaders.
- Existing planning and initiative tracking standards.
- Existing planning tracker sync services and unit-test coverage.

## Risks
- Validator relaxation could accidentally mask truly missing planning content if the required set becomes too small.
- Compacting trackers could create instability in tests if the empty-state shape and column decisions are not deterministic.

## Open Questions
- Whether the compact-authoring standard should eventually govern command pages and reference docs more strongly than this first pass.

## References
- [template_and_output_efficiency.md](/home/j/WatchTowerPlan/docs/planning/prds/template_and_output_efficiency.md)
- [docs/templates/README.md](/home/j/WatchTowerPlan/docs/templates/README.md)
- [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md)
- [decision_record_template.md](/home/j/WatchTowerPlan/docs/templates/decision_record_template.md)
- [documentation_generation.md](/home/j/WatchTowerPlan/workflows/modules/documentation_generation.md)

## Updated At
- `2026-03-10T16:00:54Z`
