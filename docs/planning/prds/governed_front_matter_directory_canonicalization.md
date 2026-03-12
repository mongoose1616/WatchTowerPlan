---
trace_id: trace.governed_front_matter_directory_canonicalization
id: prd.governed_front_matter_directory_canonicalization
title: Governed Front Matter Directory Canonicalization PRD
summary: Canonicalize directory-valued governed front-matter applies_to metadata so
  exact repo-path lookup stays consistent across standards, references, and planning
  documents.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T02:46:38Z'
audience: shared
authority: authoritative
applies_to:
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
---

# Governed Front Matter Directory Canonicalization PRD

## Record Metadata
- `Trace ID`: `trace.governed_front_matter_directory_canonicalization`
- `PRD ID`: `prd.governed_front_matter_directory_canonicalization`
- `Status`: `active`
- `Linked Decisions`: `decision.governed_front_matter_directory_canonicalization.direction`
- `Linked Designs`: `design.features.governed_front_matter_directory_canonicalization`
- `Linked Implementation Plans`: `design.implementation.governed_front_matter_directory_canonicalization`
- `Updated At`: `2026-03-12T02:46:38Z`

## Summary
Canonicalize directory-valued governed front-matter applies_to metadata so exact repo-path lookup stays consistent across standards, references, and planning documents.

## Problem Statement
- The expansive internal standards review found 11 governed Markdown docs and 2 control-plane front-matter examples that still authored directory-valued `applies_to` entries without a trailing slash.
- That authored drift leaked into derived indexes such as the standard index, so exact slash-terminated path queries like `watchtower-core query standards --applies-to docs/commands/ --format json` could miss the governing standard even though repository guidance already used canonical directory syntax.
- The drift was also still reproducible because governed authoring paths such as planning scaffolds and task lifecycle writes accepted raw `applies_to` values without canonicalizing directory paths, while semantic validation did not enforce a shared repo-relative file-versus-directory rule.

## Goals
- Publish one shared canonicalization rule for path-valued governed `applies_to` metadata so directory entries always end in `/` and file entries do not.
- Apply that rule consistently across governed authoring, semantic validation, and derived sync surfaces for standards, references, foundations, planning docs, and tasks.
- Normalize the live governed corpus and control-plane examples so exact path lookup and derived `related_paths` remain deterministic.
- Close the review loop only after a final expansive audit reports zero remaining governed directory `applies_to` issues.

## Non-Goals
- Changing the meaning of concept-valued `applies_to` entries that do not represent repo paths.
- Introducing wildcard or future-path semantics to `applies_to`; path-valued entries should keep representing live repo-local surfaces.
- Reworking standard-query matching into fuzzy path search beyond the canonical exact-path contract already documented for slash-terminated directories.

## Requirements
- `req.governed_front_matter_directory_canonicalization.001`: Governed authoring and loading surfaces must share one canonical path rule for `applies_to`, automatically normalizing write-time directory inputs and rejecting non-canonical authored directory or file path syntax during validation and sync.
- `req.governed_front_matter_directory_canonicalization.002`: Standard, reference, foundation, planning, and task surfaces that derive `related_paths` or `applies_to` from governed front matter must project canonical repo-relative file-versus-directory syntax.
- `req.governed_front_matter_directory_canonicalization.003`: The live governed corpus, companion standards guidance, templates, and valid front-matter examples must be updated in the same change set so no currently governed directory-valued `applies_to` entry remains non-canonical.
- `req.governed_front_matter_directory_canonicalization.004`: Exact slash-terminated standards lookup must succeed for the currently affected command-doc directory surface and the final expansive review audit must report zero remaining governed directory `applies_to` issues.

## Acceptance Criteria
- `ac.governed_front_matter_directory_canonicalization.001`: Shared governed authoring and validation paths canonicalize or reject directory-valued `applies_to` metadata consistently, with targeted regression coverage for planning scaffolds, task lifecycle writes, and document semantics.
- `ac.governed_front_matter_directory_canonicalization.002`: The standard index and standards query return `std.engineering.cli_help_text` for canonical directory filters on `docs/commands/`, and the live affected docs plus front-matter examples publish slash-terminated directory `applies_to` values.
- `ac.governed_front_matter_directory_canonicalization.003`: `watchtower-core sync all --write --format json`, acceptance validation for this trace, full repository validation, targeted regressions, and the final expansive governed-doc audit all pass with zero remaining issues.

## Risks and Dependencies
- Tightening validation before normalizing the live corpus would fail standard, reference, planning, and task loads immediately, so the code and corpus changes have to land together.
- The final fix depends on derived indexes, trackers, and coordination surfaces being refreshed after the canonical authored paths are written.
- Template and standards guidance must stay aligned with the implementation or future manual authorship could regress even if automated writers normalize inputs.

## References
- docs/standards/metadata/front_matter_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/references/front_matter_reference.md
- docs/references/agent_workflow_authoring_reference.md
