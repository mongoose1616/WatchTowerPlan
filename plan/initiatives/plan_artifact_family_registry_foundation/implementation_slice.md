# Plan Artifact Family Registry Foundation Implementation Slice

## Summary
Adds the missing artifact family registry so plan-pack artifact placement, status subsets, and derived index participation stop living only in path conventions and scattered code.

## Initial Work Breakdown
- `task.plan_artifact_family_registry_foundation.publish_artifact_family_registry_schema`: Add the governed schema contract for the plan-pack artifact family registry.
- `task.plan_artifact_family_registry_foundation.seed_artifact_family_registry_entries`: Seed the initial plan-pack artifact family taxonomy for live initiative, task, evidence, promotion, discrepancy, project, and aggregate surfaces.
- `task.plan_artifact_family_registry_foundation.validate_artifact_family_registry_coverage`: Add validation coverage proving the artifact family registry stays aligned with current live plan artifact schemas and indexes.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
