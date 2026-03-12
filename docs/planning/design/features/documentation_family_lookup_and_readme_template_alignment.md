---
trace_id: trace.documentation_family_lookup_and_readme_template_alignment
id: design.features.documentation_family_lookup_and_readme_template_alignment
title: Documentation Family Lookup and README Template Alignment Feature Design
summary: Defines the technical design boundary for Documentation Family Lookup and
  README Template Alignment.
type: feature_design
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T00:58:00Z'
audience: shared
authority: authoritative
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

# Documentation Family Lookup and README Template Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.documentation_family_lookup_and_readme_template_alignment`
- `Design ID`: `design.features.documentation_family_lookup_and_readme_template_alignment`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.documentation_family_lookup_and_readme_template_alignment`
- `Linked Decisions`: `decision.documentation_family_lookup_and_readme_template_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.documentation_family_lookup_and_readme_template_alignment`
- `Updated At`: `2026-03-12T00:58:00Z`

## Summary
Defines the technical design boundary for Documentation Family Lookup and README Template Alignment.

## Source Request
- Another expansive internal standards review confirmed two live issues: standards lookup cannot reliably resolve several concrete governed docs because operationalization metadata cannot represent repeating filename families or some family-document surfaces, and the README template still drifts from the governed README title contract.

## Scope and Feature Boundary
- Covers standard operationalization parsing and query matching, the affected live document-family standards, the standards query command docs, and the README template plus regression tests.
- Excludes new query families, new document validators for README or AGENTS files, and unrelated document-family restructures.

## Current-State Context
- Standard lookup already supports exact operationalization files and directory descendants, but it cannot express repeating filename families such as nested `README.md` or `AGENTS.md`.
- Several family standards omit the concrete document families they govern from `Operational Surfaces`, so concrete reference and standard docs do not resolve back to their own family standards.
- The README template still suggests a generic title placeholder instead of the repo-relative directory-path title the README standard requires.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): prefer one reusable contract improvement over growing special-case enumerations for individual files.

## Internal Standards and Canonical References Applied
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): operationalization metadata must stay queryable and auditable through the derived standard index.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): operationalization metadata must stay precise enough to explain how a standard is enforced or embodied locally.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): README authoring must use repo-relative directory-path titles and a compact inventory-first shape.
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md) and [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): recurring documentation families must remain discoverable through the standards corpus.

## Design Goals and Constraints
- Add the smallest operationalization-contract change that fixes real lookup gaps without weakening existing exact or directory semantics.
- Avoid hard-coded special cases for README, AGENTS, reference, or standard documents in query code.
- Preserve existing standard-index schema compatibility by continuing to publish operationalization values as strings.

## Options Considered
### Option 1
- Keep exact-file and directory-only operationalization semantics and enumerate more individual files in the affected standards.
- Minimal code change.
- Still leaves recurring file families stale-prone and forces manual enumeration every time a new governed README or AGENTS file appears.

### Option 2
- Allow bounded repo-relative glob patterns in standard operationalization metadata and use them where repeating filename families or precise family-document coverage need them.
- Keeps the contract compact, reusable, and expressive enough for concrete governed file lookup.
- Requires coordinated updates across parser, query behavior, standards docs, command docs, and regression coverage.

## Recommended Design
### Architecture
- Extend the standard operationalization helper layer so it can validate and preserve three surface types: exact files, directories, and bounded repo-relative glob patterns.
- Teach the standards query service to match a requested concrete path against exact paths, directory descendants, and published glob patterns without adding family-specific branching.
- Update the affected live standards to publish precise family coverage through their `Operational Surfaces` metadata, then align the README template with the README family contract.

### Data and Interface Impacts
- Standard-index entries may now legitimately contain bounded repo-relative glob patterns in `operationalization_paths`.
- `watchtower-core query standards --operationalization-path` documentation and help text must describe exact, directory-descendant, and glob-pattern matching behavior.
- Artifact tests need to assert both the new operationalization coverage and the corrected README template shape.

### Execution Flow
1. Parse `Operational Surfaces` metadata, preserving exact paths and directories while validating that any glob pattern is repo-relative and matches at least one live repository surface.
2. Match `--operationalization-path` requests against the indexed exact paths, directory prefixes, and glob patterns.
3. Update the affected standards and template surfaces, then prove the lookup and authoring behavior with unit and integration coverage.

### Invariants and Failure Cases
- Existing exact-path and directory-descendant query behavior must remain unchanged for already-indexed standards.
- Invalid operationalization glob patterns must fail validation and sync rather than silently entering the standard index.
- Root-level recurring files such as `README.md` and `AGENTS.md` must stay resolvable even though `**/README.md` and `**/AGENTS.md` do not match root files.

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

## Design Guardrails
- Keep glob support bounded to standard operationalization metadata; do not broaden unrelated query filters in the same slice.
- Update docs, tests, and derived lookup surfaces in the same change set as the parser and query behavior.

## Risks
- Glob matching semantics can be easy to misread, so the live standards should pair exact root-file entries with nested-family glob entries where needed.

## References
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/documentation/compact_document_authoring_standard.md
