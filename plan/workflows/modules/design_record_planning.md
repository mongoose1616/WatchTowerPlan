# Design Record Planning Workflow

## Purpose
Use this workflow to define design options, recommend a technical design, and capture the guardrails that `design_record.md` must hand off to `implementation_slice.md`.

## Use When
- An initiative is defined well enough to start technical design but not yet ready for direct implementation slicing.
- The team needs a proposed solution shape, architecture impact assessment, and design tradeoff analysis for a scoped change.
- A change crosses multiple systems, introduces significant risk, or needs a reviewed design before work is broken into implementation tasks.

## Inputs
- Scoped design-record planning brief
- Initiative brief, issue, or planning brief
- Current-state context summary
- Foundation-context brief
- Internal standards and canonical references applied
- External guidance notes when needed
- Constraints, dependencies, and non-functional requirements
- Known risks, assumptions, or open questions

## Additional Files to Load
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md): defines the live initiative package split and keeps design work scoped between intake and execution surfaces.
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): defines the upstream and downstream trace links the design record should preserve.
- [decision_capture_standard.md](/plan/docs/standards/governance/decision_capture_standard.md): use when the design flow needs a durable decision note rather than silent rationale.

## Workflow
1. Confirm the upstream planning boundary.
   - Treat the approved or review-ready `initiative_brief.md` as the scope authority for design work.
   - If the brief is missing, contradictory, or lacks the acceptance or constraint boundary needed for design, return to initiative-brief authoring or clarification before continuing.
2. Define the viable design options and unresolved decisions.
   - Identify the credible implementation approaches and compare them in terms of correctness, complexity, maintainability, performance, security, and delivery risk at the level needed to explain the choice.
   - If a material architecture or governance tradeoff cannot be resolved inside the design flow, merge `decision_capture.md` instead of burying the decision in design prose.
3. Propose the recommended design.
   - Define the target architecture, major flow changes, interface changes, data impacts, migration concerns, and invariants the implementation must respect.
   - Identify the surfaces that will change and the failure cases or compatibility boundaries that implementation must preserve.
4. Prepare the exact implementation-slice handoff.
   - Capture the validation expectations, rollout constraints, dependencies, prerequisites, and settled design guardrails that `implementation_slice.md` must preserve.
   - Distinguish what is fixed by design from what implementation-slice planning may still choose.
5. Validate design-record readiness.
   - Confirm the design record stays at design level rather than collapsing into a task breakdown or execution log.
   - Confirm `implementation_slice_planning.md` can begin without reopening core design rationale or scope assumptions.

## Data Structure
- Source request and scope boundary
- Design goals and constraints
- Material options considered
- Recommended design and affected surfaces
- Design guardrails, risks, and optional handoff notes when needed

## Outputs
- A review-ready `design_record.md`
- A recommended technical approach for the scoped change
- Explicit downstream handoff inputs for `implementation_slice.md`

## Done When
- The scoped change has a clear recommended technical design.
- The design remains aligned with the repository foundations in `core/docs/foundations/`.
- The design reflects applicable internal standards, canonical references, and existing repository patterns.
- Major tradeoffs, dependencies, constraints, and implementation guardrails are documented.
- The implementation-slice handoff is explicit enough that execution planning can start without rediscovering the design boundary.
- The output is ready for implementation-slice planning without itself becoming an execution plan or task breakdown.
- The design avoids low-value execution detail or repeated metadata that belongs elsewhere.
