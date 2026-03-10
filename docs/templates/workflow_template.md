# <Workflow Name> Workflow

> Use this template for routed workflow modules, especially under `workflows/modules/`.
> Keep the exact section names and order below unless a narrower workflow standard explicitly requires more.
> Scope the file to one primary execution concern and delete any placeholder text that does not help the live workflow.
> Do not add YAML front matter unless a narrower standard or validator explicitly requires it.
> Treat `AGENTS.md`, `workflows/ROUTING_TABLE.md`, and `workflows/modules/core.md` as already-loaded routing baseline, not as per-module load hints.
> Use `## Additional Files to Load` only when the module truly needs extra repo-local files beyond the normal routing baseline.
> When `## Additional Files to Load` is present, keep it short, use repository-native Markdown links, and write each bullet in `source: execution implication` form.

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
3. <Continue until the workflow reaches a clear stop condition.>

## Data Structure
- <Describe the working structure, checklist shape, or tracked state the workflow expects or produces.>
- <Keep this brief if the workflow does not rely on a strong internal structure.>

## Outputs
- <List the concrete deliverables, records, or updated surfaces the workflow should produce.>
- <Keep outputs tied to real task outcomes.>

## Done When
- <State the completion criteria that make the workflow complete.>
- <Make it clear what must be true before execution stops.>
