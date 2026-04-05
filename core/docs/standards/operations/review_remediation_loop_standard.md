---
id: "std.operations.review_remediation_loop"
title: "Review Remediation Loop Standard"
summary: "This standard defines the operating contract for seeded or fresh review-remediation loops, including baseline capture, original-review reruns, required Python-test proof, stop conditions, and closeout proof."
type: "standard"
status: "active"
tags:
  - "standard"
  - "operations"
  - "review_remediation"
owner: "repository_maintainer"
updated_at: "2026-04-05T02:10:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/docs/"
  - "pack_owned_docs"
  - "core/workflows/"
  - "pack_owned_workflows"
  - "core/control_plane/"
  - "core/python/"
aliases:
  - "review remediation"
  - "review remediation loop"
  - "fix loop"
  - "rerun until clean"
---

# Review Remediation Loop Standard

## Summary
This standard defines the operating contract for seeded or fresh review-remediation loops, including baseline capture, original-review reruns, required Python-test proof, stop conditions, and closeout proof.

## Purpose
- Prevent review-remediation work from stopping early while actionable findings still remain.
- Make dirty-worktree, multi-developer, and reusable-core ownership boundaries explicit before edits start.
- Ensure closeout distinguishes committed work, pre-existing dirty state, recurring findings, and unverified boundaries.
- Require the final clean signal to come from both code-boundary validation and a rerun of the starting review prompt, not from either proof path alone.

## Scope
- Applies to iterative review-remediation work that alternates findings, fixes, validation, and rerun review.
- Applies whether the loop starts from pasted findings, a saved report, current-context findings, or a fresh first-pass review.
- Does not replace narrower remediation, commit, or validation standards; it coordinates them for looped review repair.

## Use When
- A task says to fix findings and rerun the same review until the scope is clean.
- A prior review report, audit, or findings inventory should seed remediation instead of forcing another first-pass review.
- A repository is already dirty, shared with concurrent contributors, or split across canonical shared core and consuming-repo ownership.

## Related Standards and Sources
- [repository_maintenance_loop_standard.md](/core/docs/standards/operations/repository_maintenance_loop_standard.md): review-remediation loops are the stricter recurring-maintenance path when work starts from findings or requires rerun review.
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md): each loop iteration must still close against the relevant validation baseline.
- [git_workflow_standard.md](/core/docs/standards/engineering/git_workflow_standard.md): clean worktree or bounded-branch expectations constrain how a remediation loop should isolate concurrent changes.
- [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md): validated logical slices and explicit commit metadata should stay aligned with the loop ledger when commits are created.
- [review_remediation.md](/core/workflows/modules/review_remediation.md): defines how one remediation pass should repair findings in the owning surfaces.
- [review_remediation_loop.md](/core/workflows/modules/review_remediation_loop.md): operationalizes this standard for routed execution.
- [shared_core_refresh.md](/core/workflows/modules/shared_core_refresh.md): defines how reusable shared-core fixes land upstream in `WatchTowerCore/core` and sync back into another repository.
- [commit_closeout.md](/core/workflows/modules/commit_closeout.md): governs final commit creation when the loop includes commit closeout.

## Guidance
- Prefer explicit pasted findings or a cited saved report over paraphrase when a seeded loop is available.
- Keep one stable originating review identity through the loop. Do not silently swap review families midstream unless the prior selection was clearly wrong and the route mismatch is recorded.
- Before edits start, refresh the current state of the owning surfaces and recent local changes that could affect the remediation boundary.
- When the source repository is already dirty, destructive checks are likely, or concurrent contributors are active on the same owning surfaces, prefer a clean worktree or bounded branch instead of editing in the live dirty worktree.
- If the loop proceeds in a dirty worktree anyway, capture a baseline state before edits start and keep it in the iteration ledger:
  - current branch or worktree identity
  - chosen comparison ref for committed-delta reporting
  - `git status --short` or equivalent dirty-worktree snapshot
  - committed delta against the chosen comparison ref when git history is available
  - uncommitted delta against the current `HEAD`
- Normalize findings into stable issue families so recurring problems are tracked instead of duplicated blindly across iterations.
- Keep actionable findings, blocked findings, cleared observations, and unverified areas separate in the ledger.
- Fix findings in the owning surfaces, not only in the first files a review cited.
- When a loop starts in a repository other than `WatchTowerCore` and the remediation would modify any shared `core/` surface, land that change upstream in `WatchTowerCore/core` first. Do not close the recipient loop on a recipient-only `core/` patch.
- After the upstream `WatchTowerCore/core` fix is validated, bring it back into the initiating repository through the [shared_core_refresh.md](/core/workflows/modules/shared_core_refresh.md) workflow instead of reimplementing the same shared-core change locally.
- Commit by validated logical slice when commit creation is in scope. When commits are deferred, keep the slice boundary explicit enough for downstream closeout.
- Record the starting or original review prompt when it is available, not only the review family or route label. If a fresh loop begins from the current user request, preserve that request text or a tightly equivalent rerun prompt in the loop ledger.
- Re-run the same originating review prompt after the latest remediation pass before claiming the loop is clean, blocked, or iteration-capped. If the original prompt cannot be recovered safely, stop after one remediation pass with an explicit rerun boundary instead of guessing.
- When the remediated scope includes Python-bearing implementation or another repo-published unit/Python test boundary, rerun that unit/Python test surface after the latest remediation pass and keep its result separate from the review rerun.
- Do not classify a loop as clean unless both of these are true after the latest remediation pass:
  - the relevant unit/Python test gate ran and reported no failures or other open findings, when such a gate exists for the touched boundary
  - the rerun of the starting or original review prompt reported zero actionable findings
- Do not classify a loop as blocked while actionable findings still remain open. `blocked` means only blocked items or explicitly unverified boundaries remain after the latest rerun review.
- If either the required unit/Python test gate or the rerun review prompt still reports findings, keep iterating instead of collapsing that state into `clean` or `blocked`.
- When the same issue family recurs, identify whether the cause was an incomplete fix, weak validation, wrong ownership target, or insufficient review coverage, then strengthen the relevant validator, test, workflow, or standard instead of repeatedly patching symptoms.
- Closeout must distinguish:
  - findings fixed this iteration
  - recurring findings
  - blocked findings
  - unverified areas
  - committed delta since the chosen comparison ref
  - current uncommitted delta, including any pre-existing dirty baseline that was not part of the loop work
- Do not treat a large dirty worktree by itself as evidence that commit creation was skipped. Report committed and uncommitted deltas separately.
- When the loop runs in a temporary or bounded branch or worktree, closeout should include branch lifecycle handling. Delete the local branch or remove the temporary worktree once the branch is fully handed off, merged, or otherwise no longer needed. If branch cleanup is intentionally deferred for review or handoff, record that boundary explicitly.
- When the loop exposes weak prompt design, missing review coverage, or missing machine enforcement, record the improvement recommendation explicitly instead of treating the loop result as fully self-explanatory.

## Structure or Data Model
### Required loop controls
| Control | Requirement |
|---|---|
| Seed source | Identify whether the loop started from pasted findings, a saved report, current context, or a fresh first-pass review. |
| Originating review identity | Record the stable review route, workflow, or prompt used for reruns. |
| Originating review prompt | Preserve the starting or original review prompt text, or record the exact rerun-boundary reason when it cannot be recovered safely. |
| Baseline repo state | Record dirty-worktree and committed-delta context before edits when git metadata is available. |
| Python test gate | Record the relevant unit/Python test surface for the touched code boundary, or record that no such gate exists for the scoped work. |
| Iteration ledger | Track findings opened, findings closed, recurring findings, blocked findings, unverified areas, validations run, rerun-review outcomes, and slice or commit boundaries per pass. |
| Stop condition | Record whether the loop ended `clean`, `blocked`, `rerun-boundary`, `automation-boundary`, or `iteration-capped`. |
| Closeout proof | Distinguish committed delta, current uncommitted delta, and remaining risks explicitly. |

## Operationalization
- `Modes`: `workflow`; `documentation`; `validation`
- `Operational Surfaces`: `core/workflows/modules/review_remediation.md`; `core/workflows/modules/review_remediation_loop.md`; `core/workflows/modules/commit_closeout.md`; `core/docs/standards/operations/repository_maintenance_loop_standard.md`; `core/docs/standards/validations/repository_validation_standard.md`

## Validation
- Reviewers should reject loop closeout that does not identify the seed source, stable originating review family, and starting or original review prompt when that prompt was available.
- Reviewers should reject loop closeout in a dirty repository when baseline dirty-state and committed-versus-uncommitted proof are not separated clearly.
- Reviewers should reject `clean` loop status when the latest rerun review still reports actionable findings.
- Reviewers should reject `clean` loop status for Python-bearing scopes when the relevant unit/Python test gate was skipped, unavailable without explanation, or still reports failures or open findings.
- Reviewers should reject loop closeout that skips the rerun of the starting or original review prompt after the latest remediation pass unless the rerun boundary is explicit and justified.
- Reviewers should reject loop closeout that treats one green proof path as sufficient while the companion unit/Python test gate or rerun-review gate still reports findings.
- Reviewers should reject a non-`WatchTowerCore` loop that modifies shared `core/` only in the recipient repository instead of landing the shared fix upstream in `WatchTowerCore/core` and syncing it back with the shared-core refresh workflow.
- Reviewers should reject temporary-branch or temporary-worktree loop closeout that leaves branch-cleanup status implicit.
- Loop results should make recurring issue families and the chosen hardening response visible rather than treating recurrence as noise.

## Change Control
- Update this standard when the repository changes its expected review-remediation stop conditions, baseline-capture rules, or closeout proof requirements.
- Update the remediation workflows, maintenance-loop standard, and any companion closeout guidance in the same change set when this loop contract changes materially.

## References
- [repository_maintenance_loop_standard.md](/core/docs/standards/operations/repository_maintenance_loop_standard.md)
- [review_remediation.md](/core/workflows/modules/review_remediation.md)
- [review_remediation_loop.md](/core/workflows/modules/review_remediation_loop.md)
- [commit_closeout.md](/core/workflows/modules/commit_closeout.md)
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md)
- [git_workflow_standard.md](/core/docs/standards/engineering/git_workflow_standard.md)

## Updated At
- `2026-04-05T02:10:00Z`
