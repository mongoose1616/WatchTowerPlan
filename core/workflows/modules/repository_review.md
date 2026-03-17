# Repository Review Workflow

## Purpose
Use this workflow to synthesize an existing repository review into evidence-backed findings, remediation guidance, and explicit stop-condition evidence.

## Use When
- A repository review has already established review criteria, internal context, repository inventory, and assessment results.
- The active review needs prioritized findings, risks, and remediation guidance.
- A reviewer needs to turn a broad assessment into a durable review report.

## Inputs
- Scoped repository-review brief
- Review criteria and standards applied
- Internal standards and canonical references applied
- Repository inventory and coverage map
- Repository assessment results
- External guidance notes when needed
- Open questions or unresolved uncertainties

## Workflow
1. Establish the review boundary and evidence basis.
   - Confirm the scope, coverage map, standards applied, and any remaining blind spots before synthesizing findings.
   - When the review continues a stable theme from earlier passes, keep one trace, one master findings ledger, and one closeout boundary instead of starting a new trace for each adjacent same-theme issue.
   - Separate confirmed facts, strong inferences, tentative concerns, and unresolved unknowns.
2. Build the findings ledger.
   - Consolidate the inventory and assessment results into distinct findings by category, severity, confidence, and affected surfaces.
   - Tie each finding to repository evidence, impacted workflows or users, and whether the issue is same-change repairable or explicit follow-up work.
3. Build the remediation sequence.
   - Prioritize issues by severity, repository risk, and user or operator impact.
   - Convert major findings into concrete remediation tasks, prerequisites, and non-recommended simplifications when a tempting refactor would violate foundations or governance.
4. Run a post-synthesis confirmation pass.
   - Re-check the highest-risk areas from a different angle, including direct dependencies, derived surfaces, and review boundaries that could still hide issues.
   - If the active review loop finds a new actionable issue inside the same scope, add it to the findings ledger and repeat the synthesis.
5. Prepare the durable review report.
   - Summarize the scope, standards applied, coverage boundary, findings, remediation plan, and confirmation-pass result in a shape a later contributor can use without replaying the investigation.

## Data Structure
- Review scope and coverage map
- Review criteria, standards, and foundations applied
- Findings ledger by severity, confidence, and category
- Systemic patterns and non-recommended simplifications
- Recommended remediation sequence
- Remaining blind spots or open questions
- Confirmation-pass results

## Outputs
- A durable repository review report
- A prioritized list of findings, risks, and systemic patterns
- A remediation plan plus explicit confirmation-pass or remaining-gap status

## Done When
- The repository review has been synthesized into a durable report.
- Findings are tied to explicit standards, clear reasoning, or primary-source guidance.
- Stale, inconsistent, risky, or unsupported areas are identified.
- The team has a prioritized path to bring the repository into a coherent and maintainable state.
- A confirmation pass has finished and either no new actionable issues remain in scope or the remaining gaps are explicit.
