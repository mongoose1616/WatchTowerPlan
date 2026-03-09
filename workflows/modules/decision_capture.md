# Decision Capture Workflow

## Purpose
Use this workflow to analyze viable options and record a durable repository decision with rationale, status, and downstream impacts.

## Use When
- A planning, design, architecture, governance, or standards decision needs a durable written record.
- Multiple options have been considered and the repository needs the chosen direction and rationale recorded clearly.
- A blocker, tradeoff, or policy choice must be resolved before downstream planning or implementation can proceed.

## Inputs
- Scoped decision brief
- Decision request, open question, or blocker
- Relevant PRD, feature design, implementation plan, review notes, or proposal materials
- Current-state context summary
- Internal standards and canonical references applied
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md)
- External guidance notes when needed
- Known options, constraints, assumptions, risks, and stakeholders

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. Define the viable options and tradeoffs.
   - Capture the credible options, including the option to defer or reject the change when relevant.
   - Compare them in terms of correctness, complexity, maintainability, policy fit, delivery risk, and downstream consequences.
   - Record why an option is recommended, rejected, or deferred when the tradeoff matters.
2. Record the decision outcome.
   - State the chosen outcome or the current recommendation clearly.
   - Capture the rationale, assumptions, and conditions that make the outcome valid.
   - Mark the status clearly, such as proposed, accepted, deferred, or rejected.
3. Record consequences and repository impacts.
   - Identify what standards, workflows, designs, plans, or implementation work must change because of the decision.
   - Distinguish immediate follow-up work from longer-term implications.
   - If the accepted outcome should become active repository policy, note which canonical artifacts must be updated so the decision does not live only in the decision record.

## Data Structure
- Title
- Decision statement
- Decision status
- Source request
- Affected surfaces
- Options considered
- Recommended or chosen outcome
- Rationale
- Consequences and follow-up impacts
- Dependencies
- Risks
- Open questions

## Outputs
- A durable decision record or decision recommendation
- A clear statement of the outcome, rationale, and status
- A list of affected artifacts, follow-up work, and unresolved questions

## Done When
- One decision has been captured clearly rather than blended with unrelated issues.
- The decision reflects applicable internal standards, canonical references, and existing repository patterns.
- The rationale, tradeoffs, and consequences are visible.
- The next artifacts or workflows affected by the decision are identified explicitly.
