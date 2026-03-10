---
trace_id: "trace.template_and_output_efficiency"
id: "design.implementation.template_and_output_efficiency_execution"
title: "Template and Output Efficiency Implementation Plan"
summary: "Breaks the template and output efficiency initiative into compact authoring, tracker compaction, and workflow-guidance slices."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:00:54Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/templates/"
  - "workflows/modules/"
  - "core/python/src/watchtower_core/repo_ops/"
  - "core/python/tests/"
aliases:
  - "template efficiency plan"
---

# Template and Output Efficiency Implementation Plan

## Record Metadata
- `Trace ID`: `trace.template_and_output_efficiency`
- `Plan ID`: `design.implementation.template_and_output_efficiency_execution`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.template_and_output_efficiency`
- `Source Designs`: `design.features.compact_document_authoring_and_tracking`
- `Linked Acceptance Contracts`: `contract.acceptance.template_and_output_efficiency`
- `Updated At`: `2026-03-10T16:00:54Z`

## Summary
Breaks the template and output efficiency initiative into compact authoring, tracker compaction, and workflow-guidance slices.

## Source Request or Design
- Feature design: [compact_document_authoring_and_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/features/compact_document_authoring_and_tracking.md)
- PRD: [template_and_output_efficiency.md](/home/j/WatchTowerPlan/docs/planning/prds/template_and_output_efficiency.md)
- User request to start a new initiative, complete the related work, and commit each succinct slice.

## Scope Summary
- Add a durable compact-authoring rule and align planning, decision, and generic documentation templates with their governed outputs.
- Relax low-value required sections in planning and task validation where machine authority already exists elsewhere.
- Compact generated planning trackers without weakening their routing value.
- Tighten workflow instructions that currently encourage excessive content.

## Assumptions and Constraints
- Existing governed machine surfaces remain the authority for IDs, status, and lookup.
- The change should remain backward compatible with the current planning corpus rather than forcing bulk rewrites.
- Each slice should land in a coherent commit and keep the repo green.

## Current-State Context
- Template-machine misalignment already exists in PRD and decision templates because their outputs require front matter that the templates omit.
- Planning-document validators already centralize section requirements, so compact-authoring changes can be made in one place and flow into index sync logic.
- Generated trackers are deterministic and already have test coverage, which makes compact renderer changes straightforward to validate.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): keep the work modular, tested, and companion-surface aligned.
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): regenerate derived trackers and indexes before the final validation pass.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): compact human output should not change source-of-truth boundaries.

## Proposed Technical Approach
- Extend planning-document helper utilities so explained-bullet sections can be optional when present, not universally required.
- Update templates and standards in the same slice so the authoring guidance, validator rules, and generated index assumptions remain aligned.
- Refactor tracker sync services toward compact zero-state text and conditional columns rather than verbose repeated scaffolding.
- Tighten workflow module wording to optimize for proportional repository output rather than generic documentation ceremony.

## Work Breakdown
1. Bootstrap the traced planning chain, acceptance contract, planning evidence, and bounded task set for this initiative.
2. Add the compact-authoring standard, align planning and documentation templates with their governed families, and relax validator requirements where optional sections should truly be optional.
3. Compact the generated planning trackers and add regression coverage for zero-state and low-signal cases.
4. Tighten workflow-module instructions so documentation and planning routes explicitly prefer the smallest useful output for the current scope.
5. Rerun validation, close the tasks, and close the initiative.

## Dependencies
- `watchtower_core` planning-document and task-document loaders.
- Current planning tracker sync services and indexes.
- Current documentation and planning standards under `docs/standards/`.

## Risks
- Compact authoring rules could drift from sync and index behavior if the standards and code are not updated in the same slice.
- Tracker compaction may require a few targeted test rewrites where assertions currently expect verbose footer scaffolding.

## Validation Plan
- Run `uv run watchtower-core sync all --write --format json` after planning, standards, or sync-renderer changes.
- Run `uv run pytest -q`, `uv run mypy src`, `uv run ruff check .`, `uv run watchtower-core validate all --format json`, and `uv run watchtower-core doctor --format json` after each implementation slice.
- Add targeted tests for lean planning semantics and compact tracker rendering where the existing suite does not already cover them.

## Rollout or Migration Plan
- Land one planning bootstrap commit first.
- Land one commit for compact authoring and validation alignment.
- Land one commit for tracker compaction.
- Land one commit for workflow-guidance tightening.
- Land a final planning closeout commit once the repo is green.

## Open Questions
- None. The initiative is bounded to repository-local guidance, validation, and generated output behavior.

## References
- [template_and_output_efficiency.md](/home/j/WatchTowerPlan/docs/planning/prds/template_and_output_efficiency.md)
- [compact_document_authoring_and_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/features/compact_document_authoring_and_tracking.md)

## Updated At
- `2026-03-10T16:00:54Z`
