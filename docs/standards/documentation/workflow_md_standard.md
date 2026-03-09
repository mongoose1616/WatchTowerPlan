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
updated_at: "2026-03-09T18:46:06Z"
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
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md)

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
- Keep the required section names stable so routed use and review stay predictable.
- `Workflow` should be written as an ordered sequence when step order matters.
- `Inputs`, `Data Structure`, `Outputs`, and `Done When` should stay compact and task-oriented rather than turning into long narrative sections.
- `Data Structure` and `Outputs` may remain brief when the workflow does not define a stable working structure or durable deliverable, but the headings should still be present.
- Use repository-native Markdown links when companion standards, templates, or canonical files materially govern the workflow.
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
- Optional supporting sections may appear after `Done When` only when they materially improve local usability and do not obscure the core workflow shape.

## Validation
- The file should be recognizable as a workflow module from its title and required headings alone.
- The required sections should appear in the standard order with the standard names.
- The file should stay focused on one execution concern rather than mixing multiple unrelated procedures.
- The workflow body should be actionable and sequence-aware rather than only descriptive.
- Content that belongs in `AGENTS.md`, `ROUTING_TABLE.md`, or `docs/standards/**` should not be embedded as if it were workflow procedure.

## Change Control
- Update this standard when the repository changes the expected file shape for workflow Markdown documents.
- Update the workflow template in the same change set when the required heading set or order changes.
- Update affected workflow modules in the same change set when structural expectations change.

## References
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md)
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md)

## Notes
- The workflow template is an authoring scaffold. This standard is the normative file-shape rule.
- The workflow design standard defines how workflow behavior should be bounded; this document defines how the Markdown file should be structured.

## Updated At
- `2026-03-09T18:46:06Z`
