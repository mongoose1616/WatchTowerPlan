# Code Review Workflow

## Purpose
Use this workflow to evaluate a code change for correctness, regression risk, maintainability, standards alignment, and review completeness, then summarize evidence-backed findings clearly.

## Use When
- A diff, branch, commit set, or pull request needs review.
- A change should be checked for regressions, standards alignment, or implementation risk before merge or handoff.
- A team needs a structured audit of a code change rather than new implementation work.
- The active task should keep reviewing the same code scope until repeated confirmation passes stop finding new actionable issues.

## Inputs
- Scoped review brief
- Code changes under review plus the touched and high-risk adjacent surfaces
- Relevant PRD, implementation plan, issue, or acceptance criteria
- Current-state context summary
- Internal standards and canonical references applied
- External guidance notes when needed
- Known risks, constraints, or review focus areas
- Open questions or known blind spots

## Workflow
1. Build the review coverage map.
   - Identify the touched files, direct dependencies, direct consumers, public interfaces, data or state boundaries, config or migration surfaces, and companion docs or tests that could change behavior.
   - Record what is intentionally out of scope or still unknown so the review does not hide blind spots.
2. Inspect behavior and failure modes.
   - Check requested behavior, invariants, edge cases, failure handling, compatibility, state transitions, concurrency, security, and performance where they are relevant to the change.
   - Compare the implementation shape to the intended design and established local patterns.
3. Check validation and companion surfaces.
   - Review tests, negative coverage, validation strategy, fixtures, and release-risk controls relative to the change risk.
   - Check whether docs, configs, schemas, examples, migrations, or operational guidance were updated when the code change makes them part of the behavior boundary.
4. Build the findings ledger.
   - Record findings by severity and confidence with file or code evidence, impacted scenarios, and the recommended next action.
   - Separate confirmed bugs, broader risks, intentional tradeoffs, open questions, and follow-up validation gaps.
5. Run a confirmation pass.
   - Re-check the highest-risk paths from a different angle, focusing on touched files, unchanged code that can be broken indirectly, and any surfaces the first pass nearly skipped.
   - If the active task is a same-scope review loop and a new actionable issue appears, add it to the findings ledger and repeat until a confirmation pass finds no new issues.

## Data Structure
- Review coverage map
- Review criteria and risk areas
- Findings ledger by severity and confidence
- Validation and companion-surface gaps
- Open questions and follow-up recommendations

## Outputs
- A structured code-review report for the change set
- An explicit coverage boundary plus prioritized findings, risks, and open questions
- Follow-up validation or remediation recommendations when they are still needed

## Done When
- The change set has been reviewed against the requested behavior, repository standards, and the high-risk adjacent surfaces in scope.
- Findings are tied to code evidence, internal standards, or authoritative external guidance.
- The review clearly distinguishes confirmed issues, broader risks, intentional tradeoffs, and open questions.
- A confirmation pass has finished and any remaining blind spots are explicit rather than hidden.
