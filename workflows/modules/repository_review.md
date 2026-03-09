# Repository Review Workflow

## Purpose
Use this workflow to synthesize an existing repository review into prioritized findings, risks, and remediation guidance.

## Use When
- A repository review has already established review criteria, internal context, repository inventory, and assessment results.
- The active review needs prioritized findings, risks, and remediation guidance.
- A reviewer needs to turn a broad assessment into a durable review report.

## Inputs
- Scoped repository-review brief
- Review criteria and standards applied
- Internal standards and canonical references applied
- Repository inventory
- Repository assessment results
- External guidance notes when needed
- Open questions or unresolved uncertainties

## Workflow
1. Establish the final finding set.
   - Consolidate the inventory and assessment results into distinct findings, risks, and unknowns.
   - Separate confirmed facts from inferences and remaining open questions.
2. Prioritize findings and remediation.
   - Prioritize issues by severity, risk, and user or operational impact.
   - Convert major findings into concrete remediation tasks, owners, or next steps.
   - Distinguish adjacent same-change fixes from explicit deferred follow-up work.
3. Prepare the review report.
   - Summarize the review scope, standards applied, findings, and remediation plan in a durable report shape.
   - Ensure the report is clear enough that a later contributor can understand the review without replaying the full investigation.

## Data Structure
- Title
- Summary
- Review scope
- Review criteria and standards applied
- Repository inventory
- Findings by severity
- Coherence and consistency assessment
- Accuracy and freshness assessment
- Code quality and maintainability assessment
- Validation and test coverage assessment
- Security and operational readiness assessment
- Developer experience assessment
- Risks
- Recommended remediation plan
- Open questions

## Outputs
- A repository review report
- A prioritized list of findings and risks
- A remediation plan for the most important gaps

## Done When
- The repository review has been synthesized into a durable report.
- Findings are tied to explicit standards, clear reasoning, or primary-source guidance.
- Stale, inconsistent, risky, or unsupported areas are identified.
- The team has a prioritized path to bring the repository into a coherent and maintainable state.
