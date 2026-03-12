---
trace_id: trace.standards_lookup_and_generic_template_alignment
id: decision.standards_lookup_and_generic_template_alignment_direction
title: Standards Lookup and Generic Template Alignment Direction Decision
summary: Records the accepted direction for descendant-aware standards lookup
  and generic-template scope alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T00:14:46Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/templates/documentation_template.md
- docs/templates/README.md
---

# Standards Lookup and Generic Template Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.standards_lookup_and_generic_template_alignment`
- `Decision ID`: `decision.standards_lookup_and_generic_template_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.standards_lookup_and_generic_template_alignment`
- `Linked Designs`: `design.features.standards_lookup_and_generic_template_alignment`
- `Linked Implementation Plans`: `design.implementation.standards_lookup_and_generic_template_alignment`
- `Updated At`: `2026-03-12T00:14:46Z`

## Summary
Records the accepted direction for descendant-aware standards lookup and
generic-template scope alignment.

## Decision Statement
Adopt descendant-aware matching for `operationalization_path` lookups in the
standards query service and narrow the generic documentation template so it is
used only when no narrower governed family template applies.

## Trigger or Source Request
- Another expansive internal standards review reproduced two live gaps: query standards path filters do not resolve directory-governed concrete files, and the generic documentation template still advertises itself as a replacement for governed family-specific templates.

## Current Context and Constraints
- The standards index already publishes many directory-scoped operational
  surfaces such as `docs/planning/prds/`, `docs/planning/decisions/`, and
  `docs/templates/`, but `StandardQueryService` currently exact-matches only
  the literal string values.
- Concrete-file lookups therefore return zero standards for many real governed
  files, including reproduced PRD and decision examples.
- The generic documentation template still tells authors to use it for
  standards, references, and design docs even though those families now have
  dedicated templates and stricter contracts.

## Applied References and Implications
- `docs/standards/documentation/compact_document_authoring_standard.md`: the
  generic template should remain a compact fallback, not a parallel governed
  scaffold for families with stricter templates.
- `docs/standards/documentation/prd_md_standard.md`: concrete PRD files should
  resolve back to the PRD family standard during standards lookup.
- `docs/standards/documentation/decision_record_md_standard.md`: concrete
  decision files should resolve back to the decision-record standard during
  standards lookup.
- `docs/standards/documentation/command_md_standard.md`: the command page for
  standards lookup must describe the actual operationalization-path behavior.
- `docs/standards/metadata/front_matter_standard.md`: generic template guidance
  must not imply that governed family-specific front matter expectations are
  optional.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/templates/documentation_template.md
- docs/templates/README.md

## Options Considered
### Option 1
- Keep exact-match query behavior and patch affected standards with more
  explicit file-level operationalization paths.
- Strength: avoids changing query semantics.
- Tradeoff: fragile and unscalable because every new governed file would need
  manual standard edits to stay discoverable.

### Option 2
- Make all standards-query path filters descendant-aware and leave the generic
  documentation template broad.
- Strength: more uniform path-filter semantics and smaller documentation diff.
- Tradeoff: expands behavior beyond the reproduced defect and leaves the stale
  template bypass surface in place.

### Option 3
- Make only `operationalization_path` descendant-aware and narrow the generic
  documentation template to fallback-only guidance.
- Strength: fixes the concrete-file lookup defect and the stale template scope
  in one bounded slice while preserving the current exact semantics of other
  filters.
- Tradeoff: requires command-doc updates and dedicated regression coverage so
  the narrower semantics stay explicit.

## Chosen Outcome
Adopt option 3. `operationalization_path` should treat indexed directories as
governing descendant files, while the generic documentation template should be
repositioned as a fallback for unguided docs only. Other path filters remain
exact in this slice.

## Rationale and Tradeoffs
- This choice fixes the user-facing standards lookup defect without rewriting
  unrelated query semantics.
- It also removes a stale authoring shortcut that now conflicts with the
  repository’s governed family-specific templates.
- The main tradeoff is that descendant matching is deliberately limited to
  `operationalization_path`, so future reviews may still decide whether other
  path filters need similar behavior for separate reasons.

## Consequences and Follow-Up Impacts
- `watchtower-core query standards` will become more useful for concrete-file
  lookups across governed families.
- The command page for that query surface must explain the descendant-match
  rule clearly.
- The generic documentation template and templates inventory will steer authors
  toward narrower family templates first.

## Risks, Dependencies, and Assumptions
- Assumes the repository-root path check can distinguish directories cleanly so
  descendant matching does not over-match file prefixes.
- Depends on regression coverage across CLI behavior and template guidance to
  keep the new boundary stable.

## References
- docs/standards/documentation/compact_document_authoring_standard.md
- docs/standards/documentation/prd_md_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/command_md_standard.md
- docs/standards/metadata/front_matter_standard.md
