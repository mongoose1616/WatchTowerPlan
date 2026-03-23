# Core Governance Reference Deplanification Followup Design Record

## Summary
Removes remaining unnecessary plan-owned governance and tracking references from shared core docs and standards while preserving true current-repo facts and explicit pack-owned boundaries.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/core_governance_reference_deplanification_followup/.wt/`.
- The implementation boundary is shared core documentation and companion validation surfaces, not plan runtime code.
- The purpose is to improve copied-core portability and future pack authoring guidance without falsifying the current donor repository.

## Architecture
### Shared-Doc Classification
- Keep shared-core references that describe the actual repository as it exists today, such as the authored foundations source in `core/docs/foundations/**` and its required mirror in `plan/docs/foundations/**`.
- Generalize references that only use `plan/**` as an accidental donor example for reusable behavior.
- When a shared doc needs an example path, prefer canonical hosted-pack forms such as `<pack>/docs/...`, `<pack>/.wt/...`, `*/docs/standards/...`, or `*/tracking/...`.

### Documentation Contract
- Shared-core governance docs should point to shared-core standards or neutral hosted-pack patterns unless a plan-owned dependency is intentional.
- Shared-core references should not require readers to open plan-owned governance docs to understand generic reusable-core behavior.
- If a touched doc feeds a governed index or validation rule, the derived machine-readable surfaces must be refreshed in the same change set.

### Validation Strategy
- Use targeted grep and file review to classify remaining `plan` references before editing.
- Run targeted validation for the touched doc families first.
- Run broad repository validation afterward to confirm no index, front-matter, or semantic drift remains.
