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
- [review_remediation_loop_standard.md](/core/docs/standards/operations/review_remediation_loop_standard.md): defines the stricter loop contract for baseline capture, rerun discipline, stop conditions, and closeout proof.

## Workflow
1. Determine the loop mode and stable originating review.
   - If explicit findings already exist in pasted text, a saved report, or current context, start in seeded-findings mode.
   - Otherwise, start in fresh-review mode and choose the narrowest matching built-in review route for the underlying scope using the authored routing surfaces or `watchtower-core route preview`.
   - Keep the originating review family stable across iterations. Do not silently swap code, documentation, workflow-system, or repository-review families mid-loop unless the prior choice is clearly wrong and the route mismatch is recorded.
2. Initialize the iteration ledger and current-state baseline.
   - Record the loop mode, seed source, originating review route or workflow, iteration count, findings opened, findings closed, recurring findings, blocked findings, unverified areas, validations run, and slice or commit boundaries.
   - Normalize findings by stable issue family so recurring problems are tracked instead of duplicated blindly across iterations.
   - Refresh the current state of the likely owning surfaces and recent local changes before editing.
   - When the repository is already dirty, concurrent contributors are active on the same surfaces, or destructive checks are likely, prefer a clean worktree or bounded branch for the remediation loop instead of editing in the live dirty worktree.
   - If the loop proceeds in a dirty worktree, capture the baseline dirty state and chosen comparison ref before edits so later closeout can separate pre-existing worktree dirt from the loop's committed and uncommitted changes.
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
   - Do not classify the loop as `clean` or `blocked` until the latest remediation pass has been followed by the rerun review or an explicit rerun boundary.
   - When findings recur, decide whether the recurrence came from an incomplete fix, weak validation, wrong ownership target, or insufficient review coverage, then strengthen that surface in the next slice instead of only repatching the symptom.
6. Evaluate the stop conditions.
   - Stop clean when the rerun review returns zero actionable findings.
   - Stop blocked when only blocked or explicitly unverified items remain and those limits are explained clearly.
   - Stop at the automation boundary when the same unresolved issue families repeat without meaningful reduction across two consecutive reruns.
   - Stop iteration-capped when the task reaches the configured cap before the review is clean.
7. Prepare closeout and downstream use.
   - Record the final loop status, the latest validated state, residual issues, and the exact review family used for reruns.
   - Distinguish findings fixed this iteration, recurring findings, blocked findings, and unverified areas instead of collapsing them into one residual bucket.
   - When git metadata is available, report committed delta against the chosen comparison ref separately from the current uncommitted delta so a dirty worktree cannot be mistaken for missing commits.
   - If commit closeout is in scope, keep the iteration slices explicit and hand the result to the commit-closeout workflow rather than hiding commit decisions inside the loop.
   - If the loop used a temporary or bounded branch or a temporary worktree, either clean it up when the branch is complete or record why cleanup is deferred for later handoff, review, or merge.
   - Record any recommendation to strengthen the review prompt, workflow, validator, or harness when the loop exposed a process weakness rather than only a code defect.

## Data Structure
- Stable originating review identity and loop mode (`seeded_findings` or `fresh_review`)
- Iteration ledger with per-pass findings opened, findings closed, recurring findings, blocked findings, unverified areas, validations, and slice boundaries
- Baseline repository-state record for dirty-worktree and committed-delta reporting when git metadata is available
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
- Dirty-worktree baseline, committed delta, and current uncommitted delta are separated clearly when the repository was not clean at loop start.
- Temporary branch or worktree cleanup status is explicit when the loop used one.
- Residual blocked, capped, or unverified issues are explicit enough that the next contributor does not need to rediscover the loop boundary.
- The repaired state and its proof are clear enough for downstream closeout, further remediation, or a new scoped review.
