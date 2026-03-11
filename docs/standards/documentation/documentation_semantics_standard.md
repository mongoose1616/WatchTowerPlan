---
id: "std.documentation.documentation_semantics"
title: "Documentation Semantics Standard"
summary: "This standard defines the cross-family semantic guardrails enforced for governed Markdown documents and workflow modules."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "documentation_semantics"
owner: "repository_maintainer"
updated_at: "2026-03-11T20:38:54Z"
audience: "shared"
authority: "authoritative"
---

# Documentation Semantics Standard

## Summary
This standard defines the cross-family semantic guardrails enforced for governed Markdown documents and workflow modules.

## Purpose
Keep document-level validation fail closed on the small set of semantic rules that should hold across document families rather than only inside one template or one reviewer habit.

## Scope
- Applies to governed Markdown documents and workflow modules validated by `watchtower-core validate document-semantics`.
- Covers repo-local Markdown link integrity and other shared Markdown-semantic guardrails.
- Does not replace family-specific front matter, required section, or section-order standards.

## Use When
- Adding or editing repo-local Markdown links in `docs/**` or `workflows/**`.
- Changing the shared document-semantics validator.
- Reviewing whether authored Markdown still satisfies cross-family semantic guardrails before closeout.

## Related Standards and Sources
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): aggregate repository validation should fail closed when cross-family document semantics break.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): governed standards inherit these semantic guardrails in addition to their family-specific structure rules.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): workflow modules inherit these same guardrails in addition to workflow-specific section rules.
- [commonmark_reference.md](/home/j/WatchTowerPlan/docs/references/commonmark_reference.md): Markdown link interpretation should stay aligned with a stable local reference instead of ad hoc parsing assumptions.

## Guidance
- Repo-local Markdown links should resolve to existing files or directories inside the current repository tree.
- Repo-local Markdown links may use repository-absolute or document-relative targets, but they should not escape the current repository root.
- Pure fragment links and external URLs do not participate in repo-local existence checks.
- Leave one blank line between the last item in a list block and the next heading.
- Apply shared Markdown-semantic rules through common parsing helpers so
  governed validation and derived sync surfaces do not disagree about the same
  authored input.
- Keep cross-family semantic rules here and keep family-specific structure or content rules in the narrower document-family standards.

## Operationalization
- `Modes`: `validation`; `documentation`; `artifact`
- `Operational Surfaces`: `core/python/src/watchtower_core/repo_ops/markdown_semantics.py`; `core/python/src/watchtower_core/repo_ops/planning_documents.py`; `core/python/src/watchtower_core/repo_ops/sync/workflow_index.py`; `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`; `docs/commands/core_python/watchtower_core_validate_document_semantics.md`; `docs/commands/core_python/watchtower_core_validate_all.md`; `core/control_plane/registries/validators/validator_registry.v1.json`

## Validation
- `watchtower-core validate document-semantics` should fail when a repo-local Markdown link target does not exist.
- `watchtower-core validate document-semantics` should fail when a heading immediately follows a list block without a blank separator line.
- Governed Markdown loaders reused by sync or index rebuild surfaces should
  reject the same invalid heading pattern instead of silently accepting it.
- Family-specific semantic validators may add stricter rules, but they should not weaken these shared rules.
- `watchtower-core validate all` should include document-semantics validation by default.

## Change Control
- Update this standard when the repository changes the shared Markdown-semantic guardrails for governed documents or workflow modules.
- Update the document-semantics validator, affected templates, and relevant command docs in the same change set when this standard changes materially.

## References
- [watchtower_core_validate_document_semantics.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_document_semantics.md)
- [watchtower_core_validate_all.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_all.md)
- [commonmark_reference.md](/home/j/WatchTowerPlan/docs/references/commonmark_reference.md)

## Updated At
- `2026-03-11T20:38:54Z`
