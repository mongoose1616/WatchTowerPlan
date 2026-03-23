# Core Governance Reference Deplanification Followup

## Summary
Removes remaining unnecessary plan-owned governance and tracking references from shared core docs and standards while preserving true current-repo facts and explicit pack-owned boundaries.

## Identity
- `initiative_id`: `initiative.core_governance_reference_deplanification_followup`
- `trace_id`: `trace.core_governance_reference_deplanification_followup`
- `scope_type`: `pack_wide`

## Problem
Most high-impact shared-core portability issues identified by the `WatchTowerOversight` assessment are already fixed in reusable code, fixtures, and shared test boundaries. The remaining tail is documentation and standards drift inside `core/**`: several shared governance, metadata, workflow, and data-contract references still route operators through `plan/**` or plan-owned surfaces even when the rule is supposed to be generic reusable-core guidance.

That residue does not usually break `WatchTowerPlan` itself, but it still biases copied-core adoption toward donor behavior and makes future pack authors more likely to recreate plan-flavored layouts, references, and test assumptions.

## Desired Outcome
- Shared core governance and reference docs describe hosted-pack behavior generically by default.
- Remaining `plan/**` references in `core/**` are limited to true current-repository facts, required mirror contracts, or deliberate live-pack examples.
- Future contributors and agents can tell which docs are allowed to point at `plan/**` and which shared-core docs must stay pack-neutral.

## In Scope
- Shared authored docs under `core/docs/standards/**` and `core/docs/references/**` that still use `plan/**`, `plan/.wt/**`, `plan/tracking/**`, or plan-owned governance docs as generic operationalization.
- Companion shared README surfaces under `core/python/**` when they encode the same donor-style guidance.
- Required governed-index refreshes or validation follow-ups caused by the doc changes.

## Out Of Scope
- Rewriting shared foundations that intentionally describe the current `WatchTowerPlan` repository.
- Removing live `plan` facts from machine registries, indexes, or schema examples when they are correct for this repository.
- Changing `WatchTowerOversight/**` directly in this initiative.
- Reopening already-closed code portability slices unless a new doc change proves they are still wrong.

## Operator Requirements
- A copied `core/` tree must not direct new pack authors through plan-owned governance or tracking surfaces unless the point is explicitly about the current donor repository.
- Shared standards must use canonical repo-relative patterns or pack-neutral wording when the rule applies to hosted packs generally.
- The final shared-core doc set must still validate cleanly and remain understandable for the current `WatchTowerPlan` repo.

## Acceptance Criteria
- Touched shared core docs no longer operationalize generic rules through `plan/**` paths or plan-owned governance surfaces.
- Any remaining `plan` references in the touched shared-core docs are deliberate current-repo facts, required mirror paths, or explicitly labeled live-pack examples.
- `watchtower-core validate all --skip-acceptance --format json`, targeted `ruff`, and targeted pytest passes succeed after the cleanup.

## Non-Goals
- Proving zero textual `plan` references anywhere under `core/**`.
- Rewriting plan-owned docs or plan runtime code in this slice.
- Renaming the current live `plan` pack or removing valid repository-specific examples.

## Task Set
- `task.core_governance_reference_deplanification_followup.bootstrap_core_governance_reference_deplanification_followup`: Bootstrap, confirm, approve, and close the initiative package.
- `task.core_governance_reference_deplanification_followup.audit_remaining_shared_doc_plan_references`: Confirm which remaining `plan` references in shared core docs are still removable versus legitimate current-repo facts.
- `task.core_governance_reference_deplanification_followup.generalize_shared_governance_and_reference_docs`: Update shared standards, references, and README surfaces to use pack-neutral guidance where appropriate.
- `task.core_governance_reference_deplanification_followup.validate_and_closeout`: Refresh required derived surfaces, run validation, and close out the initiative with a clean committed state.
