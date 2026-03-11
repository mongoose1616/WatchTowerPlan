---
trace_id: trace.standard_authoring_surface_alignment
id: prd.standard_authoring_surface_alignment
title: Standard Authoring Surface Alignment PRD
summary: Aligns the governed standard-authoring scaffold, lookup surfaces, and regression
  coverage with the live standard-document contract.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T20:05:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/standard_md_standard.md
- docs/templates/standard_document_template.md
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
- core/control_plane/indexes/standards/standard_index.v1.json
- docs/commands/core_python/watchtower_core_query_standards.md
---

# Standard Authoring Surface Alignment PRD

## Record Metadata
- `Trace ID`: `trace.standard_authoring_surface_alignment`
- `PRD ID`: `prd.standard_authoring_surface_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.standard_authoring_surface_alignment_direction`
- `Linked Designs`: `design.features.standard_authoring_surface_alignment`
- `Linked Implementation Plans`: `design.implementation.standard_authoring_surface_alignment`
- `Updated At`: `2026-03-11T20:05:00Z`

## Summary
Aligns the governed standard-authoring scaffold, lookup surfaces, and regression coverage with the live standard-document contract.

## Problem Statement
The standards review reproduced two live authoring-surface defects in the standards family. First, [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md) is stale against the governed [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md) and the current semantic validator. The template omits required sections such as `Scope`, `Use When`, `Related Standards and Sources`, `Operationalization`, and `Updated At`, and it incorrectly tells authors that some of those sections are optional. That means the repo’s canonical scaffold for new standards actively encourages outputs that would violate the documented standard-document contract.

Second, the governing standard itself does not publish the standard-authoring template as one of its operational surfaces. That omission propagates into the standard index and standards query surfaces. A direct reproduction using `watchtower-core query standards --operationalization-path docs/templates/standard_document_template.md --format json` returns zero results today, even though the standard template is the primary authoring scaffold for the governed standard-document family. This leaves the repo without a reliable lookup path from the template to its governing standard.

Together these defects weaken the standards family at the point contributors actually start authoring. The canonical template drifts from the live contract, the standard index underreports the standard’s real operational surfaces, and there is no automated regression coverage to keep that authoring boundary aligned in future changes.

## Goals
- Make the governed standard-document template match the live standard-document contract and validator expectations.
- Ensure the Standard Document Standard publishes and indexes its authoring scaffold as a real operational surface.
- Add regression coverage that fails closed when the template or standards lookup surface drifts again.
- Close the trace on a green repository validation baseline.

## Non-Goals
- Redesigning the broader standards family beyond the standard-document authoring seam reproduced here.
- Changing the schema shape of the standard index.
- Reworking unrelated documentation templates that were not found to be out of contract in this review.
- Changing the behavior of standards query beyond what is already implied by corrected indexed source data.

## Requirements
- `req.standard_authoring_surface_alignment.001`: This trace must publish a real PRD, accepted direction decision, feature design, implementation plan, refreshed acceptance contract, refreshed planning-baseline evidence, a closed bootstrap task, and bounded execution tasks covering the confirmed authoring-surface defects.
- `req.standard_authoring_surface_alignment.002`: The standard-document template must present the required standard-document sections and authoring guidance that the governed standard and semantic validator currently require, including explained `Related Standards and Sources`, `Operationalization`, and `Updated At`.
- `req.standard_authoring_surface_alignment.003`: The Standard Document Standard must treat `docs/templates/standard_document_template.md` as a real companion authoring surface so the standard index and standards query surfaces can resolve that template back to its governing standard.
- `req.standard_authoring_surface_alignment.004`: Regression coverage must fail closed if the standard template drops required standard-document sections again or if querying by the standard template operationalization path stops returning the governing standard.
- `req.standard_authoring_surface_alignment.005`: The repository must return to a green baseline on `./.venv/bin/watchtower-core validate acceptance --trace-id trace.standard_authoring_surface_alignment --format json`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check`.

## Acceptance Criteria
- `ac.standard_authoring_surface_alignment.001`: The trace publishes the full planning chain, the accepted direction decision, the refreshed acceptance contract and planning-baseline evidence, the closed bootstrap task, and two bounded execution tasks for template-contract alignment and standards lookup alignment.
- `ac.standard_authoring_surface_alignment.002`: The standard-document template now includes the required standard-document sections and guidance needed to author a standards-valid governed standard without relying on out-of-band tribal knowledge.
- `ac.standard_authoring_surface_alignment.003`: The Standard Document Standard and derived standard index now include `docs/templates/standard_document_template.md` as an operational surface, and querying standards by that path returns `std.documentation.standard_md`.
- `ac.standard_authoring_surface_alignment.004`: Regression tests prove the standard template stays aligned with the governed standard-document contract and the standards query surface preserves the template operationalization lookup.
- `ac.standard_authoring_surface_alignment.005`: The repository passes `./.venv/bin/watchtower-core validate acceptance --trace-id trace.standard_authoring_surface_alignment --format json`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check` after the trace closes.

## Risks and Dependencies
- Template fixes can drift again if the repo continues to treat templates as editorial-only artifacts instead of contract-carrying authoring surfaces.
- The lookup fix depends on keeping the standard document itself, the standard index, and query tests aligned in one slice; patching only the template would leave the standards query gap intact.
- Regression coverage needs to be specific enough to catch future authoring-surface drift without becoming a brittle snapshot of unrelated documentation wording.

## Foundations References Applied
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the canonical authoring scaffold should reinforce the governed contract rather than silently narrowing or weakening it.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): authoring entrypoints and lookup surfaces should have one explicit, tested contract instead of diverging by accident.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/templates/standard_document_template.md
- docs/commands/core_python/watchtower_core_query_standards.md
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
