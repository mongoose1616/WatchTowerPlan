---
trace_id: trace.standards_lookup_and_generic_template_alignment
id: design.implementation.standards_lookup_and_generic_template_alignment
title: Standards Lookup and Generic Template Alignment Implementation Plan
summary: Breaks the standards-query and generic-template alignment work into a
  bounded implementation slice.
type: implementation_plan
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

# Standards Lookup and Generic Template Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.standards_lookup_and_generic_template_alignment`
- `Plan ID`: `design.implementation.standards_lookup_and_generic_template_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.standards_lookup_and_generic_template_alignment`
- `Linked Decisions`: `decision.standards_lookup_and_generic_template_alignment_direction`
- `Source Designs`: `design.features.standards_lookup_and_generic_template_alignment`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-12T00:14:46Z`

## Summary
Breaks the standards-query and generic-template alignment work into a bounded
implementation slice.

## Source Request or Design
- Another expansive internal standards review reproduced two live gaps: query standards path filters do not resolve directory-governed concrete files, and the generic documentation template still advertises itself as a replacement for governed family-specific templates.

## Scope Summary
- Update standards-query path matching, its command page, and regression
  coverage so concrete files inherit directory-scoped operationalizing
  standards.
- Narrow the generic documentation template and templates inventory wording so
  contributors are routed toward governed family-specific templates first.
- Exclude a broader redesign of standard-index semantics or unrelated template
  families.

## Assumptions and Constraints
- Directory-scoped operationalization paths already encode family governance, so
  descendant lookup is less risky than enumerating every file explicitly.
- This slice should change only `operationalization_path` matching semantics;
  exact authored-field filters remain out of scope unless a new reproduced bug
  requires expansion.

## Internal Standards and Canonical References Applied
- `docs/standards/documentation/compact_document_authoring_standard.md`: the
  fallback template must stay compact and narrowly scoped.
- `docs/standards/documentation/command_md_standard.md`: command docs must
  describe the actual behavior of the query surface they document.
- `docs/standards/documentation/prd_md_standard.md`: concrete PRD lookup should
  resolve the PRD family standard.
- `docs/standards/documentation/decision_record_md_standard.md`: concrete
  decision lookup should resolve the decision family standard.
- `docs/standards/metadata/front_matter_standard.md`: generic-template guidance
  must not undercut governed family metadata rules.

## Proposed Technical Approach
- Add a repository-root-aware path-match helper to `StandardQueryService` so
  `operationalization_path` returns matches when an indexed directory governs a
  concrete descendant file.
- Update the `watchtower-core query standards` command page and CLI tests to
  capture the new descendant-path behavior explicitly.
- Rewrite the generic documentation template and templates README to make the
  fallback-template boundary explicit, then add artifact regression coverage for
  that guidance.

## Work Breakdown
1. Close the bootstrap task and publish concrete PRD, design, implementation,
   decision, and execution-task artifacts for the confirmed issue set.
2. Implement directory-aware `operationalization_path` lookup and add CLI
   regressions for concrete PRD, decision, and generic-template paths.
3. Narrow the generic documentation template and templates inventory wording,
   then add artifact checks that fail if family-specific guidance creeps back
   into the fallback scaffold.
4. Refresh acceptance artifacts, sync derived surfaces, rerun the full
   validation baseline, and close the initiative cleanly.

## Risks
- The query change could become too permissive if directory detection is not
  constrained to actual repository directories.
- The fallback template rewrite must stay useful for unguided docs rather than
  becoming so narrow that it no longer helps non-governed documentation work.

## Validation Plan
- Run targeted CLI and artifact regressions for descendant lookup and generic
  template guidance.
- Run `./.venv/bin/watchtower-core sync all --write --format json`,
  `./.venv/bin/watchtower-core validate acceptance --trace-id
  trace.standards_lookup_and_generic_template_alignment --format json`,
  `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest
  -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and
  `./.venv/bin/ruff check .`.

## References
- docs/standards/documentation/compact_document_authoring_standard.md
- docs/standards/documentation/prd_md_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/command_md_standard.md
- docs/standards/metadata/front_matter_standard.md
