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
- [requirements.md](/requirements.md): defines the capture-first execution gate and expected plan workspace structure.
- [decisions.md](/decisions.md): locks the initiative and task lifecycle rules that implementation-slice planning must respect.
- [task_tracking_standard.md](/plan/docs/standards/governance/task_tracking_standard.md): defines the live task authority that implementation-slice planning must hand off into.

## Workflow
1. Review the planning inputs.
   - Extract goals, scope, non-goals, requirements, acceptance criteria, and design constraints from the initiative brief and design inputs.
   - Identify missing details, ambiguity, and conflicts across the planning inputs.
   - Flag anything that blocks implementation-slice planning.
2. Define the implementation approach.
   - Translate the approved design into an execution-oriented implementation approach.
   - Identify which parts of the system will change first and how the work should be staged.
   - Record execution assumptions, design-dependent decisions, and plan-level tradeoffs where they matter.
3. Break the work down.
   - Split the work into milestones, workstreams, or tasks only at the level needed to guide execution.
   - Separate parallel work from sequential work.
   - Include testing, documentation, migration, and rollout work where needed, but do not create ceremony-only breakdown rows.
4. Plan validation.
   - Map requirements and acceptance criteria to verification steps.
   - Identify unit, integration, end-to-end, and manual validation needs proportionally to the risk and scope.
   - Define what must be true before the work is considered complete.
5. Sequence delivery.
   - Order the work based on dependencies and risk.
   - Call out prerequisites, blockers, and handoffs.
   - Define rollout phases only when the change should ship incrementally or migration timing materially matters.

## Data Structure
- Source design or request
- Scope summary and assumptions
- Proposed technical approach
- Work breakdown and validation plan
- Risks and optional dependencies, rollout notes, or open questions when material

## Outputs
- A review-ready `implementation_slice.md`
- An execution-oriented work breakdown tied to the design or initiative brief
- Explicit dependencies, risks, and unresolved questions only when they remain material

## Done When
- The initiative brief and approved design inputs have been translated into actionable engineering work.
- The plan reflects applicable internal standards, canonical references, and existing repository patterns.
- Dependencies, sequencing, and validation are documented.
- Risks, assumptions, and open questions are visible.
- An engineer can begin execution without needing major missing context filled in verbally.
- The plan uses the smallest breakdown that still preserves execution clarity.
