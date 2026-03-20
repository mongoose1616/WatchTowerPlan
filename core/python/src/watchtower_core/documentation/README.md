# `watchtower_core.documentation`

## Summary
Repo-shared helpers for governed Markdown semantics, front-matter path normalization, standard and reference parsing, and other documentation-support logic used by validation and sync services.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: Explicit helper modules such as `front_matter_paths`, `governed_documents`, `markdown_semantics`, `reference_semantics`, and `standards`.
- `Non-Goals`: Live plan workspace orchestration, plan task lifecycle behavior, or plan-pack sync coordination.

## Key Surfaces
- `front_matter_paths.py`: Canonical normalization for path-valued governed front matter.
- `governed_documents.py`: Shared governed-Markdown loading, section-order validation, metadata parsing, and reference-indicator helpers.
- `markdown_semantics.py`: Shared Markdown spacing and heading semantics checks.
- `reference_semantics.py`: Reference-document maturity and touchpoint parsing helpers.
- `standards.py`: Standard-document operationalization and reference-accounting helpers.

## Related Surfaces
- `core/python/src/watchtower_core/validation/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `plan/python/src/watchtower_plan/validation/README.md`
- `requirements.md`
- `decisions.md`
