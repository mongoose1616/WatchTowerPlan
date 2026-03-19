# Feature Design Planning Workflow

## Purpose
Use this workflow to define design options, recommend a technical design, and capture the guardrails that `design_record.md` must pass to `implementation_slice.md`.

## Use When
- A feature is defined well enough to start technical design but not yet ready for direct implementation.
- The team needs a proposed solution shape, architecture impact assessment, and design tradeoff analysis for a feature.
- A change crosses multiple systems, introduces significant risk, or needs a reviewed design before work is broken into implementation tasks.

## Inputs
- Scoped feature-design brief
- Feature request, initiative brief, issue, or planning brief
- Current-state context summary
- Foundation-context brief
- Internal standards and canonical references applied
- External guidance notes when needed
- Constraints, dependencies, and non-functional requirements
- Known risks, assumptions, or open questions

## Additional Files to Load
- [requirements.md](/requirements.md): defines the live initiative package model and the intended planning-to-execution boundary.
- [decisions.md](/decisions.md): locks the hard-cutover package shape and the execution-readiness gate.
- [decision_capture_standard.md](/plan/docs/standards/governance/decision_capture_standard.md): use when the design flow needs a durable decision note rather than silent rationale.

## Workflow
1. Define design options and tradeoffs.
   - Identify the viable implementation approaches.
   - Compare the options in terms of correctness, complexity, maintainability, performance, security, and delivery risk, but only at the level needed to explain the decision.
   - Record why an option is recommended or rejected when the tradeoff matters.
2. Propose the recommended design.
   - Define the target architecture, major flow changes, interface changes, and data impacts.
   - Identify the surfaces that will change and any migration or compatibility considerations.
   - Call out assumptions, invariants, and failure cases that the implementation must respect.
3. Define design guardrails and planning handoff needs.
   - Capture the validation expectations, rollout constraints, security considerations, and operational guardrails that the implementation must respect.
   - Identify dependencies, prerequisites, and unresolved decisions that implementation planning must account for.
   - Keep the output at design level rather than turning it into a task breakdown, execution log, or status memo.

## Data Structure
- Source request and scope boundary
- Design goals and constraints
- Material options considered
- Recommended design and affected surfaces
- Design guardrails, risks, and optional handoff notes when needed

## Outputs
- A review-ready `design_record.md`
- A recommended technical approach for the feature
- Implementation-planning handoff detail only when it adds non-obvious value

## Done When
- The feature has a clear recommended technical design.
- The design remains aligned with the repository foundations in `core/docs/foundations/`.
- The design reflects applicable internal standards, canonical references, and existing repository patterns.
- Major tradeoffs, dependencies, constraints, and implementation guardrails are documented.
- The output is ready for implementation planning without itself becoming an execution plan or task breakdown.
- The design avoids low-value execution detail or repeated metadata that belongs elsewhere.
