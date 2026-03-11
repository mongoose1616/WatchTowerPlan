---
trace_id: trace.reference_and_workflow_standards_alignment
id: prd.reference_and_workflow_standards_alignment
title: Reference and Workflow Standards Alignment PRD
summary: Align governed reference authoring guidance with live validator and
  index expectations, and tighten workflow additional-load enforcement so
  generic workflow standards stay implicit.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T23:19:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/templates/workflow_template.md
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
---

# Reference and Workflow Standards Alignment PRD

## Record Metadata
- `Trace ID`: `trace.reference_and_workflow_standards_alignment`
- `PRD ID`: `prd.reference_and_workflow_standards_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.reference_and_workflow_standards_alignment_direction`
- `Linked Designs`: `design.features.reference_and_workflow_standards_alignment`
- `Linked Implementation Plans`: `design.implementation.reference_and_workflow_standards_alignment`
- `Updated At`: `2026-03-11T23:19:00Z`

## Summary
Align governed reference authoring guidance with live validator and index
expectations, and tighten workflow additional-load enforcement so generic
workflow standards stay implicit.

## Problem Statement
The expansive internal standards review reproduced two still-live contract
gaps. First, the governed reference validator and reference-index sync both
require every `docs/references/**` document to publish `Canonical Upstream`,
and the reference-index standard also treats canonical upstream URLs as a
required machine-readable field, but the reference authoring standard and
template still describe that section as optional. That drift leaves authoring
guidance weaker than the live enforced contract and falsely implies that a
fully repo-native reference document can omit upstream authority while still
participating in the governed reference family. Second, the workflow Markdown
standard says generic workflow standards must stay implicit instead of being
repeated in `Additional Files to Load`, but the workflow validator and sync
path currently allow `routing_and_context_loading_standard.md` to be listed as
task-specific additional context because the routing-baseline disallow list is
incomplete.

## Goals
- Make the reference authoring standard and template publish the same canonical
  upstream requirement that governed validation and indexing already enforce.
- Tighten workflow additional-load enforcement so all generic workflow
  standards, including routing-and-context-loading guidance, stay implicit.
- Add regression coverage and traced evidence so both contracts stay aligned
  across prose docs, validators, sync surfaces, and review checks.

## Non-Goals
- Introduce a new reference-document family for purely repo-native lookup
  content.
- Expand workflow additional-load enforcement beyond the already-published
  boundary that generic workflow standards should stay implicit.
- Redesign reference-index or workflow-index schemas beyond what the current
  governed contracts already require.

## Requirements
- `req.reference_and_workflow_standards_alignment.001`: Governed reference
  authoring guidance and templates must require `Canonical Upstream` for
  `docs/references/**` documents and must stop advertising that section as
  optional.
- `req.reference_and_workflow_standards_alignment.002`: Workflow
  additional-load validation and sync must reject all generic workflow
  standards that the workflow Markdown standard says should stay implicit,
  including `routing_and_context_loading_standard.md`.
- `req.reference_and_workflow_standards_alignment.003`: Regression coverage
  must fail closed when either the reference canonical-upstream contract or the
  workflow additional-load routing-baseline contract drifts again.
- `req.reference_and_workflow_standards_alignment.004`: The trace must close
  on a green repository validation baseline after the standards, validator,
  sync, and regression updates land.

## Acceptance Criteria
- `ac.reference_and_workflow_standards_alignment.001`: The trace publishes the
  full planning chain, accepted direction decision, refreshed acceptance
  contract, refreshed planning-baseline evidence, and the bounded task set for
  the completed standards-alignment slice.
- `ac.reference_and_workflow_standards_alignment.002`: The reference document
  standard and template publish `Canonical Upstream` as a required governed
  section, and regression checks fail if the reference authoring contract
  becomes optional again.
- `ac.reference_and_workflow_standards_alignment.003`: Workflow
  additional-load validation and sync reject generic workflow standards such as
  `routing_and_context_loading_standard.md`, and regression checks fail if the
  disallow set weakens again.
- `ac.reference_and_workflow_standards_alignment.004`: The repository baseline
  revalidates cleanly after the standards, validator, sync, and regression
  changes land.

## Risks and Dependencies
- Tightening reference authoring guidance could expose contributors who were
  using `docs/references/**` as a repo-native lookup family without upstream
  authority; the standard and template must make the governed family boundary
  explicit.
- Tightening workflow additional-load enforcement must preserve legitimate
  task-specific load paths while only rejecting the generic baseline surfaces
  that the workflow standard already says to keep implicit.

## References
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/standards/data_contracts/reference_index_standard.md
- docs/standards/data_contracts/workflow_index_standard.md
