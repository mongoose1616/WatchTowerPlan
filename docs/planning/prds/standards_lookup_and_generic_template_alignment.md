---
trace_id: trace.standards_lookup_and_generic_template_alignment
id: prd.standards_lookup_and_generic_template_alignment
title: Standards Lookup and Generic Template Alignment PRD
summary: Make standards path lookup resolve directory-governed concrete files and
  narrow the generic documentation template so it no longer advertises family-specific
  governed docs.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T00:14:46Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/templates/documentation_template.md
- docs/templates/README.md
---

# Standards Lookup and Generic Template Alignment PRD

## Record Metadata
- `Trace ID`: `trace.standards_lookup_and_generic_template_alignment`
- `PRD ID`: `prd.standards_lookup_and_generic_template_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.standards_lookup_and_generic_template_alignment_direction`
- `Linked Designs`: `design.features.standards_lookup_and_generic_template_alignment`
- `Linked Implementation Plans`: `design.implementation.standards_lookup_and_generic_template_alignment`
- `Updated At`: `2026-03-12T00:14:46Z`

## Summary
Make standards path lookup resolve directory-governed concrete files and narrow the generic documentation template so it no longer advertises family-specific governed docs.

## Problem Statement
The expansive internal standards review reproduced two still-live drift
boundaries. First, `watchtower-core query standards --operationalization-path`
currently exact-matches only the literal values published in the standard
index, so directory-scoped operationalization paths such as
`docs/planning/prds/` or `docs/planning/decisions/` do not resolve when a user
asks about a concrete governed file under those families. Reproduced examples
returned zero results for
`docs/planning/prds/reference_and_workflow_standards_alignment.md` and
`docs/planning/decisions/reference_and_workflow_standards_alignment_direction.md`,
which means the standards lookup surface cannot currently return the governing
family standard for many real repository files. Second,
`docs/templates/documentation_template.md` still tells authors to use the
generic template for standards, design docs, and reference docs even though
those governed families now have dedicated templates and stricter authoring
contracts. That leaves a stale bypass surface in the template corpus and makes
standards lookup for the generic template ambiguous at the exact moment the
template should instead steer authors toward narrower family-specific
scaffolds.

## Goals
- Make `watchtower-core query standards --operationalization-path` resolve
  concrete files that sit under directory-scoped operationalization surfaces.
- Narrow the generic documentation template so it is clearly a fallback for
  unguided repository docs rather than a substitute for governed family
  templates.
- Add regression coverage and command guidance so standards lookup and template
  authoring fail closed if this drift returns.

## Non-Goals
- Redesign the standard index schema or rewrite how standards publish
  `applies_to` and `related_paths`.
- Remove `docs/templates/documentation_template.md` from the repository.
- Change unrelated standards-query filters unless the reproduced lookup bug
  requires it.

## Requirements
- `req.standards_lookup_and_generic_template_alignment.001`: Standards lookup
  must resolve a concrete repository file when an indexed standard publishes a
  governing directory in `operationalization_paths`.
- `req.standards_lookup_and_generic_template_alignment.002`: The generic
  documentation template and templates inventory must describe that template as
  a fallback for docs without a narrower family scaffold and must stop
  advertising it for governed standards, references, or planning design
  families.
- `req.standards_lookup_and_generic_template_alignment.003`: Regression
  coverage and command guidance must fail closed if descendant operationalizing
  file lookup or the generic-template family boundary drifts again.
- `req.standards_lookup_and_generic_template_alignment.004`: The trace must
  close on a green repository validation baseline after the query, docs, and
  regression updates land.

## Acceptance Criteria
- `ac.standards_lookup_and_generic_template_alignment.001`: The trace publishes
  the full planning chain, accepted direction decision, refreshed acceptance
  contract, refreshed planning-baseline evidence, and the bounded closed task
  set for the completed standards-alignment slice.
- `ac.standards_lookup_and_generic_template_alignment.002`: Querying standards
  by a concrete governed descendant file now returns the governing
  directory-scoped standard, and regression checks fail if operationalization
  path lookup falls back to exact-match-only behavior again.
- `ac.standards_lookup_and_generic_template_alignment.003`: The generic
  documentation template and templates inventory now position that template as
  fallback-only authoring guidance instead of a governed-family substitute, and
  regression checks fail if the broad stale guidance returns.
- `ac.standards_lookup_and_generic_template_alignment.004`: The repository
  baseline revalidates cleanly after sync, acceptance validation, aggregate
  validation, tests, type checking, and linting.

## Risks and Dependencies
- Directory-aware standards lookup must stay tightly scoped to
  `operationalization_paths` so other exact-match filters do not silently
  change semantics in the same slice.
- Narrowing the generic documentation template must still preserve one compact
  fallback scaffold for docs that do not belong to a narrower governed family.

## References
- docs/standards/documentation/compact_document_authoring_standard.md
- docs/standards/documentation/prd_md_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/command_md_standard.md
- docs/standards/metadata/front_matter_standard.md
