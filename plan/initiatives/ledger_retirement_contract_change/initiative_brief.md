# Ledger Retirement Contract Change

## Summary
Retire remaining ledger-authority dependencies through one governed contract change without breaking validation, command, or documentation contracts.

## Identity
- `initiative_id`: `initiative.ledger_retirement_contract_change`
- `trace_id`: `trace.ledger_retirement_contract_change`
- `scope_type`: `pack_wide`

## Problem
- The repository still treats `ledger` as a first-class surface family even though the surviving machine artifacts are already modeled and consumed as retained records.
- `requirements.md`, standards, schema IDs, validator coverage, retention policy, runtime constants, purge flow, and retained artifact paths still encode `core/control_plane/ledgers/**` and `artifacts:ledgers:*` as active contract terms.
- That older taxonomy weakens clarity for both humans and machines because the repo now mixes `record` language in some surfaces with `ledger` language in others for the same retained-history families.

## Goals
- Replace the `ledger` surface family with retained `record` families under `core/control_plane/records/**`.
- Keep the current retained artifact families intact in purpose and coverage: migrations, releases, validation evidence, and trace-purge history.
- Update schema IDs, validator coverage, retention policy, runtime helpers, docs, and tests in one coherent change so the repository does not carry mixed terminology.
- Preserve behavior for validation recording, evidence queries, trace purge, and retained-history lookup while improving naming clarity.

## Non-Goals
- Do not remove retained validation, migration, release, or purge history from the repository.
- Do not redesign the evidence, purge, or retention model beyond the taxonomy and path cleanup needed to retire ledger terminology.
- Do not introduce a compatibility alias layer that keeps `ledgers/**` as an accepted long-term active root.
- Do not widen this tranche into unrelated lifecycle, release, or archive redesign work.

## Success Criteria
- No active schema, registry, runtime helper, command doc, standard, foundation, or test depends on `core/control_plane/ledgers/**` as the live canonical path.
- No active schema ID depends on the `artifacts:ledgers:*` namespace.
- The retained machine-history families load, validate, query, and purge through `record` terminology without behavioral regression.
- Full repository validation, sync, and test gates pass after the contract change lands.

## Planned Task Set
- `task.ledger_retirement_contract_change.bootstrap`
  Capture the initiative package, publish the chosen record-taxonomy direction, and move the package through confirmation and approval.
- `task.ledger_retirement_contract_change.migrate_control_plane_record_families`
  Move retained control-plane history from `core/control_plane/ledgers/**` to `core/control_plane/records/**` and update family READMEs plus retained JSON artifacts.
- `task.ledger_retirement_contract_change.update_contracts_and_registries`
  Replace ledger schema IDs, validator coverage, retention-policy terms, repository-path classifications, and related control-plane machine contracts with record terminology.
- `task.ledger_retirement_contract_change.refactor_runtime_and_cli`
  Align reusable-core and plan-pack runtime helpers, constants, query surfaces, purge flow, and CLI output with the new record taxonomy.
- `task.ledger_retirement_contract_change.refresh_governance_docs`
  Update requirements, decisions, standards, foundations, command pages, and mirrored docs so human guidance matches the new contract.
- `task.ledger_retirement_contract_change.validate_and_closeout`
  Rebuild derived surfaces, run the full validation and test gates, fix regressions, and leave the repo in a clean record-only state.

## Constraints
- Retained history remains governed under `core/control_plane/**`; the change is a taxonomy cleanup, not a relocation into `plan/.wt/**`.
- The final tree must remain fail-closed: no stale validator path, schema ID, or runtime constant may keep silently accepting the retired ledger contract.
- The duplicated foundations under `core/docs/foundations/**` and `plan/docs/foundations/**` must stay aligned when they mention retained machine history.
