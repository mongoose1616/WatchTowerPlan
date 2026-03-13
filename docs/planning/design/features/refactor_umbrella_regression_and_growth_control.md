---
trace_id: trace.refactor_umbrella_regression_and_growth_control
id: design.features.refactor_umbrella_regression_and_growth_control
title: Refactor Umbrella Regression and Growth Control Feature Design
summary: Defines the technical design boundary for Refactor Umbrella Regression and
  Growth Control.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T22:30:01Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/closeout/initiative.py
- workflows/modules/repository_review.md
- workflows/modules/initiative_closeout.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
- docs/commands/core_python/watchtower_core_closeout.md
- docs/standards/governance/initiative_closeout_standard.md
- docs/planning/
---

# Refactor Umbrella Regression and Growth Control Feature Design

## Record Metadata
- `Trace ID`: `trace.refactor_umbrella_regression_and_growth_control`
- `Design ID`: `design.features.refactor_umbrella_regression_and_growth_control`
- `Design Status`: `active`
- `Linked PRDs`: `prd.refactor_umbrella_regression_and_growth_control`
- `Linked Decisions`: `decision.refactor_umbrella_regression_and_growth_control_direction`
- `Linked Implementation Plans`: `design.implementation.refactor_umbrella_regression_and_growth_control`
- `Updated At`: `2026-03-13T22:30:01Z`

## Summary
Defines the technical design boundary for Refactor Umbrella Regression and Growth Control.

## Source Request
- User-requested umbrella refactor review across REFACTOR.md, pass traces, and commit history with root-cause hardening for regression, duplication, and surface-growth drift.

## Scope and Feature Boundary
- Covers one umbrella review of the March 13, 2026 external refactor audit, the seven
  completed follow-up refactor traces, and the `origin..HEAD` refactor commit range.
- Covers runtime closeout hardening, review-loop guidance, command and workflow docs, governing
  standards, and the planning artifacts needed to make the umbrella review durable.
- Excludes large-scale archival restructuring of historical planning files, broad CLI-family
  redesign beyond the closeout seam, and policy-level planning-threshold rewrites.

## Current-State Context
- The original external audit identified seventeen `RF-*` findings. Most direct hotspot items
  now show improvement in the current tree:
  - `coordination_index.v1.json` is now compact and active-first with empty `entries` when no
    initiatives are active, so `RF-CTL-001` is resolved.
  - `watchtower_core.md`, `watchtower_core_query.md`, and `watchtower_core_sync.md` are now
    `77`, `86`, and `79` lines respectively, down from the much larger umbrella pages noted by
    the audit, so `RF-CMD-001` is resolved.
  - `planning_scaffolds.py` is now `307` lines, `task_lifecycle.py` is `492`, and
    `control_plane/models/planning.py` is `37`, so `RF-PY-001`, `RF-PY-002`, and `RF-PY-003`
    were materially improved.
  - the reference maturity, placeholder-family, test-hotspot, and query-surface items called
    out in `RF-CTL-002`, `RF-REF-001`, and `RF-TST-001` were also addressed by completed traces.
- The pass series still exposed two systemic root issues:
  - repeated acceptance or evidence drift reopened multiple refactor traces late because
    initiative closeout does not itself gate on acceptance reconciliation
  - the review process kept creating new bounded traces under the same continuing `refactor`
    theme, which increased planning and control-plane surface while losing one umbrella stop
    condition
- The recent refactor commit range changed `202` files with `26514` insertions and `12953`
  deletions. Planning documents grew from `359` to `431`, closed task files from `159` to
  `196`, and acceptance contracts plus evidence ledgers from `45` each to `54` each.

## Foundations References Applied
- `docs/foundations/engineering_design_principles.md`: the design keeps one canonical
  machine-readable closeout gate and one stable umbrella review trace instead of implicit
  process memory.
- `docs/foundations/repository_standards_posture.md`: explicit paired human and machine
  surfaces must stay synchronized when closeout semantics or review workflow expectations
  change.

## Internal Standards and Canonical References Applied
- `docs/standards/governance/traceability_standard.md`: traced work must remain explicit end to
  end and closeout must preserve machine-readable trace integrity.
- `docs/standards/governance/initiative_closeout_standard.md`: initiative closeout is the
  canonical terminal state boundary and must publish explicit exceptions when it proceeds with
  unresolved work.
- `docs/standards/data_contracts/acceptance_contract_standard.md`: acceptance contracts must
  stay synchronized with PRD acceptance IDs.
- `docs/standards/data_contracts/validation_evidence_standard.md`: evidence artifacts must stay
  synchronized with trace, validator, and acceptance coverage.
- `workflows/modules/repository_review.md`: themed review loops must preserve one continuing
  findings ledger until the scope is actually exhausted.

## Design Goals and Constraints
- Add a root-cause control that stops the repeated late acceptance-drift regression without
  weakening closeout, validation, or traceability behavior.
- Preserve explicit operator escape hatches when a terminal closeout must proceed with a known
  acceptance exception.
- Keep the fix local to closeout, standards, docs, and review guidance; do not use this pass to
  redesign unrelated command families or historical planning storage.

## Options Considered
### Option 1
- Continue using disconnected refactor slices and rely on humans to remember that
  `watchtower-core validate acceptance` should run before every terminal closeout.
- Strength: no runtime changes.
- Tradeoff: does not address the repeated regression, does not create an umbrella stop
  condition, and continues to permit theme-level drift behind locally clean slices.

### Option 2
- Create one umbrella refactor review trace, publish a master current-state matrix for the
  original audit, gate initiative closeout on acceptance reconciliation by default, and update
  the repository-review plus initiative-closeout guidance to keep same-theme work under one
  trace.
- Strength: fixes the repeated late regression and addresses the process flaw that caused local
  stop conditions to masquerade as umbrella completion.
- Tradeoff: adds deliberate operator friction at closeout and does not shrink already-landed
  historical planning artifacts.

## Recommended Design
### Architecture
- Use the umbrella planning trace as the master refactor status layer for the external audit,
  completed refactor traces, and pass-series commit range.
- Extend `InitiativeCloseoutService` to run `AcceptanceReconciliationService` before terminal
  closeout and fail when issues exist unless the operator passes an explicit acceptance-drift
  override.
- Align the closeout command docs, workflow module, and initiative-closeout standard so the
  runtime guard and operator guidance stay synchronized.
- Update the repository-review workflow guidance so same-theme review loops keep one trace and
  one findings ledger until no new actionable issues remain under that continuing theme.

### Data and Interface Impacts
- `watchtower-core closeout initiative` gains an explicit acceptance-drift override.
- Initiative closeout results and handler payloads must expose whether acceptance issues were
  left in place.
- The planning corpus gains one umbrella current-state matrix that maps original `RF-*`
  findings to current status.

### Execution Flow
1. Audit the original `RF-*` findings against the current tree, completed refactor traces, and
   the refactor commit series.
2. Implement the closeout acceptance gate plus explicit override and add unit or integration
   coverage.
3. Refresh the review-loop guidance, initiative-closeout standard, and closeout command docs so
   the runtime and authored surfaces agree.
4. Re-run validation, post-fix review, second-angle confirmation, and adversarial confirmation
   on the final tree.

### Invariants and Failure Cases
- Initiative closeout must keep the existing open-task guard and surface-refresh behavior.
- A failing acceptance reconciliation must block closeout by default rather than silently
  mutating initiative state.
- The explicit override must keep the exception visible instead of hiding it behind success-only
  output.

## Affected Surfaces
- core/python/src/watchtower_core/closeout/initiative.py
- workflows/modules/repository_review.md
- workflows/modules/initiative_closeout.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
- docs/commands/core_python/watchtower_core_closeout.md
- docs/standards/governance/initiative_closeout_standard.md
- docs/planning/

## Design Guardrails
- Do not weaken or remove acceptance contracts, validation evidence, or traceability validation.
- Do not treat this umbrella review as license to create new disconnected refactor traces under
  the same continuing theme.

## Risks
- Existing operator habits may assume closeout is independent from acceptance reconciliation and
  will need updated guidance.
- The umbrella matrix improves navigation and audit memory, but it does not reduce historical
  file count immediately.

## References
- REFACTOR.md
- docs/planning/design/implementation/refactor_review_and_hardening.md
- docs/planning/design/implementation/query_family_source_surface_alignment.md
