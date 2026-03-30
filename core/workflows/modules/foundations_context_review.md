# Foundations Context Review Workflow

## Purpose
Use this workflow to load the repository foundation documents that materially shape planning, design, or foundations-aware review work so the resulting artifact stays aligned with the repository's product model, design philosophy, standards posture, and technology direction.

## Use When
- A design brief, decision record, or pack-owned planning artifact should be aligned with `core/docs/foundations/`.
- A review or documentation-alignment task explicitly asks whether guidance stays cohesive with repository foundations or scope posture.
- A planning task depends on explicit product, standards, or technology-direction context.
- A task needs an explicit record of which foundation documents materially shaped the output.

## Inputs
- Scoped planning, design, or review task brief
- Relevant documents under `core/docs/foundations/`
- Known product, standards, or technology questions already surfaced by the task

## Additional Files to Load
- [repository_scope.md](/core/docs/foundations/repository_scope.md): anchors current repository ownership so review work does not let future-product language redefine present repo scope.
- [engineering_design_principles.md](/core/docs/foundations/engineering_design_principles.md): identifies the design-philosophy constraints this workflow should surface for planning tasks.
- [repository_standards_posture.md](/core/docs/foundations/repository_standards_posture.md): identifies the governance and same-change-set alignment posture this workflow should preserve.
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md): identifies the current technology-direction constraints this workflow should surface when implementation or tooling surfaces are in scope.
- [product_direction.md](/core/docs/foundations/product_direction.md): identifies the product-shape constraints this workflow should surface when planning depends on foundation context.

## Workflow
1. Select the relevant foundation documents.
   - Start with `repository_scope.md` for foundations-aware review and documentation-alignment tasks so current repository ownership stays explicit.
   - Choose only the foundation docs that materially affect the active planning, design, or review task.
   - Use `watchtower-core query foundations --related-path <path> --format json` when the task starts from one repo surface and you need deterministic machine lookup to narrow which foundation docs to read first.
   - Add `repository_standards_posture.md` when the task can affect authority boundaries, synchronized updates, or governance expectations.
   - Add `engineering_stack_direction.md` when the task affects implementation, tooling, validation, or storage choices.
   - Add [customer_story.md](/core/docs/foundations/customer_story.md) when product or design work depends on the intended future operator or user experience, not only on the future product boundary.
   - Add another governed progress surface when the task is a review loop about overall repository coherence, authority, or next remediation work.
   - Prefer direct repository foundations over inferred product assumptions.
2. Extract the governing context.
   - Record the product boundaries, design principles, standards posture, or technology-direction guidance that should shape the task.
   - Keep the extracted context tied to the active task rather than summarizing the full foundations set, but include every materially distinct boundary, principle, or tension the task depends on.
3. Surface alignment constraints.
   - Note any conflicts, gaps, or tensions between the request and the loaded foundation guidance.
   - Record which foundation docs should be cited or acknowledged in the resulting artifact.

## Data Structure
- Foundation documents reviewed
- Product and design constraints applied
- Standards or technology-direction guidance applied
- Alignment risks or conflicts

## Outputs
- A foundation-context record for the active planning, design, or review task that captures every materially distinct governing boundary
- A record of which foundation documents materially shaped the work

## Done When
- The active planning, design, or review task is aligned to the relevant foundation documents.
- The specific foundation sources used are explicit.
- Any material conflict with repository foundations has been surfaced clearly.
