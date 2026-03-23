# Core Governance Reference Deplanification Followup Implementation Slice

## Summary
Removes remaining unnecessary plan-owned governance and tracking references from shared core docs and standards while preserving true current-repo facts and explicit pack-owned boundaries.

## Work Breakdown
- `task.core_governance_reference_deplanification_followup.bootstrap_core_governance_reference_deplanification_followup`
  - confirm authored inputs
  - approve the package
  - close the bootstrap task once execution is ready
- `task.core_governance_reference_deplanification_followup.audit_remaining_shared_doc_plan_references`
  - review the Oversight assessment again as a portability oracle
  - classify remaining `plan` references in shared core docs as removable versus legitimate current-repo facts
  - narrow the edit set to only the reusable shared-core docs that still encode donor-style operationalization
- `task.core_governance_reference_deplanification_followup.generalize_shared_governance_and_reference_docs`
  - rewrite the targeted shared standards and references to use pack-neutral language and canonical repo-relative patterns
  - update companion shared README guidance when it repeats the same donor-style assumptions
  - refresh any derived indexes or machine-readable surfaces required by the changed docs
- `task.core_governance_reference_deplanification_followup.validate_and_closeout`
  - run targeted validation first
  - run broad validation second
  - close and commit the initiative once the worktree is clean

## Commit Boundaries
- Commit 1: shared governance/reference doc generalization plus any directly coupled README updates
- Commit 2: validation-only or closeout adjustments if needed

## Validation Commands
- `./core/python/.venv/bin/watchtower-core validate front-matter --path core/docs/standards --format json`
- `./core/python/.venv/bin/watchtower-core validate document-semantics --path core/docs/standards --format json`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
- `cd core/python && ./.venv/bin/ruff check tests`
- `cd core/python && ./.venv/bin/python -m pytest tests/integration/test_control_plane_loader_and_foundation_contracts.py tests/integration/test_endstate_cutover_guards.py -q`

## Closeout Criteria
- touched shared-core docs no longer encode removable donor-style `plan/**` operationalization
- remaining `plan` references in the touched files are deliberate and justified as current-repo facts or explicit live-pack examples
- repo coordination returns to `ready_for_bootstrap`
- the worktree is clean after commit

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
