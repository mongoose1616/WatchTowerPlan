---
trace_id: trace.documentation_family_lookup_and_readme_template_alignment
id: decision.documentation_family_lookup_and_readme_template_alignment_direction
title: Documentation Family Lookup and README Template Alignment Direction Decision
summary: Records the initial direction decision for Documentation Family Lookup and
  README Template Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T00:58:00Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/templates/readme_template.md
---

# Documentation Family Lookup and README Template Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.documentation_family_lookup_and_readme_template_alignment`
- `Decision ID`: `decision.documentation_family_lookup_and_readme_template_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.documentation_family_lookup_and_readme_template_alignment`
- `Linked Designs`: `design.features.documentation_family_lookup_and_readme_template_alignment`
- `Linked Implementation Plans`: `design.implementation.documentation_family_lookup_and_readme_template_alignment`
- `Updated At`: `2026-03-12T00:58:00Z`

## Summary
Records the initial direction decision for Documentation Family Lookup and README Template Alignment.

## Decision Statement
Standard operationalization metadata will support bounded repo-relative glob patterns, and the affected document-family standards will use those patterns or precise family surfaces so concrete governed files resolve back to their governing standards; the README template will be aligned in the same slice.

## Trigger or Source Request
- Another expansive internal standards review confirmed two live issues: standards lookup cannot reliably resolve several concrete governed docs because operationalization metadata cannot represent repeating filename families or some family-document surfaces, and the README template still drifts from the governed README title contract.

## Current Context and Constraints
- `watchtower-core query standards --operationalization-path docs/references/AGENTS.md --format json` returns only `std.data_contracts.format_selection`, so nested `AGENTS.md` files are not discoverable through `std.documentation.agents_md`.
- `watchtower-core query standards --operationalization-path docs/planning/README.md --format json` omits `std.documentation.readme_md`, and `docs/references/commonmark_reference.md` omits `std.documentation.reference_md`.
- `watchtower-core query standards --operationalization-path docs/standards/documentation/readme_md_standard.md --format json` omits `std.documentation.standard_md`.
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md) still starts with `# \`<Directory Name>\`` and places optional sections before the required inventory scaffold.

## Applied References and Implications
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the standard index must stay authoritative for standards lookup, so the operationalization contract has to express the real governing surfaces.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): operationalization metadata should explain enforcement and embodiment clearly enough that maintainers do not need code spelunking to understand scope.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): the README template must use repo-relative directory-path titles and a compact inventory-first structure.
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md) and [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): recurring documentation families must remain discoverable through standards lookup, not only by manual browsing.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/templates/readme_template.md

## Options Considered
### Option 1
- Keep the current exact-file and directory-descendant operationalization model and enumerate more one-off files in the affected standards.
- Smallest immediate code change.
- Leaves repeating filename families stale-prone and still requires ongoing manual enumeration whenever new governed files are added.

### Option 2
- Add bounded repo-relative glob-pattern support for operationalization metadata and use it for recurring file families, while tightening live standards and template coverage in the same slice.
- Solves the lookup gap once at the contract layer and keeps family standards concise and maintainable.
- Requires coordinated updates across parser, query behavior, docs, and regression tests.

## Chosen Outcome
Accept Option 2. Extend operationalization metadata to allow bounded repo-relative glob patterns that match live repository surfaces, preserve existing exact and directory semantics, update the affected family standards to publish precise operationalization coverage, and align the README template in the same traced slice.

## Rationale and Tradeoffs
- One contract-level enhancement is more maintainable than growing a list of one-off README and AGENTS files across the standards corpus.
- The approach keeps standards lookup generic and reusable instead of adding family-specific hard-coded branching.
- The tradeoff is a slightly richer operationalization model, but it stays bounded to repo-relative patterns and retains string compatibility in the standard index.

## Consequences and Follow-Up Impacts
- The standards parser, standard-index sync, document semantics, and standards query behavior must all agree on the new operationalization-pattern semantics.
- The AGENTS, README, reference, and standard document-family standards need same-change operationalization updates.
- The README template and artifact tests need same-change alignment so authoring guidance stops encouraging non-compliant README titles.

## Risks, Dependencies, and Assumptions
- Root-level `README.md` and `AGENTS.md` still need explicit exact entries because nested glob patterns do not match root files.
- The new pattern support must remain repo-relative and must fail closed when a pattern matches no live repository surface.

## Open Questions
- None. The bounded glob-pattern approach is the recommended direction for this slice.

## References
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/documentation/compact_document_authoring_standard.md
