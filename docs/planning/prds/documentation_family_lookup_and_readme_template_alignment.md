---
trace_id: trace.documentation_family_lookup_and_readme_template_alignment
id: prd.documentation_family_lookup_and_readme_template_alignment
title: Documentation Family Lookup and README Template Alignment PRD
summary: Allow standards operationalization metadata to cover repeating documentation
  filename families, repair missing family lookup coverage for AGENTS/README/reference/standard
  docs, and align the README template with the governed title contract.
type: prd
status: active
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

# Documentation Family Lookup and README Template Alignment PRD

## Record Metadata
- `Trace ID`: `trace.documentation_family_lookup_and_readme_template_alignment`
- `PRD ID`: `prd.documentation_family_lookup_and_readme_template_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.documentation_family_lookup_and_readme_template_alignment_direction`
- `Linked Designs`: `design.features.documentation_family_lookup_and_readme_template_alignment`
- `Linked Implementation Plans`: `design.implementation.documentation_family_lookup_and_readme_template_alignment`
- `Updated At`: `2026-03-12T00:58:00Z`

## Summary
Allow standards operationalization metadata to cover repeating documentation filename families, repair missing family lookup coverage for AGENTS/README/reference/standard docs, and align the README template with the governed title contract.

## Problem Statement
- `watchtower-core query standards --operationalization-path docs/planning/README.md --format json` does not return `std.documentation.readme_md`, even though the README standard governs that file family.
- `watchtower-core query standards --operationalization-path docs/references/AGENTS.md --format json` returns only `std.data_contracts.format_selection`, so nested `AGENTS.md` files are not discoverable through the AGENTS standard.
- `watchtower-core query standards --operationalization-path docs/references/commonmark_reference.md --format json` does not return `std.documentation.reference_md`, and `docs/standards/documentation/readme_md_standard.md` does not return `std.documentation.standard_md`, because those family standards do not operationalize the governed document families themselves.
- [readme_template.md](/home/j/WatchTowerPlan/docs/templates/readme_template.md) still uses a generic `<Directory Name>` title placeholder and places optional sections ahead of the required inventory, which drifts from the governed README contract.

## Goals
- Make `watchtower-core query standards --operationalization-path <concrete_path>` return the governing family standards for representative concrete `AGENTS.md`, `README.md`, reference, and standard documents.
- Extend standard operationalization metadata so repeating filename families can be represented without hard-coding an ever-growing list of exact files.
- Align the README template with the governed title and inventory-first authoring contract.

## Non-Goals
- Introduce a new query command or a second standards lookup surface.
- Add a generic validator for every README or AGENTS file in the repository.
- Re-scope unrelated document families whose lookup coverage already resolves through exact files or directories.

## Requirements
- `req.documentation_family_lookup_and_readme_template_alignment.001`: Standard operationalization metadata and standards-path query behavior must support bounded repo-relative glob patterns in addition to exact files and directory descendants.
- `req.documentation_family_lookup_and_readme_template_alignment.002`: The AGENTS, README, reference, and standard document-family standards must publish operationalization coverage precise enough that representative concrete governed files resolve back to those standards.
- `req.documentation_family_lookup_and_readme_template_alignment.003`: The README template must use the repo-relative directory-path title convention and keep the required inventory scaffold ahead of optional sections.

## Acceptance Criteria
- `ac.documentation_family_lookup_and_readme_template_alignment.001`: `watchtower-core query standards --operationalization-path docs/references/AGENTS.md --format json` returns `std.documentation.agents_md`, and `docs/planning/README.md` returns `std.documentation.readme_md`.
- `ac.documentation_family_lookup_and_readme_template_alignment.002`: `watchtower-core query standards --operationalization-path docs/references/commonmark_reference.md --format json` returns `std.documentation.reference_md`, and `docs/standards/documentation/readme_md_standard.md` returns `std.documentation.standard_md`.
- `ac.documentation_family_lookup_and_readme_template_alignment.003`: Standard-index sync and document-semantics validation accept the updated operationalization metadata and preserve the published glob patterns in the derived index.
- `ac.documentation_family_lookup_and_readme_template_alignment.004`: The README template uses `# \`<repo-relative-directory-path>\`` and keeps the inventory scaffold immediately after `Description`, with artifact tests covering the alignment.

## Risks and Dependencies
- `PurePosixPath.match` semantics differ between root and nested paths, so root `README.md` and `AGENTS.md` need explicit exact coverage alongside nested glob coverage.
- The standard-index and command-doc contracts must stay synchronized with the new operationalization-pattern semantics in the same change set.

## References
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/documentation/compact_document_authoring_standard.md
