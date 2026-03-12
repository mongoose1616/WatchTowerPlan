---
trace_id: trace.governed_front_matter_directory_canonicalization
id: design.implementation.governed_front_matter_directory_canonicalization
title: Governed Front Matter Directory Canonicalization Implementation Plan
summary: Breaks Governed Front Matter Directory Canonicalization into a bounded implementation
  slice.
type: implementation_plan
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T02:46:38Z'
audience: shared
authority: supporting
applies_to:
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
---

# Governed Front Matter Directory Canonicalization Implementation Plan

## Record Metadata
- `Trace ID`: `trace.governed_front_matter_directory_canonicalization`
- `Plan ID`: `design.implementation.governed_front_matter_directory_canonicalization`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.governed_front_matter_directory_canonicalization`
- `Linked Decisions`: `decision.governed_front_matter_directory_canonicalization.direction`
- `Source Designs`: `design.features.governed_front_matter_directory_canonicalization`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-12T02:46:38Z`

## Summary
Breaks Governed Front Matter Directory Canonicalization into a bounded implementation slice.

## Source Request or Design
- Execute the internal project standards review loop until no new issues are identified.

## Scope Summary
- Implement shared path canonicalization for governed `applies_to` metadata across authoring, loading, and sync.
- Normalize the live governed docs, valid examples, and guidance surfaces that currently publish non-canonical directory paths.
- Prove the reproduced standards-query fix and the final no-new-issues stop condition.
- Exclude unrelated query-behavior redesign outside the canonical exact-path contract.

## Assumptions and Constraints
- Slash-containing `applies_to` entries in governed docs should represent live repo-local paths rather than abstract concepts.
- The implementation must preserve concept-valued `applies_to` strings that do not resolve as repo paths.
- Derived coordination and planning surfaces must be refreshed after the authored corpus changes or stale paths will remain in indexes and trackers.

## Internal Standards and Canonical References Applied
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): governs the canonical path syntax that authored `applies_to` metadata must use.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): exact standards lookup depends on canonical authored `applies_to` and derived `related_paths`.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): implementation, tests, and CLI validation stay inside `core/python/`.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): planning docs, tasks, and derived trackers need to stay synchronized throughout the slice.

## Proposed Technical Approach
- Add a shared `front_matter_paths` helper that canonicalizes path-valued `applies_to` entries and optionally rejects authored non-canonical path syntax.
- Use that helper in planning-document and task-document loads, standard/reference/foundation sync services, and planning or task authoring paths so write-time and read-time behavior agree.
- Normalize the affected live docs, standards guidance, templates, and valid examples, then rebuild all affected machine-readable planning and governance surfaces in the same slice.

## Work Breakdown
1. Add the shared canonicalization helper and wire it through governed authoring, load, semantic-validation, and sync paths.
2. Normalize the affected governed Markdown docs, front-matter examples, and guidance surfaces, then refresh the derived indexes and trackers.
3. Add targeted regressions for document semantics, task lifecycle, planning scaffolds, standards query behavior, and live-corpus canonicalization.
4. Run the final expansive audit, validate the acceptance contract for this trace, and close the initiative after all remaining issues are zero.

## Risks
- New validation can surface previously silent drift in live governed docs beyond the already-audited set if another family was missed.
- Template and standards guidance updates have to land with the code or future manual edits could pass review even if automated authoring canonicalizes inputs.

## Validation Plan
- Run targeted unit and integration regressions covering task lifecycle writes, planning scaffolds, standards query filters, semantic validation, and live-corpus canonicalization.
- Run `watchtower-core sync all --write --format json` and `watchtower-core validate acceptance --trace-id trace.governed_front_matter_directory_canonicalization --format json`.
- Run final `watchtower-core validate all --format json`, `pytest -q`, `python -m mypy src/watchtower_core`, and `ruff check .`.
- Run the expansive governed-doc audit that scans governed Markdown docs and valid front-matter examples for remaining non-canonical directory `applies_to` values.

## References
- docs/standards/metadata/front_matter_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/references/front_matter_reference.md
