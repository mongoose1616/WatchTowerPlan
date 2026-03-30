---
id: "std.governance.initiative_engineer_handoff_support"
title: "Initiative Engineer Handoff Support Standard"
summary: "Defines the minimum support-doc kit and template posture for engineer-facing initiative packages that are meant to be executed directly."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "initiative_handoff"
owner: "repository_maintainer"
updated_at: "2026-03-29T04:05:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "plan/initiatives/"
  - "plan/projects/"
  - "plan/.wt/registries/template_catalog.json"
  - "plan/.wt/templates/initiatives/"
  - "plan/docs/standards/governance/initiative_tracking_standard.md"
aliases:
  - "initiative handoff support"
  - "engineer handoff support kit"
---

# Initiative Engineer Handoff Support Standard

## Summary
This standard defines the minimum support-doc kit, cold-start posture, and reusable template expectations for engineer-facing initiative packages that are meant to be executed directly.

## Purpose
- Make large initiative packages executable without forcing engineers to rediscover read order, proof boundaries, or baseline recording rules from scattered docs.
- Standardize the minimum support kit that sits beneath initiative-level authority surfaces and live task state.
- Promote reusable initiative-support templates and patterns so future initiatives can adopt the same handoff posture by default.

## Scope
- Applies when an initiative package is intended to hand engineers directly into execution from the initiative root.
- Applies especially when an initiative is `ready_for_execution`, spans multiple phases, or is expected to guide work in another repository.
- Applies to initiative-local support docs plus the reusable template and standards surfaces that define or publish that support posture.
- Does not replace the canonical authored inputs, live task state, traceability surfaces, or initiative phase vocabulary.

## Use When
- A preserved implementation package is large enough that a new engineer needs a guided start path.
- A first ready task depends on several canonical and support docs being read in a specific order.
- The initiative needs reusable README, manifest, checklist, or cold-start templates rather than bespoke one-off support files.

## Related Standards and Sources
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md): defines the live initiative package and execution-facing tracking posture this support kit complements.
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): defines the trace spine and joined machine surfaces that support docs must stay aligned with.
- [acceptance_evidence_reconciliation_standard.md](/plan/docs/standards/governance/acceptance_evidence_reconciliation_standard.md): governs how support-surface claims stay aligned with acceptance and evidence artifacts.
- [README.md](/plan/.wt/templates/initiatives/README.md): reusable template for the initiative-root navigation surface.
- [cold_start_runbook.md](/plan/.wt/templates/initiatives/cold_start_runbook.md): reusable template for first-ready-task entry guidance.

## Guidance
- Engineer-facing initiative packages must keep the four canonical authored docs and live task state as the authority layer.
- Engineer-facing initiative packages must publish this core support kit:
  - initiative-root `README.md`
  - `phase_output_manifest.md`
  - `phase_closeout_checklists.md`
  - `cold_start_runbook.md` for the first ready task or first ready phase
- The initiative-root `README.md` must route a new reader to the first ready task, the canonical docs, the key support docs, and the live machine start-here surfaces.
- `cold_start_runbook.md` must make these things explicit for the first ready task:
  - read order
  - review questions
  - command anchors
  - where to record a delta or a no-change conclusion
- Support docs must remain execution aids. They must not become a second source of planning authority.
- When the implementation shape needs them, initiatives should also publish the relevant conditional support surfaces:
  - `starter_surface_blueprint.md` and `starter_registry_exemplars.md` for bootstrap or human-surface posture
  - `vertical_slice_proof_spec.md` for first-runtime proof boundaries
  - `artifact_specimens.md` and `machine_surface_specimen_index.md` for first governed machine records and indexes
  - `phase_test_matrix.md` for phase-level proof expectations
  - `engineer_ambiguity_kill_sheet.md`, `conditional_revisit_queue.md`, and `contradiction_sweep_ledger.md` when defaults, deferrals, or reconciled tensions matter materially
  - `promotion_extraction_map.md` when closeout-to-knowledge promotion is part of the package
- If a support surface changes the execution meaning of a phase, update the canonical docs, live tasks, and machine acceptance or evidence surfaces in the same change set.
- Do not ship a `ready_for_execution` engineer handoff package that still leaves the first-ready-task read order or outcome-recording path implicit.

## Structure or Data Model
### Core support kit
| Surface | Required role |
|---|---|
| `README.md` | Initiative-root navigation and first-hop routing |
| `phase_output_manifest.md` | Phase-by-phase outputs, commands, validators, and evidence anchors |
| `phase_closeout_checklists.md` | Phase close criteria and proof reminders |
| `cold_start_runbook.md` | Explicit first-ready-task read order, review questions, and outcome-recording path |

### Conditional support kit
| Surface family | Use when |
|---|---|
| Starter surfaces and registry exemplars | Bootstrap-heavy or human-surface-heavy implementation phases |
| Runtime proof specs and artifact specimens | First governed runtime or machine-surface families need concrete examples |
| Test matrices and ambiguity aids | Multi-phase proof or default-handling would otherwise require guesswork |
| Promotion maps | Closeout outputs are expected to promote into reusable knowledge |

## Process or Workflow
1. Confirm the initiative is execution-facing enough to require an engineer handoff support kit.
2. Publish or update the core support kit at the initiative root.
3. Add only the conditional support surfaces that the implementation shape genuinely needs.
4. Update canonical docs, live tasks, acceptance artifacts, evidence artifacts, and support docs in the same change set when handoff meaning changes.
5. Sync plan indexes and rendered surfaces after materially changing the support kit.
6. Promote generally reusable support surfaces into `plan/docs/**` and `plan/.wt/templates/initiatives/` once the initiative-local shape has been validated in real use.

## Operationalization
- `Modes`: `documentation`; `artifact`
- `Operational Surfaces`: `plan/docs/standards/governance/initiative_engineer_handoff_support_standard.md`; `plan/docs/patterns/initiative_engineer_handoff_support_pattern.md`; `plan/.wt/registries/template_catalog.json`; `plan/.wt/templates/initiatives/`

## Validation
- Reviewers should reject engineer-ready initiative packages that lack the core support kit or hide the first-ready-task path behind broad narrative docs.
- Reviewers should also reject packages where support docs disagree with the canonical docs or live task state about the next engineer action.
- The template catalog should publish reusable initiative-support templates for the core kit so future initiatives can adopt the same support posture without reauthoring the structure from scratch.
- When initiative-local support docs are materially added or changed, sync the plan indexes and rendered surfaces in the same change set.
- A cold-start engineer should be able to determine the first read order and where to record either a delta or a no-change conclusion without inspecting unrelated directories.

## Change Control
- Update this standard when the repository changes initiative handoff posture, the minimum support kit, or the reusable template expectations for execution-facing initiatives.
- Update the initiative tracking guidance, template catalog, initiative templates, and any affected acceptance or evidence guidance in the same change set when this standard changes materially.

## References
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md)
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md)
- [acceptance_evidence_reconciliation_standard.md](/plan/docs/standards/governance/acceptance_evidence_reconciliation_standard.md)
- [README.md](/plan/.wt/templates/initiatives/README.md)
- [cold_start_runbook.md](/plan/.wt/templates/initiatives/cold_start_runbook.md)

## Updated At
- `2026-03-29T04:05:00Z`
