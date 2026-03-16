---
id: task.documentation_family_lookup_and_readme_template_alignment.readme_template_alignment.001
trace_id: trace.documentation_family_lookup_and_readme_template_alignment
title: Align README template with governed title and inventory contract
summary: Update the README template and artifact coverage to follow the repo-relative
  title and inventory-first README standard.
type: task
status: active
task_status: done
task_kind: documentation
priority: medium
owner: repository_maintainer
updated_at: '2026-03-12T00:57:23Z'
audience: shared
authority: authoritative
applies_to:
- docs/templates/readme_template.md
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/standards/documentation/readme_md_standard.md
related_ids:
- prd.documentation_family_lookup_and_readme_template_alignment
- design.features.documentation_family_lookup_and_readme_template_alignment
- design.implementation.documentation_family_lookup_and_readme_template_alignment
- decision.documentation_family_lookup_and_readme_template_alignment_direction
- contract.acceptance.documentation_family_lookup_and_readme_template_alignment
---

# Align README template with governed title and inventory contract

## Summary
Update the README template and artifact coverage to follow the repo-relative title and inventory-first README standard.

## Scope
- Replace the README template title placeholder with the governed repo-relative directory-path title form.
- Move the required inventory scaffold ahead of optional README sections so the template follows the documented family shape.
- Add artifact coverage so future README template drift is caught.

## Done When
- The README template reflects the governed title and section-order contract.
- Artifact tests assert the corrected README template guidance.
