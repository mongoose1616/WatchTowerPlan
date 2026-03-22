# Ledger Retirement Contract Change Implementation Slice

## Summary
Retire remaining ledger-authority dependencies through one governed contract change without breaking validation, command, or documentation contracts.

## Work Breakdown
- `task.ledger_retirement_contract_change.bootstrap`
  Author the initiative package, confirm inputs into machine state, and approve the package for execution.
- `task.ledger_retirement_contract_change.migrate_control_plane_record_families`
  Move `core/control_plane/ledgers/` to `core/control_plane/records/`, refresh the family READMEs, and update the retained JSON artifacts to their new canonical paths and schema IDs.
- `task.ledger_retirement_contract_change.update_contracts_and_registries`
  Update artifact schemas, schema catalog, validator registry, retention-policy registry, repository-path classification, and any machine-readable contract that still encodes ledger terminology.
- `task.ledger_retirement_contract_change.refactor_runtime_and_cli`
  Rename path constants and purge/evidence helper terminology, align query and validation handlers, and keep record loading plus trace purge behavior stable.
- `task.ledger_retirement_contract_change.refresh_governance_docs`
  Refresh requirements, decisions, standards, command pages, foundations, mirrors, READMEs, and AGENTS files where the durable contract still says ledger.
- `task.ledger_retirement_contract_change.validate_and_closeout`
  Rebuild derived surfaces, run targeted regressions plus the full repo gate, fix any residue, and leave no active ledger contract behind.

## Acceptance Focus
- Retained machine-history surfaces are canonical under `core/control_plane/records/**`.
- Schema validation, evidence recording, evidence querying, and trace purge operate against record schema IDs and record roots only.
- Governance docs, control-plane inventory, and machine registries all describe the same retained-history taxonomy.
- No active runtime, validator, or human guidance surface still depends on `ledger` as an accepted contract term.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
