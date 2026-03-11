---
id: task.standard_authoring_surface_alignment.lookup_alignment.001
trace_id: trace.standard_authoring_surface_alignment
title: Expose the standard authoring template through standards lookup and regression
  coverage
summary: Publish the standard template as a real operational surface of the Standard
  Document Standard and add regression checks for the resulting query path.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T20:04:18Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/standard_md_standard.md
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
related_ids:
- prd.standard_authoring_surface_alignment
- design.features.standard_authoring_surface_alignment
- design.implementation.standard_authoring_surface_alignment
- decision.standard_authoring_surface_alignment_direction
- contract.acceptance.standard_authoring_surface_alignment
---

# Expose the standard authoring template through standards lookup and regression coverage

## Summary
Publish the standard template as a real operational surface of the Standard Document Standard and add regression checks for the resulting query path.

## Scope
- Add the standard-document template to the governing standard's companion and operationalization surfaces.
- Add regression coverage for template contract alignment and standards query lookup by the template path.

## Done When
- Querying standards by docs/templates/standard_document_template.md returns std.documentation.standard_md.
- Regression tests fail closed if the template operationalization path or required template sections drift again.
- Derived standard-index and planning surfaces are refreshed.
