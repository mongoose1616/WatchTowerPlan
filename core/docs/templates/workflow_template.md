# <Workflow Name> Workflow

> Use this template for routed workflow documents, especially under `core/workflows/modules/`, `core/workflows/roles/`, and pack-owned workflow roots.
> For role-root files, rename the H1 to `# <Role Name> Role` and keep the `## Composes Modules` section. For module-root files, delete `## Composes Modules`.
> Keep the exact section names and order below unless a narrower workflow standard explicitly requires more.
> Scope the file to one primary execution concern and delete any placeholder text that does not help the live workflow.
> Do not add YAML front matter unless a narrower standard or validator explicitly requires it.
> Treat `AGENTS.md`, the shared routing table, any pack-owned routing tables, and `core/workflows/modules/core.md` as already-loaded routing baseline, not as per-module load hints.
> Treat the routing table as the authority for which workflow documents become active. `## Composes Modules` in a role documents explicit role-to-module orchestration; it does not replace routed activation.
> Do not list generic workflow standards such as `workflow_design_standard.md`, `routing_and_context_loading_standard.md`, or `workflow_md_standard.md` in `## Additional Files to Load`; they stay implicit in the routing baseline.
> Use `## Additional Files to Load` only when the module truly needs extra repo-local files beyond the normal routing baseline.
> When `## Additional Files to Load` is present, list every extra repo-local file whose absence would materially change execution, use repository-native Markdown links such as `/core/docs/...`, `/<pack>/docs/...`, `/core/workflows/...`, `/<pack>/workflows/...`, or another concrete repo path, and write each bullet in `source: execution implication` form.
> Do not use filesystem-absolute checkout paths such as `/home/...` in workflow modules; they are not portable across clones, branches, or worktrees.
> Use repo-local Markdown links only when the target already exists or is being created in the same change.
> Treat `## Data Structure` and `## Outputs` as workflow-internal scaffolding that should be as detailed as needed to remove ambiguity. They should not imply extra repository sections, extra summaries, or extra status records unless another governed surface explicitly requires them.
> Do not normalize sibling sections to the same size or replace materially distinct branches, exceptions, handoffs, or outputs with catch-all placeholders.
> If the workflow result is a single document, code change, validation run, or task update, say that plainly while still documenting any materially distinct constraints, branches, or outputs needed for correct execution.

## Purpose
Use this workflow to <state the single execution objective clearly and concretely>.

## Use When
- <List the trigger conditions for using this workflow.>
- <Keep these conditions specific enough that routing or manual selection is clear.>

## Inputs
- <List the request, artifacts, standards, or canonical docs this workflow expects.>
- <Include companion standards or repository surfaces only when they materially govern execution.>

## Composes Modules
- <Repo-local workflow module path>: <How this role directly orchestrates or specializes that reusable module.>
- <Repo-local workflow module path>: <How this role directly orchestrates or specializes that reusable module.>

<Delete this section for module-root workflow files. Keep it for role-root workflow files and list only the reusable modules that are materially part of the role's direct orchestration contract.>

## Additional Files to Load
- <Repo-local file to open next>: <What this file changes or constrains in execution.>
- <Repo-local file to open next>: <What this file changes or constrains in execution.>

<Delete this section when the normal routing baseline already provides enough context. Keep every extra file whose absence would materially change execution, and omit the section entirely when there are none. Do not list `AGENTS.md`, the shared routing table, pack-owned routing tables, `core/workflows/modules/core.md`, or the generic workflow standards here. For role-root files, keep `## Composes Modules` separate from these extra context hints.>

## Workflow
<Write the workflow as an ordered sequence when step order matters. Continue the sequence for as many steps as the workflow requires, and include each materially distinct branch, checkpoint, or handoff needed for correct execution. Add clarifying detail only where interpretation boundaries matter.>

## Data Structure
- <Describe the workflow's internal working state or tracked fields.>
- <Include every materially distinct tracked field or concept the workflow depends on, and avoid restating the final artifact outline unless execution depends on it.>

## Outputs
- <List the concrete resulting surfaces or artifacts.>
- <Do not add meta deliverables unless another governed surface explicitly requires them.>

## Done When
- <State the completion criteria that make the workflow complete.>
- <Make it clear what must be true before execution stops.>
