---
trace_id: trace.standards_lookup_and_generic_template_alignment
id: design.features.standards_lookup_and_generic_template_alignment
title: Standards Lookup and Generic Template Alignment Feature Design
summary: Defines the technical design boundary for descendant-aware standards
  lookup and generic-template scope alignment.
type: feature_design
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

# Standards Lookup and Generic Template Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.standards_lookup_and_generic_template_alignment`
- `Design ID`: `design.features.standards_lookup_and_generic_template_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.standards_lookup_and_generic_template_alignment`
- `Linked Decisions`: `decision.standards_lookup_and_generic_template_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.standards_lookup_and_generic_template_alignment`
- `Updated At`: `2026-03-12T00:14:46Z`

## Summary
Defines the technical design boundary for descendant-aware standards lookup and
generic-template scope alignment.

## Source Request
- Another expansive internal standards review reproduced two live gaps: query standards path filters do not resolve directory-governed concrete files, and the generic documentation template still advertises itself as a replacement for governed family-specific templates.

## Scope and Feature Boundary
- Covers directory-aware `operationalization_path` lookup in the standards
  query service and CLI-facing command guidance for that behavior.
- Covers narrowing `docs/templates/documentation_template.md` and
  `docs/templates/README.md` so the generic template no longer competes with
  governed family-specific scaffolds.
- Excludes changing `applies_to`, `related_path`, or `reference_path` filter
  semantics in the same slice.
- Excludes creating a new generic-document governed family or adding new front
  matter profiles.

## Current-State Context
- `StandardQueryService` exact-matches `operationalization_path` against the
  indexed string set, so directory-scoped standards do not resolve when users
  ask about a concrete descendant file.
- Reproduced queries for
  `docs/planning/prds/reference_and_workflow_standards_alignment.md` and
  `docs/planning/decisions/reference_and_workflow_standards_alignment_direction.md`
  returned zero standards even though their family standards publish
  `docs/planning/prds/` and `docs/planning/decisions/` as operational surfaces.
- `docs/templates/documentation_template.md` still advertises itself for
  standards, design docs, and reference docs even though those families now
  have governed templates and explicit authoring standards.

## Foundations References Applied
- `docs/foundations/repository_standards_posture.md`: standards lookup and
  authoring scaffolds should point to one coherent contract instead of leaving
  contributors to infer which surface actually governs a concrete file.

## Internal Standards and Canonical References Applied
- `docs/standards/documentation/compact_document_authoring_standard.md`: the
  generic template should remain compact and scoped to documents that lack a
  narrower family scaffold.
- `docs/standards/documentation/prd_md_standard.md`: PRD family lookup should
  resolve a concrete PRD file back to its governing standard.
- `docs/standards/documentation/decision_record_md_standard.md`: decision
  family lookup should resolve a concrete decision file back to its governing
  standard.
- `docs/standards/documentation/command_md_standard.md`: the command page for
  `watchtower-core query standards` must describe the actual path-filter
  behavior after the query-layer fix.
- `docs/standards/metadata/front_matter_standard.md`: the generic documentation
  template must not imply that governed-family front matter profiles can be
  bypassed casually.

## Design Goals and Constraints
- Return useful standards lookup results for concrete files without requiring
  every governed standard to enumerate every descendant file explicitly.
- Keep non-operationalization path filters stable unless a reproduced bug
  proves they must change.
- Preserve the generic documentation template as a fallback, not a deprecated
  dead file.

## Options Considered
### Option 1
- Add explicit file-level operationalization paths to every affected standard.
- Strength: avoids changing query semantics.
- Tradeoff: brittle, high-maintenance, and does not scale to future governed
  files under already-published family directories.

### Option 2
- Make `operationalization_path` descendant-aware for indexed directory
  surfaces and narrow the generic documentation template to fallback-only use.
- Strength: fixes concrete standards lookup across governed families and aligns
  the generic template with the current family-template posture in one bounded
  change.
- Tradeoff: command docs and regression coverage must update together so the
  new lookup semantics remain explicit.

### Option 3
- Make all standards-query path filters descendant-aware in one pass.
- Strength: more uniform path-filter semantics.
- Tradeoff: widens behavior beyond the reproduced lookup defect and changes
  filters that are currently documented and used as exact authored-field
  filters.

## Recommended Design
### Architecture
- Teach `StandardQueryService` to treat indexed directory paths as governing
  descendants when evaluating `operationalization_path`.
- Leave other path filters exact in this slice so the behavior change stays
  bounded to the reproduced standards-lookup defect.
- Rewrite the generic documentation template and templates README so they point
  authors to family-specific scaffolds first and reserve the generic template
  for repository docs without a narrower family contract.

### Data and Interface Impacts
- `watchtower-core query standards --operationalization-path` becomes
  descendant-aware for directory-scoped indexed surfaces.
- `docs/commands/core_python/watchtower_core_query_standards.md` must describe
  that descendant lookup behavior.
- `docs/templates/documentation_template.md` and `docs/templates/README.md`
  will publish a narrower authoring boundary without changing any governed
  front matter schema.

### Execution Flow
1. Replace the scaffold planning docs with the confirmed findings, accepted
   direction, and bounded task set.
2. Implement descendant-aware `operationalization_path` matching and add CLI
   regressions for concrete governed files and the generic documentation
   template path.
3. Narrow the generic template guidance and add artifact coverage that rejects
   family-specific governed-doc instructions in that fallback scaffold.
4. Refresh acceptance evidence, sync derived surfaces, and rerun the full
   repository validation baseline.

### Invariants and Failure Cases
- Querying a concrete file under a directory-scoped operational surface must
  return the governing standard instead of zero results.
- Exact file-path matches must continue to work unchanged.
- The generic documentation template must not tell authors to use it for
  governed standards, references, or planning design docs that already have
  dedicated templates.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/templates/documentation_template.md
- docs/templates/README.md

## Design Guardrails
- Do not broaden this slice into a global path-filter semantics rewrite.
- Do not remove the generic documentation template; narrow and operationalize
  its intent instead.

## Risks
- Directory detection must stay repository-root-aware so descendant matching
  does not accidentally treat similarly-prefixed file paths as governed by a
  non-directory operational surface.

## References
- docs/standards/documentation/compact_document_authoring_standard.md
- docs/standards/documentation/prd_md_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/command_md_standard.md
- docs/standards/metadata/front_matter_standard.md
