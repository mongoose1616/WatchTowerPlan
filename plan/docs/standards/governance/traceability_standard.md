---
id: "std.governance.traceability"
title: "Traceability Standard"
summary: "This standard defines the repository's baseline traceability model so initiative intent, decisions, designs, implementation slices, and later executable or validation surfaces can be linked end to end."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "traceability"
owner: "repository_maintainer"
updated_at: "2026-03-20T23:55:00Z"
audience: "shared"
authority: "authoritative"
---

# Traceability Standard

## Summary
This standard defines the repository's baseline traceability model so initiative intent, decisions, designs, implementation slices, and later executable or validation surfaces can be linked end to end.

## Purpose
- Keep important repository changes reviewable as they move from request through design and implementation.
- Prevent requirements, decisions, and design rationale from becoming disconnected from downstream implementation work.
- Establish a minimal shared trace model before Python query and validation tooling begins to depend on it.

## Scope
- Applies to durable planning and governance artifacts such as initiative briefs, decision notes, design records, implementation slices, task records, and their machine-readable indexes.
- Applies to acceptance contracts, validation-evidence artifacts, and the unified traceability index when those families participate in a traced initiative.
- Applies to derived initiative coordination views when they project from traceability and current planning or task state.
- Defines the baseline trace chain, required identifiers, and synchronization expectations across human-readable and machine-readable tracking surfaces.

## Use When
- Creating or updating initiative briefs, decision notes, design records, or implementation slices.
- Adding machine-readable tracking indexes for planning or governance artifacts.
- Reviewing whether a repository change leaves an important upstream or downstream trace link implicit.

## Related Standards and Sources
- [naming_and_ids_standard.md](/core/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [status_tracking_standard.md](/plan/docs/standards/data_contracts/status_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [acceptance_contract_standard.md](/plan/docs/standards/data_contracts/acceptance_contract_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [validation_evidence_standard.md](/plan/docs/standards/data_contracts/validation_evidence_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_index_standard.md](/plan/docs/standards/data_contracts/traceability_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [initiative_closeout_standard.md](/plan/docs/standards/governance/initiative_closeout_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md): companion standard that constrains when closed trace-local artifacts remain retained history versus becoming purge-eligible.

## Guidance
- Use one shared `trace_id` to tie the artifacts of a single initiative, feature, or change boundary together.
- Use explicit identifiers for durable planning artifacts instead of relying only on filenames or titles.
- Prefer readable semantic `trace_id` values over adding a second opaque UUID layer for normal repository traceability.
- Treat traceability as both a human-readable and machine-readable concern:
  - human-readable trackers summarize the current corpus
  - machine-readable indexes provide stable lookup surfaces for tooling
- The baseline end-to-end trace chain is:
  - request or initiative brief
  - decision note when a durable choice is required
  - design record
  - implementation slice
  - task record when work is decomposed into engineer-sized execution items
  - implementation surface, command surface, validator surface, or other executable artifact
  - acceptance contract when acceptance must be machine-loaded explicitly
  - validation evidence
  - closeout artifacts when that family is established
- Use the unified traceability index as the machine-readable join layer for the full traced chain.
- Use the traceability index plus the live initiative and task indexes as the preferred deep machine join when the question needs linked planning, task, acceptance, and evidence context.
- Use the initiative index and initiative tracker as derived coordination rendered surfaces over the traceability layer plus current planning and task state.
- Use the authority map when you need to resolve whether traceability or another planning surface is canonical for a recurring lookup question.
- Keep family-specific human trackers active-first by default. Route terminal trace browsing to explicit initiative or trace query surfaces instead of inlining the full closed trace corpus in every tracker.
- Do not treat retained closed trace packages as the enduring source of current policy when equivalent standards, current initiative-package authored docs, or machine-readable authority surfaces already exist.
- If a closed trace is later purged under the planning retention standard, remove stale canonical references to its trace-local paths and keep only the surviving authority surfaces plus the minimal purge record.
- Use `initiative_status` on the traceability entry for initiative outcome instead of overloading artifact lifecycle `status`.
- Treat initiative closeout metadata as a meaningful traceability change; when terminal closeout is recorded, effective `updated_at` should be at least `closed_at`.
- Keep family-specific indexes as their local lookup surfaces and keep them aligned with the unified traceability index.
- An initiative package should publish:
  - a shared `trace_id`
  - a stable `initiative_id`
  - stable requirement identifiers where the requirement list is durable
  - stable acceptance identifiers where acceptance criteria are durable
- A decision note should publish:
  - a shared `trace_id`
  - a stable `decision_id`
  - a decision-outcome status such as `proposed`, `accepted`, `deferred`, `rejected`, or `superseded`
  - explicit links to affected initiative briefs, design records, implementation slices, or repository paths when they exist
- Design records and implementation slices should preserve their upstream links rather than forcing later readers to infer them from prose.
- Acceptance contracts should preserve source `acceptance_id` values from the initiative acceptance source rather than inventing alternate identifiers.
- Validation-evidence artifacts should publish the validators, acceptance items, and subject surfaces they cover when those are known.
- Task records should publish `trace_id` when they belong to a traced initiative and should preserve task-to-task dependencies explicitly.
- Active traced initiatives should not remain active without linked task records.
- Machine-readable indexes for initiative packages, task records, acceptance contracts, validation evidence, and traceability joins should carry `trace_id` explicitly so tooling can join related artifacts without parsing prose.
- Add UUIDs only when an external integration requires them as external identifiers; do not treat them as the default local join key when `trace_id` already exists.
- Update trackers and indexes in the same change set when a traced planning artifact is added, renamed, removed, or materially retargeted.
- Prefer a missing-link follow-up note over silent omission when a downstream artifact cannot yet point back to its upstream planning source.

## Structure or Data Model
### Baseline identifier families
| Identifier Kind | Expected Prefix | Example |
|---|---|---|
| Shared trace | `trace.` | `trace.governed_acceptance_example` |
| Initiative package | `initiative.` | `initiative.traceability_baseline` |
| Requirement | `req.` | `req.traceability_baseline.001` |
| Acceptance criterion | `ac.` | `ac.traceability_baseline.001` |
| Decision | `decision.` | `decision.traceability_storage_model` |
| Task | `task.` | `task.local_task_tracking_foundation.001` |
| Acceptance contract | `contract.acceptance.` | `contract.acceptance.governed_acceptance_example` |
| Validation evidence | `evidence.` | `evidence.governed_acceptance_example.validation_baseline` |

### Required baseline trace links
| Artifact Family | Minimum Trace Links |
|---|---|
| Initiative package | `trace_id` plus linked decisions, design records, or implementation slices when they exist |
| Decision note | `trace_id` plus linked initiative briefs, design records, implementation slices, or affected paths when they exist |
| Design record | `trace_id`, source request, and linked implementation slices when they exist |
| Implementation slice | `trace_id` plus source design records, initiative briefs, or decisions that justify the slice |
| Task record | `trace_id` for traced initiatives, explicit task `id`, and linked planning IDs or task dependencies when they exist |
| Acceptance contract | `trace_id`, source initiative identity, and preserved `acceptance_id` values |
| Validation evidence | `trace_id`, covered validators or check methods, and covered acceptance or artifact surfaces |
| Unified traceability index | `trace_id` plus joined upstream and downstream artifact identifiers |

## Process or Workflow
1. Identify the durable planning artifact being created or updated.
2. Assign or preserve its stable identifier before downstream docs or indexes reference it.
3. Add or refresh the human-readable tracker for that family.
4. Add or refresh the machine-readable index entry for that family.
5. Update upstream or downstream artifacts when the change introduces or invalidates a trace link.
6. Refresh the unified traceability index when the change affects a traced initiative.
7. Refresh the derived initiative coordination surfaces when the change affects initiative phase, ownership, or next-step guidance materially.
8. Record missing downstream trace work explicitly when the full chain cannot be completed in the same change.

## Examples
- An initiative brief should name requirement IDs so a later implementation slice or validation artifact can point back to them.
- A decision note that changes validation behavior should point to the affected initiative brief or design record, not just describe the decision in isolation.
- A design record without a linked implementation slice is acceptable when planning has not started yet, but the absence should remain explicit rather than implied.
- A validation-evidence artifact should link to the acceptance items and validators it covers rather than forcing later readers to reconstruct the relationship manually.

## Operationalization
- `Modes`: `documentation`; `sync`; `query`; `workflow`
- `Operational Surfaces`: `plan/tracking/coordination_tracking.md`; `plan/python/src/watchtower_plan/sync/traceability.py`; `core/python/src/watchtower_core/query/traceability.py`; `plan/workflows/modules/traceability_reconciliation.md`

## Validation
- Durable planning and trace artifacts should have stable IDs where this standard expects them.
- Human trackers and machine indexes should agree on the set of current initiative, decision, design, plan, contract, and evidence artifacts they claim to cover.
- A reviewer should be able to walk upstream and downstream links without relying on verbal context.
- Trace links should be updated when a planning artifact is renamed or materially retargeted.
- Active trace entries should carry linked task IDs instead of relying on implied execution state.
- Terminal trace entries should not leave `updated_at` earlier than `closed_at`.
- Family trackers should not default to exhaustive terminal-trace tables when the repository already provides explicit history query surfaces.
- Canonical standards, README entrypoints, and trackers should not rely on purgeable trace-local paths as the enduring source of current policy.

## Change Control
- Update this standard when the repository changes the baseline trace chain or introduces a new first-class traced artifact family.
- Update the initiative, decision, design, acceptance, evidence, and traceability tracking surfaces in the same change set when traceability expectations change materially.

## References
- [decision_capture_standard.md](/plan/docs/standards/governance/decision_capture_standard.md)
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md)
- [initiative_closeout_standard.md](/plan/docs/standards/governance/initiative_closeout_standard.md)
- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md)

## Updated At
- `2026-03-20T23:55:00Z`
