# Requirements And Decisions Adherence Remediation Decision Notes

## Summary
This remediation is a hard cutover. Root `docs/**` is retired completely, active planning terminology moves to the initiative-package model, and compatibility-only residue is removed rather than preserved.

## Decision Statements
- Retire root `docs/**` as an active documentation root.
- Make `core/docs/**` the canonical home for shared command docs, references, templates, and shared or core-owned standards.
- Make `plan/docs/**` the canonical home for durable plan-domain guidance and plan-owned standards.
- Keep duplication narrow: only the mirrored foundations corpus is mandatory by default.
- Treat the six-section `plan_overview.md` contract as authoritative.
- Replace active initiative projection phases with `capture`, `execution`, `closeout`, and `closed`.
- Remove the remaining PRD / feature-design / implementation-plan semantic layer instead of carrying renamed compatibility helpers.

## Why
- The current hybrid state keeps reintroducing authority confusion and documentation sprawl.
- Root `docs/**` contradicts the desired `core/**` and `plan/**` boundary.
- The current terminology mismatch hides the actual live initiative-package model behind stale route names, help text, and standards.
- `domain_packs` has historically returned because tests and fixtures recreated it without a hard regression guard.

## Follow-Through
- Update all active code, schemas, registries, indexes, tests, README surfaces, and help text in the same cutover.
- Allow historical `docs/**` mentions only in purge and migration ledgers.
- Add residue and `domain_packs` regression gates so the cutover fails closed if the old surfaces reappear.
