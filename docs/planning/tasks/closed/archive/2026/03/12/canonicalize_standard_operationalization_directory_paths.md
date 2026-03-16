---
id: task.standard_operationalization_directory_canonicalization.implementation.001
trace_id: trace.standard_operationalization_directory_canonicalization
title: Canonicalize standard operationalization directory paths
summary: Hardens standard operationalization parsing, aligns the CLI help standard
  with canonical directory syntax, and adds regression coverage for duplicate directory-path
  drift.
type: task
status: active
task_status: done
task_kind: bug
priority: medium
owner: repository_maintainer
updated_at: '2026-03-12T02:17:16Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/standards.py
- docs/standards/engineering/cli_help_text_standard.md
- docs/standards/documentation/standard_md_standard.md
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
related_ids:
- prd.standard_operationalization_directory_canonicalization
- design.features.standard_operationalization_directory_canonicalization
- design.implementation.standard_operationalization_directory_canonicalization
- decision.standard_operationalization_directory_canonicalization_direction
- contract.acceptance.standard_operationalization_directory_canonicalization
---

# Canonicalize standard operationalization directory paths

## Summary
Hardens standard operationalization parsing, aligns the CLI help standard with canonical directory syntax, and adds regression coverage for duplicate directory-path drift.

## Scope
- Canonicalize directory operationalization path handling in the governed standards parser and validation path.
- Align the CLI help standard and standard-document guidance to one canonical directory-path form.
- Add regression coverage for live and fixture-driven duplicate directory operationalization paths.

## Done When
- Directory operationalization paths are canonicalized and semantically duplicate directory entries cannot reach the standard index.
- The governing standards corpus publishes canonical directory-path syntax for this slice.
- Regression tests cover fixture and live-corpus protection for duplicate directory operationalization paths.
