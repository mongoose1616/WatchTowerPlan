# Implementation Planning Workflow

## Purpose
Use this workflow to turn approved planning inputs into an actionable implementation plan with a work breakdown, validation strategy, and delivery sequence.

## Use When
- A PRD and feature design are approved or mostly complete and engineering planning needs to begin.
- The team needs technical scope, sequencing, and dependencies before implementation.
- Work must be broken into concrete tasks, milestones, or workstreams.

## Inputs
- Scoped implementation-planning brief
- Approved or draft PRD
- Approved or draft feature design, technical design, or architecture proposal
- Current-state context summary
- Internal standards and canonical references applied
- External guidance notes when needed
- Technical constraints
- Non-functional requirements
- Timeline or staffing assumptions
- Known dependencies
- Open questions

## Additional Files to Load
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): defines the required plan structure, validation expectations, and handoff sections for the output.
- [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md): provides the drafting shape for the execution-ready implementation plan.

## Workflow
1. Review the planning inputs.
   - Extract goals, scope, non-goals, requirements, acceptance criteria, and design constraints from the PRD and design inputs.
   - Identify missing details, ambiguity, and conflicts across the planning inputs.
   - Flag anything that blocks implementation planning.
2. Define the implementation approach.
   - Translate the approved design into an execution-oriented implementation approach.
   - Identify which parts of the system will change first and how the work should be staged.
   - Record execution assumptions, design-dependent decisions, and plan-level tradeoffs where they matter.
3. Break the work down.
   - Split the work into milestones, workstreams, or tasks.
   - Separate parallel work from sequential work.
   - Include testing, documentation, migration, and rollout work where needed.
4. Plan validation.
   - Map requirements and acceptance criteria to verification steps.
   - Identify unit, integration, end-to-end, and manual validation needs.
   - Define what must be true before the work is considered complete.
5. Sequence delivery.
   - Order the work based on dependencies and risk.
   - Call out prerequisites, blockers, and handoffs.
   - Define rollout phases if the change should ship incrementally.

## Data Structure
- Title
- Summary
- Source PRD
- Scope summary
- Assumptions and constraints
- Proposed technical approach
- Work breakdown
- Dependencies
- Risks
- Validation plan
- Rollout or migration plan
- Open questions

## Outputs
- A review-ready implementation plan
- An execution plan derived from the approved design inputs
- A scoped work breakdown tied to the PRD
- A list of dependencies, risks, and unresolved questions

## Done When
- The PRD and approved design inputs have been translated into actionable engineering work.
- The plan reflects applicable internal standards, canonical references, and existing repository patterns.
- Dependencies, sequencing, and validation are documented.
- Risks, assumptions, and open questions are visible.
- An engineer can begin execution without needing major missing context filled in verbally.
