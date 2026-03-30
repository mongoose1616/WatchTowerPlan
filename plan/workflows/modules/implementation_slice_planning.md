# Implementation Slice Planning Workflow

## Purpose
Use this workflow to turn approved initiative inputs into an actionable `implementation_slice.md` with a work breakdown, validation strategy, and delivery sequence.

## Use When
- An initiative brief and design record are approved or mostly complete and engineering planning needs to begin.
- The team needs technical scope, sequencing, and dependencies before implementation.
- Work must be broken into concrete tasks, milestones, or workstreams.

## Inputs
- Scoped implementation-slice planning brief
- Approved or draft initiative brief
- Approved or draft design record, technical design, or architecture proposal
- Current-state context summary
- Internal standards and canonical references applied
- External guidance notes when needed
- Technical constraints
- Non-functional requirements
- Timeline or staffing assumptions
- Known dependencies
- Open questions

## Additional Files to Load
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md): defines the current plan-workspace structure and initiative package split that implementation-slice planning must respect.
- [task_tracking_standard.md](/plan/docs/standards/governance/task_tracking_standard.md): defines the live task authority that implementation-slice planning must hand off into.
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): defines the required upstream links from implementation slices into the traced planning chain.

## Workflow
1. Confirm the upstream planning boundary.
   - Use the initiative brief and design record together as the authoritative upstream input set for execution planning.
   - If either artifact is missing, materially incomplete, contradictory, or still depends on an unresolved architecture or policy choice, return to the upstream planning workflow or merge `decision_capture.md` before creating slices.
2. Define the execution-oriented implementation approach.
   - Translate the settled design into an implementation approach that names staging assumptions, design-dependent decisions, and system boundaries that affect execution order.
   - Identify which parts of the system should change first and why.
3. Break the work into actionable slices.
   - Split the work into milestones, workstreams, or tasks only at the level needed to guide execution without creating ceremony-only rows.
   - Separate sequential dependencies from safe parallel work and include testing, documentation, migration, or rollout work when they are real execution requirements.
4. Map slices to validation and done criteria.
   - Tie the work breakdown back to requirements, acceptance criteria, and risk.
   - Define the unit, integration, end-to-end, or manual validation needed for each major slice and what must be true before the slice is done.
5. Prepare the downstream task-management handoff.
   - Order the slices by dependency and risk and make explicit which work items `task_lifecycle_management.md` or `task_phase_transition.md` should create, preserve, or hand off.
   - If unresolved design ambiguity would cause churn in live task creation, escalate back to design planning or decision capture instead of pushing ambiguity into execution tasks.

## Data Structure
- Source design or request
- Scope summary and assumptions
- Proposed technical approach
- Work breakdown and validation plan
- Risks and optional dependencies, rollout notes, or open questions when material

## Outputs
- A review-ready `implementation_slice.md`
- An execution-oriented work breakdown tied to the design or initiative brief
- Explicit downstream handoff inputs for live task creation and phase transitions
- Explicit dependencies, risks, and unresolved questions only when they remain material

## Done When
- The initiative brief and approved design inputs have been translated into actionable engineering work.
- The plan reflects applicable internal standards, canonical references, and existing repository patterns.
- Dependencies, sequencing, and validation are documented.
- Risks, assumptions, and open questions are visible.
- An engineer can begin execution without needing major missing context filled in verbally.
- The task-management handoff is explicit enough that live tasks can be created or transitioned without rediscovering slice intent.
- The plan uses the smallest breakdown that still preserves execution clarity.
