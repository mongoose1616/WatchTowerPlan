# Foundations Context Review Workflow

## Purpose
Use this workflow to load the repository foundation documents that materially shape planning, design, or foundations-aware review work so the resulting artifact stays aligned with the repository's product model, design philosophy, standards posture, and technology direction.

## Use When
- A PRD, feature design, or related planning artifact should be aligned with `docs/foundations/`.
- A review or documentation-alignment task explicitly asks whether guidance stays cohesive with repository foundations or scope posture.
- A planning task depends on explicit product, standards, or technology-direction context.
- A task needs a short record of which foundation documents materially shaped the output.

## Inputs
- Scoped planning, design, or review task brief
- Relevant documents under `docs/foundations/`
- Known product, standards, or technology questions already surfaced by the task

## Additional Files to Load
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): identifies the design-philosophy constraints this workflow should surface for planning tasks.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): identifies the product-shape constraints this workflow should surface when planning depends on foundation context.

## Workflow
1. Select the relevant foundation documents.
   - Choose only the foundation docs that materially affect the active planning, design, or review task.
   - Prefer direct repository foundations over inferred product assumptions.
2. Extract the governing context.
   - Record the product boundaries, design principles, standards posture, or technology-direction guidance that should shape the task.
   - Keep the extracted context concise and tied to the active task rather than summarizing the full foundations set.
3. Surface alignment constraints.
   - Note any conflicts, gaps, or tensions between the request and the loaded foundation guidance.
   - Record which foundation docs should be cited or acknowledged in the resulting artifact.

## Data Structure
- Foundation documents reviewed
- Product and design constraints applied
- Standards or technology-direction guidance applied
- Alignment risks or conflicts

## Outputs
- A short foundation-context brief for the active planning, design, or review task
- A record of which foundation documents materially shaped the work

## Done When
- The active planning, design, or review task is aligned to the relevant foundation documents.
- The specific foundation sources used are explicit.
- Any material conflict with repository foundations has been surfaced clearly.
