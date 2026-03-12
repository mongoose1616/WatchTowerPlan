---
trace_id: trace.governed_front_matter_directory_canonicalization
id: decision.governed_front_matter_directory_canonicalization.direction
title: Governed Front Matter Directory Canonicalization Direction Decision
summary: Records the initial direction decision for Governed Front Matter Directory
  Canonicalization.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T02:46:38Z'
audience: shared
authority: supporting
applies_to:
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
---

# Governed Front Matter Directory Canonicalization Direction Decision

## Record Metadata
- `Trace ID`: `trace.governed_front_matter_directory_canonicalization`
- `Decision ID`: `decision.governed_front_matter_directory_canonicalization.direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.governed_front_matter_directory_canonicalization`
- `Linked Designs`: `design.features.governed_front_matter_directory_canonicalization`
- `Linked Implementation Plans`: `design.implementation.governed_front_matter_directory_canonicalization`
- `Updated At`: `2026-03-12T02:46:38Z`

## Summary
Records the initial direction decision for Governed Front Matter Directory Canonicalization.

## Decision Statement
Use one shared canonicalization helper for path-valued governed `applies_to` metadata, auto-normalize write-time directory inputs, reject non-canonical authored path syntax during validation and sync, and normalize the current governed corpus in the same slice.

## Trigger or Source Request
- Execute the internal project standards review loop until no new issues are identified.

## Current Context and Constraints
- The review reproduced a real user-visible miss: canonical slash-terminated directory filters on `watchtower-core query standards` did not resolve `std.engineering.cli_help_text` because the live standard authored `docs/commands` and `core/python/src/watchtower_core/cli` without trailing slashes.
- The broader audit found 11 governed Markdown docs and 2 valid front-matter examples with the same non-canonical directory pattern.
- Planning scaffolds and task lifecycle writes could still reproduce the drift, while semantic validation and sync did not share one common `applies_to` path rule.

## Applied References and Implications
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): governed `applies_to` metadata is the authoritative place to define canonical repo-relative file-versus-directory syntax.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): exact standards lookup depends on canonical authored `applies_to` values and canonical derived `related_paths`.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the canonicalization logic and regressions should live in the shared Python workspace instead of ad hoc scripts.

## Affected Surfaces
- docs/
- core/python/src/watchtower_core/
- core/control_plane/

## Options Considered
### Option 1
- Normalize only the currently affected live docs and examples.
- Strength: minimal code churn.
- Tradeoff: leaves the authoring recurrence vector and shared validation gap unresolved.

### Option 2
- Add fuzzy or normalized query matching while leaving authored governed metadata unchanged.
- Strength: hides the reproduced standards-query failure quickly.
- Tradeoff: preserves corpus drift and leaves derived indexes inconsistent with published front-matter guidance.

### Option 3
- Add one shared canonicalization helper, use it in authoring and load paths, fail closed on non-canonical authored docs during validation and sync, and normalize the live governed corpus in the same slice.
- Strength: fixes the current corpus, the exact standards-query miss, and the recurrence path together.
- Tradeoff: requires coordinated changes across code, standards guidance, templates, examples, and derived artifacts.

## Chosen Outcome
Option 3 is accepted.

## Rationale and Tradeoffs
- Exact path lookup is already documented in canonical slash-terminated form, so the durable fix is to canonicalize authored metadata rather than loosening query semantics.
- Centralizing the rule in one helper keeps standards, references, foundations, planning docs, and tasks from drifting through family-specific parsing code.
- Auto-normalizing write-time inputs keeps authoring ergonomic, while fail-closed validation prevents hand-edited non-canonical docs from silently repopulating bad index data.

## Consequences and Follow-Up Impacts
- Live governed docs, valid front-matter examples, and templates need slash-terminated directory `applies_to` values where they represent directories.
- Standards, reference, foundation, planning, task, and coordination surfaces will republish canonical derived paths after sync.
- Final closeout requires a no-new-issues audit proving that no governed directory `applies_to` entries remain non-canonical.

## Risks, Dependencies, and Assumptions
- The change depends on refreshing derived artifacts immediately after the authored corpus is normalized.
- This direction assumes slash-containing governed `applies_to` entries are intended to reference live repo-local paths rather than arbitrary concepts.
- Tightening validation may expose additional drift during the final audit; the initiative should not close until that audit is clean.

## References
- docs/standards/metadata/front_matter_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/engineering/python_workspace_standard.md
