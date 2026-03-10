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
   - Capture the requirements, scenarios, and acceptance criteria that materially reduce ambiguity for the current scope.
   - Do not force user stories, metrics, or rollout notes when the PRD can stay simpler without losing review value.
4. Plan delivery.
   - Record dependencies, risks, milestones or phases, and unresolved questions only when they affect review or later planning.
5. Draft the PRD.
   - Convert the planning notes into the leanest PRD shape allowed by the PRD standard.
   - Remove ambiguity and vague language.
   - Keep requirements testable.

## Data Structure
- Problem statement
- Goals and non-goals
- Requirements and acceptance criteria
- Risks and dependencies
- Optional actors, scenarios, metrics, or open questions only when material

## Outputs
- A review-ready PRD draft
- Explicit unresolved questions only when they remain

## Done When
- The problem, goals, scope, and requirements are documented.
- The PRD remains aligned with the repository foundations in `docs/foundations/`.
- The PRD reflects applicable internal standards, canonical references, and existing planning patterns.
- Success metrics and acceptance criteria are defined.
- Risks, dependencies, and open questions are visible.
- The PRD does not carry low-value planning filler that the current scope does not need.
