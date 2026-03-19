# Requirements And Decisions Adherence Remediation Implementation Slice

## Summary
Retire the root docs tree, finish the initiative-package hard cutover, and restore rich machine-backed documentation surfaces.

## Work Breakdown
1. Re-root active documentation families.
   - Move root command docs, references, templates, and shared or core-owned standards into `core/docs/**`.
   - Move plan-domain governance standards and durable plan guidance into `plan/docs/**`.
   - Remove root `docs/**`, plus the README and AGENTS guidance that still describe it as active.
2. Rework governed path contracts.
   - Update schema patterns, validator scopes, indexes, authority maps, loader assumptions, introspection constants, repository-path classification, and tests to the new documentation roots.
3. Enforce the `plan_overview.md` contract.
   - Align the rendered-surface registry, runtime renderer, tests, and live output to the six-section template and section schema.
   - Add fail-closed parity validation between templates, registries, and renderer payloads.
4. Finish the terminology and phase cutover.
   - Replace active PRD / feature-design / implementation-plan language with initiative brief / design record / implementation slice.
   - Replace `implementation_planning` and related stale phase terminology with `capture`, `execution`, `closeout`, and `closed`.
5. Replace retired planning semantics.
   - Remove the helper layer that still models PRDs and implementation plans as active documentation families.
   - Validate only the live initiative-package authored inputs.
6. Restore rich human rendering and harden guards.
   - Recover stronger Markdown structure, tables, and navigation from `main` where it fits the new model.
   - Add root-doc and `domain_packs` residue guards.
   - Run two repository assessment passes and close any remaining findings.

## Commit Slices
- `refactor(doc_roots): move command reference template and core standard families under core/docs`
- `refactor(plan_docs): move plan governance standards under plan/docs and remove root docs`
- `fix(plan_overview): enforce six-section overview contract and fail-closed parity checks`
- `docs(plan_bootstrap): rewrite bootstrap docs and active command guidance`
- `refactor(plan_terms): hard-cut route workflow schema and phase vocabulary`
- `refactor(plan_runtime): replace retired planning-document helpers and remove scaffold residue`
- `fix(plan_rendering): restore rich human trackers and migrated doc navigation`
- `test(plan_cutover): add residue guards domain_packs guards and full assessment proofs`

## Validation Plan
- Targeted command proofs:
  - `watchtower-core plan bootstrap --help`
  - `watchtower-core query coordination --format json`
  - `watchtower-core query initiatives --current-phase capture --format json`
  - `watchtower-core query initiatives --current-phase execution --format json`
  - `watchtower-core validate all --format json`
- Add and run fail-closed tests for:
  - `plan_overview` section parity
  - six-section rendered output
  - command-doc parity against the governed command index
  - initiative phase mapping
  - initiative-package authored-input semantics
  - non-creation of repo-root `domain_packs`
  - zero-tolerance residue checks for active root `docs/**`
- Run full validation after the functional slices and again after each assessment pass:
  - `uv run pytest -q`
  - `uv run watchtower-core validate all --format json`

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
