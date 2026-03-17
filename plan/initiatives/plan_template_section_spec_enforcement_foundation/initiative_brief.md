# Plan Template Section-Spec Enforcement Foundation

## Summary
Adds governed section-spec schemas and validation coverage for plan template contracts and rendered surface templates.

## Identity
- `initiative_id`: `initiative.plan_template_section_spec_enforcement_foundation`
- `trace_id`: `trace.plan_template_section_spec_enforcement_foundation`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_template_section_spec_enforcement_foundation.publish_section_spec_schema_contracts`: Add governed section-spec schemas for the current high-impact plan templates and rendered surfaces.
- `task.plan_template_section_spec_enforcement_foundation.bind_templates_to_section_spec_contracts`: Update template catalog entries and related family bindings to reference the new section-spec schemas.
- `task.plan_template_section_spec_enforcement_foundation.add_template_validation_coverage`: Extend template helpers and tests so section-spec references and template headings fail closed on drift.
