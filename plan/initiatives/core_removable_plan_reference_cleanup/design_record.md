# Core Removable Plan Reference Cleanup Design Record

## Summary
Removes non-essential plan-specific wording and examples from shared core docs, host help, and reusable-core boundaries while preserving only references required by the current repository contract.

## Classification Rule
Use three buckets for every `plan` reference found under `core/**`:

1. Remove
- Shared rule, example, or explanatory text that treats plan as the reusable default.
- Shared host or reusable-core messages that send operators to `watchtower_plan` specifically when the owning-pack abstraction is enough.

2. Rewrite To Generic
- Shared examples that can become `watchtower-core <pack-namespace> ...`, `watchtower-core pack describe --pack <pack-slug>`, or `watchtower_<pack>`.
- Shared standards and READMEs that can describe the current plan pack as one hosted pack example without hard-binding the rule to that name.

3. Preserve
- Current-repo governed machine authority where plan is a true current fact.
- Current generated indexes and registries that reflect the live repository state.
- Tests whose purpose is to prove the current internal plan-pack contract rather than a generic shared-core rule.

## Implementation Shape
- Refresh authored core docs and README surfaces first because they drive generated indexes.
- Update host CLI family examples and shared parser examples next.
- Update reusable-core boundary guard messages and related READMEs afterward.
- Adjust only the tests that assert the changed wording.
- Regenerate the affected indexes and trackers as the final reconciliation step.

## Validation Boundary
- Use targeted lint/tests while iterating on the shared docs/help surfaces.
- Finish with `watchtower-core validate all --skip-acceptance --format json`.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/core_removable_plan_reference_cleanup/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
