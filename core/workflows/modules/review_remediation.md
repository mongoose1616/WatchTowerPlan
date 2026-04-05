# Review Remediation Workflow

## Purpose
Use this workflow to turn an existing review findings set into owning-surface fixes, aligned companion updates, and explicit validation proof without forcing a fresh broad review first.

## Use When
- Actionable findings already exist in pasted text, a saved report, or the current task context.
- A review report should be remediated in the owning surfaces rather than merely summarized.
- The task needs one focused remediation pass before a later handoff, commit-closeout step, or iterative re-review loop.

## Inputs
- Scoped remediation request
- Existing review findings, review report, or explicit current-context findings for the same repository scope
- Current repository state for the cited and analogous surfaces
- Governing standards, references, command docs, and canonical docs that constrain the affected surfaces
- Any explicit originating review route, task type, or workflow identity when it is already known

## Additional Files to Load
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md): defines the broad validation baseline that should close remediation work after issue-family fixes land.
- [git_commit_standard.md](/core/docs/standards/engineering/git_commit_standard.md): defines commit-slice and message expectations when the request explicitly includes commit creation or the active route later merges commit closeout.

## Workflow
1. Recover the seed findings set.
   - Prefer explicit pasted findings or a cited saved report over paraphrase.
   - If no pasted or file-backed findings exist but the current task context already carries explicit findings, normalize the latest relevant findings set instead of forcing a fresh review first.
   - If a finding is too summary-only to fix safely, reopen the cited surfaces until the issue can be restated with concrete paths, boundary evidence, or governing-surface references.
2. Normalize the findings into a remediation ledger.
   - Record one stable issue family for each materially distinct problem, with severity, confidence, ownership target, affected paths or surfaces, governing sources, observed evidence, why it matters, recommended remediation, validation needs, and likely slice boundary.
   - Merge findings only when the evidence, owning surface, remediation path, and validation story are genuinely the same.
   - Distinguish actionable findings from blocked items, explicit unknowns, and already-cleared observations instead of flattening them into one bucket.
3. Choose the owning repair surface and related update scope.
   - Fix each issue in the owning surface rather than only in the first file the review cited.
   - Search analogous surfaces for the same pattern and decide whether the issue is local, reusable, or cross-boundary before editing.
   - Decide whether each item is a canonical shared-core fix, repo-local core drift that must be reconciled, a pack-owned fix, a cross-boundary interoperability fix, a missing standard/reference/template/harness that must be authored, or a blocked item that cannot be fixed safely yet.
   - Shared `core/` defects belong in the canonical shared-core root, even when discovered while reviewing another repository. Do not land a shared-core fix only inside another repository's `core/`.
   - If the remediation is not being initiated from `WatchTowerCore` and the next repair slice would modify any shared `core/` surface, land that change upstream in `WatchTowerCore/core` first and then sync it back into the initiating repository through `shared_core_refresh.md`.
   - Treat non-`WatchTowerCore` `core/` trees as synchronized consumers of the canonical shared core, not as the first landing zone for shared-core edits.
   - Pack-specific behavior, docs, workflows, tests, machine state, and runtime wiring belong under the pack root.
   - Cross-boundary issues may touch both shared core and the pack root, but keep the pieces explicit and interoperable rather than blending them into one ambiguous change.
   - Expand the same-change scope when companion docs, tests, schemas, validators, indexes, or command surfaces would otherwise become stale.
4. Execute remediation by issue family.
   - Land the narrowest durable fix that removes the root cause instead of only patching the immediate symptom.
   - If a finding reveals a missing validator, test, standard, or authoring instruction, strengthen that surface in the same pass when it is part of the same behavior boundary.
   - Keep complete fixes, partial fixes, and blocked items explicit in the ledger as the work progresses.
   - Update all related surfaces in the same pass:
     - Documentation: command docs, standards, foundations docs, READMEs, overview docs, examples, naming guidance, and references.
     - Workflows: workflow docs, routing tables, workflow indexes, route previews, and workflow-adjacent guidance.
     - Tests: add or update tests for the corrected behavior, interoperability boundaries, and newly enforced constraints.
     - Validation/tooling: strengthen validators, checks, or automation where feasible to prevent recurrence.
     - Schemas/contracts: tighten JSON Schema, contract surfaces, or machine-readable authority when a finding reveals missing constraints or permissive structures.
     - Standards/references: publish missing standards or references when the repository relies on norms not actually documented in the owning docs surface.
     - Naming and style: synchronize naming conventions across runtime code, schemas, docs, workflows, tests, and command surfaces when one finding exposes drift.
     - Indexes/registries/rendered artifacts: refresh derived views, indexes, registries, manifests, and generated artifacts that depend on changed source surfaces.
5. Apply prevention and hardening.
   - If a finding exposes a standards gap, update the governing standard or machine-enforceable policy.
   - If a finding exposes a validator gap in shared reusable behavior, strengthen the canonical validator and then reconcile consuming repos as needed.
   - If a convention is only documented, add enforcement where practical rather than leaving it as prose-only guidance.
   - If a workflow, checklist, or review process allowed the issue to persist, update the relevant workflow or checklist to close that gap.
   - If existing tests or validators are missing, weak, or absent for a high-risk area, create the narrowest durable harness that proves the fix and can fail on regression.
   - If performance or maintainability problems are part of the finding, refactor enough to remove the root cause rather than applying a cosmetic patch.
6. Validate the repaired state.
   - Run the narrowest relevant checks after each issue family or logical slice, then run the broader applicable validation baseline for the touched surfaces.
   - Use the repository's documented sync/rebuild entrypoints after mutations that affect derived indexes, registries, manifests, or rendered views.
   - Run quality checks when the repository publishes them: `ruff check`, `ruff format --check`, `mypy`, `uv run pytest`, plus repo-native validation suites, schema checks, portability checks, export/bootstrap checks, or pack-specific validation commands relevant to the touched surfaces.
   - When the remediated scope includes Python-bearing implementation or another repo-published unit/Python test harness, run that unit/Python test surface explicitly and report its result separately instead of relying only on a broader aggregate validation command.
   - When the originating review targets a different repository and the remediation touches shared `core/`, validate those canonical slices first in `WatchTowerCore/core`. Do not treat unrelated consumer-pack validation failures as blockers for repo-external shared-core remediation.
   - When performance-sensitive code changes, run the available benchmark or comparative proof path. If no such harness exists, add a regression guard where practical and call out the remaining gap explicitly.
   - Separate confirmed passing proof from blocked checks, flaky results, environment limits, and still-unverified areas.
   - If a validation gap remains material, keep it open in the ledger instead of treating the remediation as fully closed.
7. Prepare closeout and downstream use.
   - If the task explicitly includes commit intent or the route later merges commit closeout, keep the remediation grouped into logical, reviewable slices and hand the result to the commit-closeout workflow.
   - Otherwise, keep the slice plan explicit enough that the next contributor can commit or continue the work without reconstructing the remediation logic from scratch.

## Data Structure
- Seed findings source and any originating review identity recovered from the request, saved report, or current context
- Remediation ledger keyed by stable issue family with severity, confidence, ownership target, evidence, affected surfaces, remediation status, and validation needs
- Same-change companion update map for docs, tests, validators, schemas, indexes, registries, or command surfaces touched by the remediation
- Logical slice or commit plan, including whether the current task is only preparing slices or also closing them out

## Outputs
- Remediated owning surfaces and same-change companion updates for the actionable findings in scope
- Validation results tied back to the remediated issue families
- An explicit remediation ledger showing fixed, partially fixed, blocked, cleared, and still-unverified findings
- A logical slice plan or commit-closeout-ready boundary when the task needs downstream commit handling

## Done When
- Every actionable finding in scope has been remediated or explicitly marked blocked with rationale.
- Owning surfaces and required companion surfaces no longer contradict the repaired state.
- The remediation has passing proof for the relevant checks or an explicit record of the remaining validation gap.
- The next contributor can see what was fixed, what remains open, and how the work should be sliced without replaying the entire investigation.
