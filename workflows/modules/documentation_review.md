# Documentation Review Workflow

## Purpose
Use this workflow to evaluate documentation or standards for accuracy, structure, operationalization, and cross-surface coherence, then summarize evidence-backed findings clearly.

## Use When
- Existing documentation, standards, command pages, workflow docs, templates, or references need review.
- A documentation or standards audit should check for stale guidance, broken lookup paths, family-rule drift, or missing operationalization before edits are planned.
- The active task should keep reviewing the same documentation scope until repeated confirmation passes stop finding new actionable issues.

## Inputs
- Scoped documentation-review brief
- Documentation or standards files in scope plus the high-risk companion surfaces
- Current repository contents and behavior
- Internal standards, templates, and canonical references applied
- External guidance notes when needed
- Known risks, blind spots, or open questions

## Workflow
1. Build the review coverage map.
   - Identify the in-scope docs plus the companion templates, examples, command pages, references, indexes, validators, loaders, and query or sync surfaces that operationalize or expose them.
   - Record intentionally excluded surfaces and any remaining blind spots so the review boundary is explicit.
2. Inspect document quality and family compliance.
   - Check accuracy against the current repository state, document mode or classification, required sections, link targets, naming, structure, and mixed-purpose or stale content.
   - For standards, compare the document guidance to the examples, templates, and operational surfaces that are supposed to enforce it.
3. Check operationalization and cross-surface coherence.
   - Verify that related command docs, workflow docs, standards, templates, examples, validators, indexes, registries, and query or sync paths describe or enforce the same behavior.
   - If the main issue is implementation-versus-documentation drift or governed-artifact drift, add the dedicated reconciliation workflow instead of handling it only implicitly here.
4. Build the findings ledger.
   - Record findings by severity and confidence with document or artifact evidence, impacted readers or workflows, and the recommended next action.
   - Separate confirmed issues, intentional explicitness, open questions, and follow-up validation gaps.
5. Run a confirmation pass.
   - Re-review the highest-risk documents and their direct companion surfaces from a fresh angle for missed stale examples, lookup gaps, or enforcement mismatches.
   - If the active task is a same-scope review loop and a new actionable issue appears, add it to the findings ledger and repeat until a confirmation pass finds no new issues.

## Data Structure
- Review coverage map
- Review criteria and governing family rules
- Findings ledger by severity and confidence
- Operationalization and companion-surface gaps
- Open questions and follow-up recommendations

## Outputs
- A structured documentation or standards review report for the selected scope
- An explicit coverage boundary plus prioritized findings, risks, and open questions
- Follow-up refresh or reconciliation recommendations when they are still needed

## Done When
- The documents or standards in scope have been reviewed against current reality, governing family rules, and the high-risk companion surfaces in scope.
- Findings are tied to document, artifact, or implementation evidence plus the relevant governing standards or references.
- The review clearly distinguishes confirmed issues, intentional explicitness, broader risks, and open questions.
- A confirmation pass has finished and any remaining blind spots are explicit rather than hidden.
