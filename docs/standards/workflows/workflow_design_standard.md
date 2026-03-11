---
id: "std.workflows.workflow_design"
title: "Workflow Design Standard"
summary: "This standard defines how workflow modules in this repository should be designed, structured, and bounded."
type: "standard"
status: "active"
tags:
  - "standard"
  - "workflows"
  - "workflow_design"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
---

# Workflow Design Standard

## Summary
This standard defines how workflow modules in this repository should be designed, structured, and bounded.

## Purpose
Keep workflow modules small, composable, and explicit so routed task execution stays predictable, reviewable, and aligned with the repository's governed operating model.

## Scope
- Applies to workflow modules under `workflows/modules/**`.
- Covers workflow-module objective, structure, boundary rules, and handoff expectations.
- Does not define routing classification logic for `ROUTING_TABLE.md` or repository-wide wrapper behavior for `AGENTS.md`.

## Use When
- Creating a new workflow module.
- Reviewing whether an existing workflow module is too broad, too vague, or misplaced.
- Splitting a large workflow into smaller routed modules.

## Related Standards and Sources
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): foundation intent this standard must remain aligned with.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md): distilled external guidance for keeping workflow modules narrow, explicit, and efficient for LLM or agent use.
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md): authoring scaffold that should stay aligned with this standard.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): workflow surface that operationalizes or depends on this standard.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): companion repository surface this standard should stay aligned with.

## Inputs
- The task type or execution concern the workflow is meant to govern.
- The adjacent routing behavior and companion workflows that interact with it.
- The minimum standards, references, and repository surfaces the workflow needs to reference.

## Guidance
- Design each workflow module around one primary objective.
- Keep workflow modules loadable through routing rather than as broad narrative docs that require human interpretation to become usable.
- Make triggers explicit through `Use When`.
- Make expected inputs explicit through `Inputs`.
- Make execution behavior explicit through `Workflow`.
- Use `Data Structure` and `Outputs` to describe the workflow's internal working shape and real task outcomes, not to justify extra prose in repository artifacts.
- Prefer the smallest useful repository artifact, response, or change set that satisfies the task.
- Make stop conditions explicit through `Done When`.
- Prefer composing multiple small workflows over one catch-all workflow that mixes unrelated execution concerns.
- When the same concrete execution phase recurs across multiple task families, factor it into a reusable shared workflow module instead of copying it into every task-family workflow.
- Put repository-wide wrappers and dos and don'ts in `AGENTS.md`, not inside workflow modules.
- Put classification rules in `ROUTING_TABLE.md`, not inside workflow modules.
- Put normative repository policy in `docs/standards/**`, not inside workflow modules.
- Workflows may reference standards, templates, or canonical docs, but they should not silently replace them.
- Workflow modules may publish `Additional Files to Load` only when extra repo-local files beyond the routing baseline materially change execution.
- `Additional Files to Load` should point to the next files an agent or maintainer should actually open, not to generic repo-wide context that routing already guarantees.
- `Additional Files to Load` bullets should use `source: execution implication` form and remain short enough to keep the module scan-friendly.
- Steps should be ordered and concrete enough that the workflow can be followed without hidden verbal context.
- Workflows should prefer clarify-before-execute behavior when ambiguity materially affects correctness.
- Workflow steps should call out adjacent-document updates or companion workflow loading when coherence requires it.
- Workflow modules should be written so they can be merged with other routed modules without contradicting them.
- Do not treat `Outputs` as permission to require meta summaries, quality-check reports, source logs, or progress notes when the changed artifact or validation result already captures that information.

## Structure or Data Model
### Required module sections
| Section | Required Role | Notes |
|---|---|---|
| `Purpose` | Defines the workflow's primary objective | Keep it singular and specific. |
| `Use When` | Defines the trigger conditions | Make routing or invocation intent clear. |
| `Inputs` | Defines the information the workflow expects | Include standards or canonical docs when they materially govern execution. |
| `Workflow` | Defines the ordered execution behavior | Steps should be concrete and bounded. |
| `Data Structure` | Defines the internal working structure the workflow expects or produces | Keep it brief and avoid mirroring final-document headings unless the workflow truly depends on them. |
| `Outputs` | Defines the intended deliverables | List actual changed surfaces or resulting artifacts, not generic meta records. |
| `Done When` | Defines completion criteria | Make stopping conditions visible. |

### Optional module sections
| Section | Optional Role | Notes |
|---|---|---|
| `Additional Files to Load` | Identifies extra repo-local files to open beyond the routing baseline | Keep it short and use `source: execution implication` bullets. |

### Boundary rules
- A workflow module should not mix routing logic, repository-wide wrappers, and task execution in one document.
- A workflow module should not become a hidden policy document.
- A workflow module should not depend on unstated tribal knowledge to be usable.
- A shared phase module is valid only when it remains a concrete execution concern rather than vague meta-guidance.
- A workflow module may reference external sources only when authoritative guidance materially affects the workflow and no adequate internal source exists.
- A workflow module should not restate routing-baseline files as if they were task-specific additional context.

## Process or Workflow
1. Identify the single execution concern the workflow should own.
2. Confirm that the concern belongs in a workflow module rather than a standard, template, or routing surface.
3. Draft the module using the workflow template and the required sections.
4. Add `Additional Files to Load` only when the module truly needs extra repo-local files beyond normal routing context.
5. Tighten the steps until the module is specific enough to execute without broad inferred behavior.
6. Check whether the workflow should stay standalone or whether the concern should be split into multiple smaller modules.
7. Align the new or updated workflow with the routing table and any companion standards in the same change set when needed.

## Examples
- A code-implementation workflow belongs in `workflows/modules/` because it defines execution behavior for implementing changes.
- A routing rule does not belong in a workflow module because routing classification belongs in `ROUTING_TABLE.md`.
- A repository-wide documentation policy does not belong in a workflow module because it belongs in `docs/standards/**`.

## Operationalization
- `Modes`: `workflow`; `documentation`
- `Operational Surfaces`: `workflows/modules/`; `workflows/ROUTING_TABLE.md`; `docs/templates/workflow_template.md`; `AGENTS.md`

## Validation
- A reviewer should be able to identify the workflow's single objective quickly.
- The module should be executable as written without broad unstated assumptions.
- The workflow should not duplicate the role of `AGENTS.md`, `ROUTING_TABLE.md`, or a standards document.
- The required sections should be present and materially useful rather than empty headings.
- `Data Structure` and `Outputs` should stay concise and should not imply extra deliverables beyond the requested task.
- `Additional Files to Load` should appear only when the workflow actually needs task-specific extra files beyond the routing baseline.
- When `Additional Files to Load` appears, it should point to concrete repo-local files and explain why each file changes execution.
- Generic routing-baseline files should not be repeated as task-specific authorities.
- The module should compose cleanly with the other routed workflows that are likely to be loaded with it.

## Change Control
- Update this standard when the repository changes the expected shape or role of workflow modules.
- Update the workflow template and affected workflow modules in the same change set when structural expectations change.
- Update routing surfaces in the same change set when a workflow split, merge, or rename changes task classification.

## References
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md)
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md)
- [workflow_template.md](/home/j/WatchTowerPlan/docs/templates/workflow_template.md)
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md)
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md)

## Notes
- This standard is about workflow-module design, not about one specific workflow family.
- File-level Markdown shape belongs in [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md).
- Narrower workflow standards may add extra rules for specific workflow types, but they should refine rather than weaken this baseline.

## Updated At
- `2026-03-11T06:00:00Z`
