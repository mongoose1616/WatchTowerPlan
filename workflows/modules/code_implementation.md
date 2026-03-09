# Code Implementation Workflow

## Purpose
Use this workflow to define the implementation approach and apply the requested code change while keeping the affected repository surfaces coherent.

## Use When
- A feature, fix, refactor, or behavior change needs to be implemented.
- Existing code must be changed to satisfy a PRD, plan, issue, or bug report.
- A task requires code changes plus the adjacent tests, docs, or configuration updates needed to keep the repository coherent.

## Inputs
- Scoped implementation brief
- Relevant PRD, implementation plan, issue, or acceptance criteria
- Current-state context summary
- Internal standards and canonical references applied
- External guidance notes when needed
- Technical constraints and non-functional requirements
- Open questions

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. Define the implementation approach.
   - Decide how the change will be introduced before editing.
   - Keep the scope aligned with the request and avoid unrelated cleanup.
   - Call out tradeoffs or risks when they affect correctness or maintainability.
2. Implement the change.
   - Modify the relevant code, tests, docs, configs, or schemas needed for a coherent result.
   - Keep related surfaces synchronized when the change affects a governed source of truth.
   - Follow existing repository patterns unless there is a clear reason to change them.

## Data Structure
- Change summary
- Implementation approach
- Affected surfaces
- Open questions or implementation risks

## Outputs
- A code change aligned with the request and repository standards
- Updated adjacent surfaces when needed to keep the change coherent
- A short record of the implementation approach and affected surfaces

## Done When
- The requested code change has been implemented.
- The implementation reflects applicable internal standards, canonical references, and existing repository patterns.
- Related tests, docs, configs, or other affected surfaces have been updated when needed.
