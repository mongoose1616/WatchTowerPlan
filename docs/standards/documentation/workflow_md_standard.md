---
id: "std.documentation.workflow_md"
title: "Workflow Markdown Standard"
summary: "This standard defines the document-level structure and boundary rules for workflow Markdown files in this repository."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "workflow_md"
owner: "repository_maintainer"
updated_at: "2026-03-11T23:19:00Z"
audience: "shared"
authority: "authoritative"
---

# Workflow Markdown Standard

## Summary
This standard defines the document-level structure and boundary rules for workflow Markdown files in this repository.

## Purpose
Keep workflow files predictable, easy to scan, and easy to route to by standardizing their required headings, ordering, and file-level scope.

## Scope
- Applies to workflow Markdown files that define task execution behavior, especially files under `workflows/modules/**`.
- Covers file-level structure, heading conventions, section ordering, and what belongs in the document body.
- Does not define routing classification logic for `ROUTING_TABLE.md`.
- Does not replace the deeper behavioral rules in the workflow design standard.

## Use When
- Creating a new workflow module.
- Revising an existing workflow Markdown file.
- Reviewing whether a workflow file is structurally consistent with the repository model.

## Related Standards and Sources
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): workflow modules inherit the shared semantic guardrails for repo-local links and list-to-heading spacing.
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md): distilled external guidance for keeping workflow modules explicit, narrow, and efficient for LLM or agent use.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow modules publish machine-readable lookup records through the derived workflow index.
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md): authoring scaffold that should stay aligned with this standard.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): workflow surface that operationalizes or depends on this standard.

## Guidance
- Workflow files should live under `workflows/modules/` unless a narrower repository standard defines another workflow surface.
- Each file should define one workflow with one primary execution concern.
- The document title should clearly name the workflow and include `Workflow`.
- Use these exact H2 section headings in this order:
  - `Purpose`
  - `Use When`
  - `Inputs`
  - `Workflow`
  - `Data Structure`
  - `Outputs`
  - `Done When`
- `Additional Files to Load` is optional and may appear only between `Inputs` and `Workflow`.
- Keep the required section names stable so routed use and review stay predictable.
- `Workflow` should be written as an ordered sequence when step order matters.
- `Inputs`, `Data Structure`, `Outputs`, and `Done When` should stay compact and task-oriented rather than turning into long narrative sections.
- `Data Structure` should describe internal working state or tracked fields, not a shadow outline for the final repository artifact.
- `Outputs` should name the actual resulting surfaces. When the changed document, tracker, code change, or validation result is itself the output, do not pad the workflow with extra record-keeping deliverables.
- Prefer `1` to `5` bullets in `Inputs`, `Data Structure`, and `Outputs` unless the task genuinely needs more structure.
- `Additional Files to Load` should be omitted when the routing baseline already provides enough context.
- `Additional Files to Load` should list only repo-local files that a reader or agent should open in addition to the normal routing baseline.
- `Additional Files to Load` bullets should use `source: execution implication` form so the local effect of each file is explicit.
- `Additional Files to Load` should stay short, normally `1` to `5` bullets.
- `Additional Files to Load` should not repeat repo-wide baseline surfaces such
  as `AGENTS.md`, `workflows/ROUTING_TABLE.md`, `workflows/modules/core.md`, or
  generic workflow standards such as
  `workflow_design_standard.md`, `routing_and_context_loading_standard.md`, and
  `workflow_md_standard.md`.
- Repo-local Markdown links should resolve to existing repository targets and should fail validation when they drift.
- Workflow modules should stay structured enough that the derived workflow index can capture their title, purpose summary, and task-specific additional files without manual curation.
- `Data Structure` and `Outputs` may remain brief when the workflow does not define a stable working structure or durable deliverable, but the headings should still be present.
- Use repository-native Markdown links when `Additional Files to Load` is present so the files can be captured and queried deterministically.
- Prefer governed local reference docs under `docs/references/**` instead of raw external URLs when outside authority materially affects the workflow.
- Do not add front matter to workflow modules unless a narrower standard or validator explicitly requires it.
- Do not put routing-table row logic in a workflow file.
- Do not put repository-wide wrapper rules in a workflow file when they belong in `AGENTS.md`.
- Do not turn a workflow file into a standards document, design note, or broad explainer.

## Structure or Data Model
- Title in the form `# <Workflow Name> Workflow`
- Required H2 sections in this order:
  - `Purpose`
  - `Use When`
  - `Inputs`
  - `Workflow`
  - `Data Structure`
  - `Outputs`
  - `Done When`
- Optional `Additional Files to Load` may appear between `Inputs` and `Workflow`.
- Optional supporting sections may appear after `Done When` only when they materially improve local usability and do not obscure the core workflow shape.

## Operationalization
- `Modes`: `workflow`; `documentation`
- `Operational Surfaces`: `workflows/modules/`; `workflows/modules/core.md`; `workflows/ROUTING_TABLE.md`; `docs/templates/workflow_template.md`

## Validation
- The file should be recognizable as a workflow module from its title and required headings alone.
- The required sections should appear in the standard order with the standard names.
- The file should stay focused on one execution concern rather than mixing multiple unrelated procedures.
- The workflow body should be actionable and sequence-aware rather than only descriptive.
- `Data Structure` and `Outputs` should remain brief and should not require standalone meta deliverables unless another governed surface explicitly requires them.
- `Additional Files to Load` should be absent when the workflow does not need extra repo-local context beyond the routing baseline.
- If `Additional Files to Load` is present, each bullet should identify a concrete repo-local file and explain the execution implication of loading it.
- Repo-local Markdown links should resolve to existing files or directories under the repository root.
- If `Additional Files to Load` is present, it should not repeat generic routing-baseline authorities.
- Content that belongs in `AGENTS.md`, `ROUTING_TABLE.md`, or `docs/standards/**` should not be embedded as if it were workflow procedure.

## Change Control
- Update this standard when the repository changes the expected file shape for workflow Markdown documents.
- Update the workflow template and workflow index surfaces in the same change set when the required heading set, order, or optional additional-load model changes.
- Update affected workflow modules in the same change set when structural expectations change.

## References
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md)
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md)
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md)
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md)

## Notes
- The workflow template is an authoring scaffold. This standard is the normative file-shape rule.
- The workflow design standard defines how workflow behavior should be bounded; this document defines how the Markdown file should be structured.

## Updated At
- `2026-03-11T23:19:00Z`
