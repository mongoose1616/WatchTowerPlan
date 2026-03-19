# Plan Extraction Output Envelope Alignment

## Summary
Adds a typed extraction-output envelope helper and aligns guidance promotion with an explicit extraction stage instead of schema-only coverage.

## Identity
- `initiative_id`: `initiative.plan_extraction_output_envelope_alignment`
- `trace_id`: `trace.plan_extraction_output_envelope_alignment`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_extraction_output_envelope_alignment.add_typed_extraction_output_helper`: Publish reusable typed models and helper methods for the pack-facing extraction output envelope contract.
- `task.plan_extraction_output_envelope_alignment.wire_guidance_promotion_through_extraction_stage`: Refactor guidance promotion so extraction is an explicit validated stage before durable promotion output is written.
- `task.plan_extraction_output_envelope_alignment.validate_extraction_output_alignment`: Add focused tests and requirements reconciliation proving the extraction envelope now aligns with promotion flows.
