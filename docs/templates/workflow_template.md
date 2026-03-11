# <Workflow Name> Workflow

> Use this template for routed workflow modules, especially under `workflows/modules/`.
> Keep the exact section names and order below unless a narrower workflow standard explicitly requires more.
> Scope the file to one primary execution concern and delete any placeholder text that does not help the live workflow.
> Do not add YAML front matter unless a narrower standard or validator explicitly requires it.
> Treat `AGENTS.md`, `workflows/ROUTING_TABLE.md`, and `workflows/modules/core.md` as already-loaded routing baseline, not as per-module load hints.
> Do not list generic workflow standards such as `workflow_design_standard.md`, `routing_and_context_loading_standard.md`, or `workflow_md_standard.md` in `## Additional Files to Load`; they stay implicit in the routing baseline.
> Use `## Additional Files to Load` only when the module truly needs extra repo-local files beyond the normal routing baseline.
> When `## Additional Files to Load` is present, keep it short, use repository-native Markdown links, and write each bullet in `source: execution implication` form.
> Use repo-local Markdown links only when the target already exists or is being created in the same change.
> Treat `## Data Structure` and `## Outputs` as terse workflow-internal scaffolding. They should not imply extra repository sections, extra summaries, or extra status records unless another governed surface explicitly requires them.
> If the workflow result is a single document, code change, validation run, or task update, say that plainly and stop.

## Purpose
Use this workflow to <state the single execution objective clearly and concretely>.

## Use When
- <List the trigger conditions for using this workflow.>
- <Keep these conditions specific enough that routing or manual selection is clear.>

## Inputs
- <List the request, artifacts, standards, or canonical docs this workflow expects.>
- <Include companion standards or repository surfaces only when they materially govern execution.>

## Additional Files to Load
- <Repo-local file to open next>: <What this file changes or constrains in execution.>
- <Repo-local file to open next>: <What this file changes or constrains in execution.>

<Delete this section when the normal routing baseline already provides enough context. Do not list `AGENTS.md`, `workflows/ROUTING_TABLE.md`, `workflows/modules/core.md`, or the generic workflow standards here.>

## Workflow
1. <Write the first concrete step.>
   - <Add a short clarifying detail when the step needs interpretation constraints.>
2. <Write the next concrete step.>
   - <Keep steps ordered and actionable rather than descriptive only.>
   - <Prefer the smallest useful artifact or response that still satisfies the task.>
3. <Continue until the workflow reaches a clear stop condition.>

## Data Structure
- <Describe the workflow's internal working state or tracked fields.>
- <Keep this very brief and avoid restating the final artifact outline unless execution depends on it.>

## Outputs
- <List the concrete resulting surfaces or artifacts.>
- <Do not add meta deliverables unless another governed surface explicitly requires them.>

## Done When
- <State the completion criteria that make the workflow complete.>
- <Make it clear what must be true before execution stops.>
