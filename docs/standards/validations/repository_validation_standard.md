---
id: "std.validations.repository_validation"
title: "Repository Validation Standard"
summary: "This standard defines the baseline validation expectations for repository changes across governed documents, governed artifacts, and the Python helper workspace."
type: "standard"
status: "active"
tags:
  - "standard"
  - "validations"
  - "repository_validation"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/"
  - "core/control_plane/"
  - "docs/"
  - "workflows/"
aliases:
  - "repo validation baseline"
  - "validation baseline"
---

# Repository Validation Standard

## Summary
This standard defines the baseline validation expectations for repository changes across governed documents, governed artifacts, and the Python helper workspace.

## Purpose
- Make validation expectations explicit instead of leaving them only in command docs or reviewer memory.
- Keep governed human-readable and machine-readable surfaces aligned before closeout.
- Preserve the local-first, fail-closed posture described in the foundations.

## Scope
- Applies to governed Markdown documents, governed JSON artifacts, derived indexes and trackers, and the Python helper workspace.
- Covers baseline validation commands and when narrower versus broader validation is expected.
- Does not redefine domain-specific validation beyond the current repository surfaces.

## Use When
- Preparing a non-trivial change for closeout.
- Reviewing whether a change set has enough validation evidence.
- Defining or updating local automation that checks repository health.

## Related Standards and Sources
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): document-semantics validation should fail closed on shared Markdown guardrails such as repo-local link integrity.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): Python validation commands should run from the canonical workspace using the standard local environment.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): validation should stay aligned with same-change-set updates across docs, code, and governed artifacts.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): schema-backed surfaces should fail closed when malformed.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): durable evidence should be recorded when a validation flow writes governed proof.
- [watchtower_core_validate_all.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_all.md): documents the aggregate validation command that operationalizes the current baseline.
- [watchtower_core_sync_all.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_all.md): derived local state should be regenerated before broad validation when the change touches generated trackers or indexes.

## Guidance
- Use the narrowest meaningful validation while working.
- Before closeout for non-trivial changes, run the broadest meaningful validation for the touched surfaces.
- When derived trackers or indexes changed, run `watchtower-core sync all --write` before the final broad validation pass.
- Use `watchtower-core validate all` as the baseline aggregate validation for governed docs, governed artifacts, and acceptance reconciliation.
- Treat broken repo-local Markdown links as validation failures, not reviewer-only cleanup.
- Use `watchtower-core validate artifact --schema-id ... --supplemental-schema-path ...` when you need bounded validation of external artifacts or pack-owned interfaces without changing the canonical validator registry.
- When `core/python/**` changes, the normal workspace validation baseline is:
  - `./.venv/bin/python -m mypy src`
  - `./.venv/bin/ruff check src tests/unit tests/integration`
  - `./.venv/bin/python -m pytest`
- When a change is docs-only and does not affect the Python workspace, narrower validation may be sufficient if the touched surfaces remain within governed Markdown or derived-index boundaries.
- Validation results should be summarized in closeout metadata or pull-request metadata for non-trivial changes.

## Structure or Data Model
### Validation tiers
| Tier | Use When | Typical Commands |
|---|---|---|
| Narrow | Local work-in-progress checks for one surface | `watchtower-core validate front-matter`, `watchtower-core validate artifact`, targeted tests |
| Broad | Pre-closeout validation for one non-trivial change set | `watchtower-core sync all --write`, `watchtower-core validate all`, plus Python workspace checks when code changed |
| Evidence-writing | Validation flows that publish durable proof | Validator-specific commands that record validation evidence |

## Operationalization
- `Modes`: `validation`; `documentation`; `sync`
- `Operational Surfaces`: `core/python/src/watchtower_core/repo_ops/validation/all.py`; `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`; `docs/commands/core_python/watchtower_core_validate_all.md`; `docs/commands/core_python/watchtower_core_sync_all.md`

## Validation
- Reviewers should reject non-trivial changes that skip the broad validation tier without an explicit reason.
- Generated trackers and indexes should not be validated against stale source state.
- Python helper changes should not close out without typecheck, lint, and test coverage unless the exception is explicit.

## Change Control
- Update this standard when the repository changes its baseline validation commands or required validation tiers.
- Update command docs, local automation, and related workflows in the same change set when this validation contract changes materially.

## References
- [watchtower_core_validate_all.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_all.md)
- [watchtower_core_sync_all.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_all.md)
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)

## Updated At
- `2026-03-11T06:00:00Z`
