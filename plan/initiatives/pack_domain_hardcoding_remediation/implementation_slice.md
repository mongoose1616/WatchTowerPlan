# Pack Domain Hardcoding Remediation Implementation Slice

## Summary
Verify and remove remaining pack-domain hardcoding, reorganize lingering legacy artifacts, and prove the pack-driven endstate.

## Active Work Breakdown
- `task.pack_domain_hardcoding_remediation.pack_drive_runtime_roots_and_validation`: Remove the remaining shared-core default bias toward `plan/.wt` and make pack selection flow through discovered or explicit pack settings.
- `task.pack_domain_hardcoding_remediation.re_root_control_plane_and_governed_contracts`: Move shared-core control-plane assumptions to pack-declared workspace roots, validation suites, and registries.
- `task.pack_domain_hardcoding_remediation.recover_rich_human_docs_and_guidance`: Compare `main` for useful table and navigation patterns, then keep the current rich `plan/tracking/**` output where it already preserves that value.
- `task.pack_domain_hardcoding_remediation.run_assessment_pass_one`: Sweep active runtime, schemas, docs, standards, and tests for residue such as retired root `docs/` allowances or stale validation guidance.
- `task.pack_domain_hardcoding_remediation.run_assessment_pass_two`: Repeat the repository assessment after final validation and commit slicing to confirm there are no actionable residual gaps.
- `task.pack_domain_hardcoding_remediation.split_core_and_plan_python_boundary`: Complete the clean-endstate split by keeping reusable core under `watchtower_core` and plan-domain runtime under `plan/python/src/watchtower_plan/`.

## Additional Gaps Found During Execution
- Shared-core helper constructors were still reconstructing loaders from a hardcoded default token instead of a resolved effective pack path. This surfaced when trace purge exercised `PackWorkspacePaths` under a repo subset without a plan pack.
- Validation command docs still described `suite.watchtower_plan.validation_baseline` and the old fixture path `packs/plan/.wt/pack_settings.json`, even though the runtime now resolves pack defaults generically and fixture manifests live under `.wt/manifests/`.
- Two active schemas still permitted the retired root `docs/` family in Markdown path regexes. Those allowances were removed and added to the residue guard sweep.
- One integration contract test still asserted plan rendered surfaces against the old shared-core rendered-surface registry instead of the plan pack-owned registry. The test was updated to validate the current pack boundary rather than the retired core-owned assumption.
- The current Python package split was weaker than the endstate. The remaining work in this slice is to keep repo-local bootstrap and docs aligned now that the plan-owned boundary has landed.
- The mandate layer was part of that gap. `requirements.md`, `decisions.md`, and workspace READMEs now describe `watchtower_plan` as the approved plan-owned boundary and keep reusable core explicitly separate.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
