---
trace_id: trace.governed_front_matter_directory_canonicalization
id: design.features.governed_front_matter_directory_canonicalization
title: Governed Front Matter Directory Canonicalization Feature Design
summary: Defines the technical design boundary for Governed Front Matter Directory
  Canonicalization.
type: feature_design
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T02:46:38Z'
audience: shared
authority: authoritative
applies_to:
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
---

# Governed Front Matter Directory Canonicalization Feature Design

## Record Metadata
- `Trace ID`: `trace.governed_front_matter_directory_canonicalization`
- `Design ID`: `design.features.governed_front_matter_directory_canonicalization`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.governed_front_matter_directory_canonicalization`
- `Linked Decisions`: `decision.governed_front_matter_directory_canonicalization.direction`
- `Linked Implementation Plans`: `design.implementation.governed_front_matter_directory_canonicalization`
- `Updated At`: `2026-03-12T02:46:38Z`

## Summary
Defines the technical design boundary for Governed Front Matter Directory Canonicalization.

## Source Request
- Execute the internal project standards review loop until no new issues are identified.

## Scope and Feature Boundary
- Covers governed front-matter families that currently author or derive path-valued `applies_to` metadata: standards, references, foundations, traced planning docs, and local task docs.
- Covers both recurrence prevention in authoring paths and fail-closed enforcement in validation and sync paths.
- Covers live governed Markdown docs, valid front-matter examples, and family guidance or templates that currently drift from the canonical path rule.
- Does not add fuzzy matching or wildcard semantics to `applies_to`.
- Does not broaden `applies_to` to non-existent future surfaces; path-valued entries stay bound to live repo-local paths.

## Current-State Context
- The review audit found 11 governed Markdown docs and 2 valid front-matter example JSON files with directory-valued `applies_to` entries missing the canonical trailing slash.
- The reproduced user-visible failure was `watchtower-core query standards --applies-to docs/commands/ --format json`, which returned zero results because the live `std.engineering.cli_help_text` entry carried `docs/commands` and `core/python/src/watchtower_core/cli` without trailing slashes.
- Planning scaffolds and task lifecycle writes were still capable of reproducing the drift because they wrote `applies_to` values verbatim, while semantic validation and sync only enforced canonical path syntax for some other metadata families such as standard operationalization paths.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the fix should centralize one coherent path rule instead of duplicating family-specific normalization logic.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable standards guidance and machine-enforced repo behavior need to move together so lookup and governance surfaces stay aligned.

## Internal Standards and Canonical References Applied
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): path-valued `applies_to` metadata is governed front matter and needs one canonical repo-relative file-versus-directory rule.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): exact standards lookup depends on authored `applies_to` and derived `related_paths` staying canonical.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): standard docs are a live affected family and their operationalization guidance already models canonical directory syntax.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the implementation belongs in the canonical `core/python/` workspace and must keep command and validation behavior aligned with docs.

## Design Goals and Constraints
- Use one helper for canonical path-valued `applies_to` normalization so standards, references, foundations, planning docs, and tasks do not drift through copy-pasted parsing logic.
- Preserve concept-valued `applies_to` entries that do not contain repo-path syntax.
- Keep exact query behavior intact by canonicalizing authored data rather than layering fuzzy path matching over stale index values.
- Fail closed on authored non-canonical docs while still making authoring commands ergonomic through write-time normalization.

## Options Considered
### Option 1
- Normalize only the currently affected live docs and examples.
- Strength: smallest immediate diff.
- Tradeoff: does not prevent planning scaffolds, task writes, or future manual edits from reintroducing the same drift.

### Option 2
- Normalize query inputs or add descendant-style matching while leaving authored `applies_to` metadata untouched.
- Strength: can mask the reproduced standards query miss quickly.
- Tradeoff: leaves the governed corpus non-canonical and keeps derived indexes inconsistent with published front-matter guidance.

### Option 3
- Add one shared canonicalization helper, use it in governed authoring and load paths, reject non-canonical authored docs in validation and sync, and normalize the live corpus in the same slice.
- Strength: fixes the current bug and the recurrence vector together.
- Tradeoff: requires broader coordinated updates across code, docs, examples, and derived artifacts.

## Recommended Design
### Architecture
- Add a shared front-matter path helper in `watchtower_core.repo_ops` that canonicalizes path-valued `applies_to` entries to repo-relative file or slash-terminated directory forms.
- Use that helper in planning-document loading, task-document loading, standard/reference/foundation index sync, and planning or task authoring paths so all governed families share the same rule.
- Normalize the live governed documents and valid front-matter examples to the canonical forms, then refresh the derived indexes and trackers they feed.

### Data and Interface Impacts
- Affected implementation surfaces include planning scaffolds, task lifecycle writes, governed document loaders, and standard/reference/foundation sync services.
- Affected machine-readable artifacts include the standard, reference, foundation, planning, task, traceability, initiative, and coordination indexes that carry or derive the canonical paths.
- Affected human-readable guidance includes the front-matter standard, standard-index standard, family templates, and the currently affected live governed docs.

### Execution Flow
1. Introduce the shared `applies_to` helper and wire it through governed loading, sync, and authoring paths.
2. Normalize the live governed Markdown docs, affected standards guidance, templates, and valid front-matter examples to slash-terminated directory syntax where appropriate.
3. Refresh derived artifacts, run exact standards-query regressions and the expansive audit, then close the trace once no remaining issues are found.

### Invariants and Failure Cases
- Concept-valued `applies_to` entries remain untouched when they are not path-like.
- Path-valued `applies_to` entries must resolve to live repo-local surfaces; directories end in `/`, files do not.
- Authoring flows should canonicalize user-provided directory inputs such as `docs/planning` to `docs/planning/`.
- Semantic validation and sync should fail on authored non-canonical directory or file path syntax so stale docs cannot silently project bad index metadata.

## Affected Surfaces
- docs/
- core/python/src/watchtower_core/
- core/control_plane/

## Design Guardrails
- Do not invent family-specific path rules; every governed `applies_to` path should use the same canonical file-versus-directory contract.
- Do not solve the standards query miss by making lookup fuzzier while leaving authored metadata stale.
- Do not leave templates, standards guidance, or valid examples teaching the old non-canonical directory syntax.

## Risks
- Tightened validation will surface any additional non-canonical governed docs immediately, so the slice needs a final expansive audit before closeout.
- Shared canonicalization has to avoid treating concept entries as repo paths when they are not intended to resolve under the repository root.

## References
- docs/standards/metadata/front_matter_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/references/front_matter_reference.md
