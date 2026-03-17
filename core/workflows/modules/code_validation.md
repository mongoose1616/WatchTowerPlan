# Code Validation Workflow

## Purpose
Use this workflow to define, execute, and assess the validation needed for a code change or target surface.

## Use When
- A change needs verification through tests, linting, typechecking, build checks, QA, or targeted validation.
- A team wants confirmation that implemented behavior matches the request and does not introduce obvious regressions.
- A task requires structured validation rather than new implementation or broad repository review.

## Inputs
- Scoped validation brief
- Code changes or repository state to validate
- Relevant PRD, implementation plan, issue, or acceptance criteria
- Current-state context summary
- Internal standards and canonical references applied
- External guidance notes when needed
- Known risks, target environments, or validation constraints
- Open questions

## Workflow
1. Define the validation approach.
   - Select the checks needed for the task and its risk level.
   - Distinguish required validation from optional follow-up checks.
   - Keep the validation scoped to the requested change unless broader risk justifies expansion.
2. Execute validation.
   - Run the relevant automated and manual checks.
   - Capture failures, warnings, flaky behavior, and blocked checks clearly.
   - Re-run targeted checks when needed to confirm whether an issue is real.
3. Assess results.
   - Determine whether the change satisfies the requested behavior and repository standards.
   - Separate confirmed failures from environment issues, unknowns, or unverified areas.
   - Identify any remaining validation gaps that still matter for release or handoff.

## Data Structure
- Validation scope
- Validation criteria
- Validation approach
- Checks performed
- Findings or failures
- Validation gaps
- Follow-up recommendations

## Outputs
- A structured validation result for the change or target surface
- A list of checks performed and their outcomes
- A short record of validation gaps, blockers, or follow-up work

## Done When
- The requested validation has been completed or any blocked checks have been explicitly noted.
- The validation reflects applicable internal standards, canonical references, and existing repository patterns.
- The result clearly distinguishes passed checks, failures, unknowns, and remaining risks.
