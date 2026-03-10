# PRD Generation Workflow

## Purpose
Use this workflow to turn a scoped planning request into a review-ready product requirements document (PRD).

## Use When
- A new feature or initiative needs alignment before implementation.
- Scope is still fuzzy and needs structure.
- Stakeholders need a written document to review or approve.

## Inputs
- Scoped PRD brief
- Problem statement
- Target users
- Business goal
- Foundation-context brief
- Current-state context summary when the PRD depends on an existing repository or product surface
- Internal standards and canonical references applied
- External guidance notes when needed
- Constraints
- Timeline expectations
- Known dependencies
- Open questions

## Additional Files to Load
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md): defines the required PRD structure and validation bar for the output.
- [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md): gives the starting shape for drafting the PRD once scope and requirements are clear.

## Workflow
1. Define scope.
   - List what is in scope.
   - List what is out of scope.
   - Use the current-state context when the PRD extends, replaces, or depends on an existing repository or product surface.
   - Record assumptions and constraints.
2. Define success.
   - Write the primary goal.
   - Add measurable success metrics where possible.
   - Note failure conditions or risks.
3. Gather requirements.
   - Capture functional requirements, non-functional requirements, user flows or key scenarios, and acceptance criteria.
4. Plan delivery.
   - Record dependencies, risks, milestones or phases, and unresolved questions.
5. Draft the PRD.
   - Convert the planning notes into the PRD structure below.
   - Remove ambiguity and vague language.
   - Keep requirements testable.

## Data Structure
- Title
- Summary
- Problem statement
- Goals
- Non-goals
- Target users
- User stories or scenarios
- Requirements
- Acceptance criteria
- Success metrics
- Risks and dependencies
- Rollout or launch notes
- Open questions

## Outputs
- A scoped project plan
- A review-ready PRD draft
- A list of unresolved questions and decisions

## Done When
- The problem, goals, scope, and requirements are documented.
- The PRD remains aligned with the repository foundations in `docs/foundations/`.
- The PRD reflects applicable internal standards, canonical references, and existing planning patterns.
- Success metrics and acceptance criteria are defined.
- Risks, dependencies, and open questions are visible.
