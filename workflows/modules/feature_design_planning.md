# Feature Design Planning Workflow

## Purpose
Use this workflow to define design options, recommend a technical design, and capture the guardrails that implementation planning must inherit.

## Use When
- A feature is defined well enough to start technical design but not yet ready for direct implementation.
- The team needs a proposed solution shape, architecture impact assessment, and design tradeoff analysis for a feature.
- A change crosses multiple systems, introduces significant risk, or needs a reviewed design before work is broken into implementation tasks.

## Inputs
- Scoped feature-design brief
- Feature request, PRD, issue, or planning brief
- Current-state context summary
- Foundation-context brief
- Internal standards and canonical references applied
- External guidance notes when needed
- Constraints, dependencies, and non-functional requirements
- Known risks, assumptions, or open questions

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. Define design options and tradeoffs.
   - Identify the viable implementation approaches.
   - Compare the options in terms of correctness, complexity, maintainability, performance, security, and delivery risk.
   - Record why an option is recommended or rejected when the tradeoff matters.
2. Propose the recommended design.
   - Define the target architecture, major flow changes, interface changes, and data impacts.
   - Identify the surfaces that will change and any migration or compatibility considerations.
   - Call out assumptions, invariants, and failure cases that the implementation must respect.
3. Define design guardrails and planning handoff needs.
   - Capture the validation expectations, rollout constraints, security considerations, and operational guardrails that the implementation must respect.
   - Identify dependencies, prerequisites, and unresolved decisions that implementation planning must account for.
   - Keep the output at design level rather than turning it into a task breakdown.

## Data Structure
- Title
- Summary
- Source request
- Scope and feature boundary
- Design goals and constraints
- Options considered
- Recommended design
- Affected surfaces
- Design guardrails
- Implementation-planning handoff notes
- Dependencies
- Risks
- Open questions

## Outputs
- A review-ready feature design
- A recommended technical approach for the feature
- A clear handoff package for implementation planning
- A list of risks, dependencies, and unresolved questions

## Done When
- The feature has a clear recommended technical design.
- The design remains aligned with the repository foundations in `docs/foundations/`.
- The design reflects applicable internal standards, canonical references, and existing repository patterns.
- Major tradeoffs, dependencies, constraints, and implementation guardrails are documented.
- The output is ready for implementation planning without itself becoming an execution plan or task breakdown.
