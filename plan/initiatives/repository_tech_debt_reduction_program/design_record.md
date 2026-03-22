# Repository Tech Debt Reduction Program Design Record

## Summary
Makes tech-debt reduction the active repository priority, starting with legacy residue removal, integration-tail reduction, and stale compatibility cleanup across core, host, and pack-owned code.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/repository_tech_debt_reduction_program/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Recommended Design
- Run the program in ranked slices rather than one giant cleanup pass:
  1. inventory the debt
  2. remove the highest-cost residue
  3. rerun the repo gates
  4. repeat until the first tranche reaches a clear diminishing-return boundary
- Organize the first tranche around three debt families:
  - integration-test tail and redundant end-to-end coverage
  - stale compatibility or migration residue
  - duplicated registry or contract declarations that confuse the core-versus-pack authority boundary
- Keep the work deletion-biased. The best debt fix is usually to remove a surface entirely, not to document why it remains confusing.

## Debt Inventory Model
- Runtime and iteration debt
  - slow integration files
  - repeated full-workspace sync or closeout rebuilds inside tests
  - duplicated CLI-versus-service coverage
- Structural boundary debt
  - stale compatibility imports
  - barrel exports or migration shims that defeat newer boundaries
  - duplicated schema or validator declarations between `core` and `plan`
- Historical residue
  - migration-only helpers
  - retained but no-longer-governing edge-case tests
  - dead docs or machine surfaces that survive only because earlier cutovers were staged

## Design Constraints
- Do not reduce runtime by dropping the only contract-protecting test for a behavior family.
- Do not remove duplicated declarations until one authoritative owner is explicit.
- Prefer bounded file-family cleanup over cross-repo semantic churn.
- Keep every cleanup slice explainable in maintenance terms, not only aesthetics.

## Expected Deliverables
- One ranked debt inventory.
- One integration-tail reduction slice with updated suite guidance.
- One stale-compatibility and migration-residue reduction slice.
- One authority-surface reconciliation slice for duplicated registries or validators.
- One closeout summary that records deleted surfaces, retained surfaces, and recommended next debt work.
