# Review Remediation Loop Workflow

## Purpose
Use this workflow to alternate seeded or fresh review findings with remediation passes until the chosen review comes back clean, only blocked, or explicitly iteration-capped.

## Use When
- The task says to fix findings and rerun the same review until the scope is clean.
- Existing findings already exist in pasted text, a saved report, or the current task context and should drive an iterative repair loop.
- A fresh review should begin the loop, then the same review family should keep verifying the repaired state after each remediation pass.

## Inputs
- Scoped review-remediation-loop request
- Either explicit seed findings or enough underlying review scope to select the right built-in review workflow
- Current repository state for the review and remediation surfaces in scope
- Governing standards, references, command docs, and canonical docs that constrain the selected review scope
- Any explicit iteration cap, commit intent, or blocked-scope boundaries already known

## Additional Files to Load
- [repository_maintenance_loop_standard.md](/core/docs/standards/operations/repository_maintenance_loop_standard.md): defines the recurring maintenance posture and review-remediation loop expectations for same-scope repair passes.

## Workflow
1. Determine the loop mode and stable originating review.
   - If explicit findings already exist in pasted text, a saved report, or current context, start in seeded-findings mode.
   - Otherwise, start in fresh-review mode and choose the narrowest matching built-in review route for the underlying scope using the authored routing surfaces or `watchtower-core route preview`.
   - Keep the originating review family stable across iterations. Do not silently swap code, documentation, workflow-system, or repository-review families mid-loop unless the prior choice is clearly wrong and the route mismatch is recorded.
2. Initialize the iteration ledger.
   - Record the loop mode, seed source, originating review route or workflow, iteration count, findings opened, findings closed, recurring findings, blocked findings, unverified areas, validations run, and slice or commit boundaries.
   - Normalize findings by stable issue family so recurring problems are tracked instead of duplicated blindly across iterations.
3. Create the current findings set.
   - In fresh-review mode, run the chosen built-in review workflow first and convert its findings into the loop ledger.
   - In seeded-findings mode, normalize the supplied findings into the same structure without forcing another first-pass review.
   - If the originating review identity cannot be recovered safely for a seeded loop, you may still run one remediation pass, but then stop with an explicit rerun boundary instead of guessing which review to rerun.
4. Run one remediation pass.
   - Apply the `review_remediation.md` workflow to the current actionable findings set.
   - Keep issue-family status, companion updates, validation needs, and slice boundaries current as the remediation progresses.
5. Re-run validation and the originating review.
   - Run the narrowest relevant checks after each logical remediation slice and the broader applicable validation baseline after the iteration-level fixes are complete.
   - Re-run the same originating review workflow against the updated repository state and treat recurring or newly introduced findings as first-class results.
6. Evaluate the stop conditions.
   - Stop clean when the rerun review returns zero actionable findings.
   - Stop blocked when only blocked or explicitly unverified items remain and those limits are explained clearly.
   - Stop at the automation boundary when the same unresolved issue families repeat without meaningful reduction across two consecutive reruns.
   - Stop iteration-capped when the task reaches the configured cap before the review is clean.
7. Prepare closeout and downstream use.
   - Record the final loop status, the latest validated state, residual issues, and the exact review family used for reruns.
   - If commit closeout is in scope, keep the iteration slices explicit and hand the result to the commit-closeout workflow rather than hiding commit decisions inside the loop.

## Data Structure
- Stable originating review identity and loop mode (`seeded_findings` or `fresh_review`)
- Iteration ledger with per-pass findings opened, findings closed, recurring findings, blocked findings, unverified areas, validations, and slice boundaries
- Current remediation ledger carried forward from each iteration's findings set
- Final loop status and residual issue register for blocked, capped, or still-unverified work

## Outputs
- A clean, blocked, rerun-boundary, or iteration-capped review-remediation result for the selected scope
- Iteration-by-iteration proof showing which findings were closed, which recurred, and which remained blocked or unverified
- Remediated owning surfaces plus the companion updates and validations needed to support the loop result
- An explicit closeout or slice boundary for any downstream commit handling

## Done When
- The selected review family has been rerun after the latest remediation pass and one of the stop conditions has been met explicitly.
- The loop ledger shows what changed in each iteration instead of leaving progress implicit.
- Residual blocked, capped, or unverified issues are explicit enough that the next contributor does not need to rediscover the loop boundary.
- The repaired state and its proof are clear enough for downstream closeout, further remediation, or a new scoped review.
