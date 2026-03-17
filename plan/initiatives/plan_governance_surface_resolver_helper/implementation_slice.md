# Plan Governance Surface Resolver Helper Implementation Slice

## Summary
Adds the missing governance surface resolver helper so pack and core governed surfaces can be resolved through one typed query surface instead of scattered loader and registry logic.

## Initial Work Breakdown
- `task.plan_governance_surface_resolver_helper.add_governance_surface_resolver_helper`: Implement a reusable-core helper that resolves governed surface path, authority, rebuildability, and declaration source.
- `task.plan_governance_surface_resolver_helper.add_governance_surface_dependency_coverage`: Add unit coverage proving the helper resolves both pack-declared and governance-map surfaces and reports dependent declared surfaces.
- `task.plan_governance_surface_resolver_helper.validate_governance_surface_resolver_behavior`: Run targeted validation proving the helper stays aligned with requirements.md, decisions.md, and the active pack settings declarations.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
