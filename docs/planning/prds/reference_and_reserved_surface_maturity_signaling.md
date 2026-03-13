---
trace_id: trace.reference_and_reserved_surface_maturity_signaling
id: prd.reference_and_reserved_surface_maturity_signaling
title: Reference and Reserved Surface Maturity Signaling PRD
summary: Review and refactor reference-corpus maturity signaling and README-only reserved
  control-plane family signaling so query, sync, docs, and governed artifacts distinguish
  active support, supporting authority, candidate guidance, and reserved families
  deterministically.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T15:32:46Z'
audience: shared
authority: authoritative
applies_to:
- docs/references/
- core/control_plane/indexes/references/
- core/control_plane/indexes/registries/
- core/control_plane/indexes/schemas/
- core/control_plane/policies/
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/query/references.py
- core/python/src/watchtower_core/cli/query_knowledge_handlers.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- docs/commands/core_python/
- docs/standards/data_contracts/reference_index_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/operations/repository_maintenance_loop_standard.md
---

# Reference and Reserved Surface Maturity Signaling PRD

## Record Metadata
- `Trace ID`: `trace.reference_and_reserved_surface_maturity_signaling`
- `PRD ID`: `prd.reference_and_reserved_surface_maturity_signaling`
- `Status`: `active`
- `Linked Decisions`: `decision.reference_and_reserved_surface_maturity_signaling_direction`
- `Linked Designs`: `design.features.reference_and_reserved_surface_maturity_signaling`
- `Linked Implementation Plans`: `design.implementation.reference_and_reserved_surface_maturity_signaling`
- `Updated At`: `2026-03-13T15:32:46Z`

## Summary
Review and refactor reference-corpus maturity signaling and README-only reserved control-plane family signaling so query, sync, docs, and governed artifacts distinguish active support, supporting authority, candidate guidance, and reserved families deterministically.

## Problem Statement
The March 2026 refactor audit left two connected maturity-signaling gaps open after the phase-one refactor slice closed. First, the governed reference corpus already carries stable human-readable `Current Repository Status` language, but the machine-readable reference index and the `watchtower-core query references` surface do not expose that distinction. Today the index contains 63 entries, 40 of those reference docs are explicitly candidate future guidance, and 38 entries publish only `docs/references/README.md` as a related path. Because reference-index sync currently pulls repo-local paths from the generic `References` section, those candidate entries are still indexed as `uses_internal_references: true`, and human query output prints them as `internal=yes` even when no live standard, workflow, or code surface depends on them.

Second, several control-plane families remain README-only reserved boundaries, but the family entrypoints still read like active artifact families. `core/control_plane/indexes/registries/`, `core/control_plane/indexes/schemas/`, `core/control_plane/policies/execution/`, and `core/control_plane/policies/validation/` currently publish only README files. The repository-maintenance standard already says README-only families should be treated as reserved until they carry real governed artifacts, but the local entrypoints and parent family READMEs do not surface that maturity distinction clearly enough for a start-here review.

These issues belong in one bounded refactor slice because they are both about deterministic maturity signaling across supporting knowledge and governed-control-plane surfaces. The fix should tighten how the repository describes present-tense support without deleting useful future guidance, weakening governed families, or adding opaque heuristics.

## Goals
- Publish one explicit coverage map and findings ledger for the reference-signaling and reserved-family slice before remediation begins.
- Make reference maturity status deterministic across authored reference docs, semantic validation, reference-index sync, typed models, query filters, CLI output, and command docs.
- Stop candidate references from looking like live internal support when their only repo-local backlink is the family README.
- Make directory-level query routing for reference touchpoints useful for real repository review by aligning `--related-path` behavior and docs with descendant paths.
- Mark README-only schema-index, registry-index, execution-policy, and validation-policy families as reserved placeholders consistently across their leaf and parent entrypoints.
- Run targeted validation, full repository validation, repeated confirmation passes, evidence refresh, task closeout, and initiative closeout only after the bounded slice stays clean.

## Non-Goals
- Deleting candidate future references from `docs/references/**` just because they are not yet applied by a live repository standard or workflow.
- Creating a new generic planning or policy family to summarize reserved-surface maturity outside the existing docs, standards, and control-plane entrypoints.
- Reworking the broader standards-boilerplate, test-suite decomposition, or repo-local hotspot findings from the audit in this trace.
- Adding a new reference-front-matter field to every governed reference document if the existing corpus already carries a stable, machine-derivable status vocabulary.

## Requirements
- `req.reference_and_reserved_surface_maturity_signaling.001`: The trace must publish and follow an explicit coverage map plus findings ledger across reference docs, the reference README and template, reference standards, reference-index schema and examples, sync and query paths, typed models, semantic validation, command docs, reserved control-plane family entrypoints, and adjacent derived surfaces before remediation begins.
- `req.reference_and_reserved_surface_maturity_signaling.002`: Reference maturity signaling must be deterministic across authored docs and machine-readable lookup surfaces: approved repository-status language must validate semantically, the reference index must expose a machine-readable maturity field, and candidate references must not be indexed as live internal support solely because of README backlinks.
- `req.reference_and_reserved_surface_maturity_signaling.003`: `watchtower-core query references` must expose the repaired maturity signal and support related-path lookup behavior that works for real directory touchpoints used in command docs and review flows, with aligned command help, command docs, and regression coverage.
- `req.reference_and_reserved_surface_maturity_signaling.004`: README-only control-plane families for schema indexes, registry indexes, execution policies, and validation policies must be explicitly marked as reserved placeholders across their local family entrypoints and adjacent start-here guidance until live governed artifacts exist there.
- `req.reference_and_reserved_surface_maturity_signaling.005`: The initiative must create bounded execution tasks, perform targeted validation and full repository validation, run post-fix, second-angle, and adversarial confirmation passes, refresh durable evidence, close the tasks, and finish in a clean committed state.

## Acceptance Criteria
- `ac.reference_and_reserved_surface_maturity_signaling.001`: The planning corpus for `trace.reference_and_reserved_surface_maturity_signaling` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, bounded execution tasks, and the explicit coverage map plus findings ledger for the slice.
- `ac.reference_and_reserved_surface_maturity_signaling.002`: Reference docs, reference standards, the reference template, semantic validation, reference-index sync, the reference-index schema and examples, typed models, query filters, CLI output, and command docs agree on deterministic repository-status signaling, and candidate references no longer appear as live internal support because of README-only backlinks.
- `ac.reference_and_reserved_surface_maturity_signaling.003`: `watchtower-core query references` supports status-aware lookup and usable directory touchpoint lookup for related paths, and its help text, command docs, index payload, and regression coverage stay aligned with that behavior.
- `ac.reference_and_reserved_surface_maturity_signaling.004`: `core/control_plane/indexes/README.md`, `core/control_plane/indexes/registries/README.md`, `core/control_plane/indexes/schemas/README.md`, `core/control_plane/policies/README.md`, `core/control_plane/policies/execution/README.md`, `core/control_plane/policies/validation/README.md`, and adjacent maintenance guidance all describe the README-only families as reserved placeholders rather than live published artifact families.
- `ac.reference_and_reserved_surface_maturity_signaling.005`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation all complete without finding a new actionable issue inside this refactor slice.

## Risks and Dependencies
- The reference-status fix touches docs, semantic validation, schema-backed artifacts, query behavior, command docs, and tests in one slice, so incomplete same-change updates would create real drift instead of just cosmetic inconsistency.
- Deriving repository status from authored doc sections depends on keeping the current status vocabulary explicit and validated; the implementation must fail closed if a reference drifts from the approved phrases.
- Changing related-path matching for reference queries must stay deterministic and should not silently broaden unrelated query families unless that broader behavior is explicitly designed and tested later.
- Reserved-family clarification must preserve those directories as intentional future landing zones; the goal is explicit maturity signaling, not accidental retirement of valid repository boundaries.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): simplification should tighten explicit seams and deterministic read models rather than replace them with opaque heuristics or weaker authority boundaries.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable docs, machine-readable indexes, query behavior, and validation surfaces must move together when a supporting authority surface changes meaning.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the slice stays inside repository-maintenance refactor work and does not expand into future product policy or implementation work.

## References
- March 2026 refactor audit
