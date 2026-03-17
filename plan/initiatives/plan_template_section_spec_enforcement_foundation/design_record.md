# Plan Template Section-Spec Enforcement Foundation Design Record

## Summary
Adds governed section-spec schemas and validation coverage for plan template contracts and rendered surface templates.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_template_section_spec_enforcement_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
