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

## Additional Files to Load
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): defines what belongs in a durable repository decision and when this workflow should create one.
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md): defines the required decision-record structure and applied-reference capture.
- [decision_record_template.md](/home/j/WatchTowerPlan/docs/templates/decision_record_template.md): provides the drafting shape for the final decision document.

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
