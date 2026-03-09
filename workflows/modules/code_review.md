# Code Review Workflow

## Purpose
Use this workflow to evaluate a code change for correctness, risk, maintainability, and standards alignment, then summarize the resulting findings clearly.

## Use When
- A diff, branch, commit set, or pull request needs review.
- A change should be checked for regressions, standards alignment, or implementation risk before merge or handoff.
- A team needs a structured audit of a code change rather than new implementation work.

## Inputs
- Scoped review brief
- Code changes under review
- Relevant PRD, implementation plan, issue, or acceptance criteria
- Current-state context summary
- Internal standards and canonical references applied
- External guidance notes when needed
- Known risks, constraints, or review focus areas
- Open questions

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. Evaluate the change.
   - Check correctness, edge cases, failure handling, maintainability, and consistency with the intended design.
   - Review tests, validation strategy, and documentation updates relative to the change risk.
   - Distinguish confirmed issues from open questions or lower-confidence concerns.
2. Summarize findings.
   - Prioritize findings by severity and impact.
   - Tie findings to repository standards, code evidence, or authoritative guidance.
   - Record any follow-up validation or investigation that is still needed.

## Data Structure
- Review scope
- Review criteria
- Findings by severity
- Open questions
- Follow-up recommendations

## Outputs
- A structured review report for the change set
- A prioritized list of findings, risks, and open questions
- A short record of follow-up validation or investigation still needed

## Done When
- The change set has been reviewed against the requested behavior and repository standards.
- Findings are tied to code evidence, internal standards, or authoritative external guidance.
- The review clearly distinguishes confirmed issues, risks, and open questions.
