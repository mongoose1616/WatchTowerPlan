---
trace_id: trace.standard_operationalization_directory_canonicalization
id: decision.standard_operationalization_directory_canonicalization_direction
title: Standard Operationalization Directory Canonicalization Direction Decision
summary: Records the initial direction decision for Standard Operationalization Directory
  Canonicalization.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T02:06:54Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/control_plane/indexes/standards/standard_index.v1.json
---

# Standard Operationalization Directory Canonicalization Direction Decision

## Record Metadata
- `Trace ID`: `trace.standard_operationalization_directory_canonicalization`
- `Decision ID`: `decision.standard_operationalization_directory_canonicalization_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.standard_operationalization_directory_canonicalization`
- `Linked Designs`: `design.features.standard_operationalization_directory_canonicalization`
- `Linked Implementation Plans`: `design.implementation.standard_operationalization_directory_canonicalization`
- `Updated At`: `2026-03-12T02:06:54Z`

## Summary
Records the initial direction decision for Standard Operationalization Directory Canonicalization.

## Decision Statement
Standard operationalization metadata will treat exact files and directories as distinct canonical path forms: exact files stay repo-relative and slash-free, directories must end in `/`, and non-canonical directory spellings will fail validation before they reach the standard index.

## Trigger or Source Request
- Another expansive internal standards review reproduced one live defect: [cli_help_text_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/cli_help_text_standard.md) publishes both `docs/commands` and `docs/commands/`, and the current parser/sync path preserves that semantic duplicate in the governed standard index.

## Current Context and Constraints
- `parse_standard_operationalization(...)` already validates existence and bounded glob behavior, so the smallest coherent fix is to tighten canonical path syntax at the shared parser boundary rather than adding downstream index cleanup.
- The standard authoring contract and template need same-change alignment so the corpus does not keep encouraging non-canonical directory syntax after the parser becomes stricter.

## Applied References and Implications
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): operationalization metadata should remain precise, auditable, and free of ambiguous path forms in live standards.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the derived standard index should not publish semantically duplicate operationalization paths for one standard entry.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the repository should fail closed at the shared contract layer instead of normalizing bad inputs silently after they leave the authored standards corpus.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/control_plane/indexes/standards/standard_index.v1.json

## Options Considered
### Option 1
- Silently normalize directory paths during sync while leaving the authored standards corpus free to mix slash and non-slash directory spellings.
- Keeps downstream output canonical even when authors drift.
- Leaves the standards corpus inconsistent and weakens `watchtower-core validate all` as a standards-authoring guardrail.

### Option 2
- Make canonical operationalization syntax a governed validation rule, update the live standards and template to match it, and protect the behavior with regression coverage.
- Prevents semantically duplicate directory metadata from entering the standard index and keeps authoring guidance aligned with enforcement.
- Requires same-change coordination across parser logic, standards docs, the template, tests, and derived tracker surfaces.

## Chosen Outcome
Accept Option 2. Tighten the shared standards parser so non-canonical directory paths fail validation, align the live standards corpus and authoring template on canonical file-or-directory syntax, and prove the behavior with unit and integration regressions before closeout.

## Rationale and Tradeoffs
- The defect is rooted in ambiguous authored metadata, so the authoritative fix belongs at the validation boundary rather than in a downstream cleanup step.
- Making canonical path syntax explicit improves both the human guidance and the machine-readable standard index with one bounded contract change.
- The tradeoff is stricter validation for standards authors, but the corpus has only one reproduced live defect and the stricter rule closes an avoidable class of drift.

## Consequences and Follow-Up Impacts
- The shared parser, document-semantics validation, and standard-index sync now need to agree on the same canonical file-or-directory path rule.
- [cli_help_text_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/cli_help_text_standard.md), [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md), and [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md) need same-change updates so guidance matches enforcement.
- The final review pass must confirm there are no other live standards still publishing non-canonical operationalization paths.

## Risks, Dependencies, and Assumptions
- Any latent non-canonical directory path elsewhere in the live standards corpus will now fail validation immediately, which is intentional but increases the importance of the post-fix review pass.
- The closeout depends on refreshing the standard index, planning trackers, and traceability joins after task transitions and initiative closeout.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
