# Documentation-Implementation Reconciliation Workflow

## Purpose
Use this workflow to compare implementation behavior against companion documentation and machine-readable lookup surfaces so drift is found, classified, and resolved explicitly.

## Use When
- A code, command, schema, or governed artifact change may have invalidated README files, command pages, examples, or machine-readable lookup surfaces.
- A review or maintenance pass needs an explicit docs-versus-implementation reconciliation step rather than relying on broad repository review alone.
- A task's main risk is stale or contradictory behavior documentation rather than missing implementation.

## Inputs
- Scoped reconciliation brief
- In-scope implementation surfaces
- In-scope companion documentation and machine-readable lookup surfaces
- Current behavior evidence from code, tests, CLI help, examples, schemas, indexes, or live governed artifacts
- Internal standards and canonical references applied
- Known authoritative source-of-truth rules for the surfaces in scope
- Known drift suspects, open questions, or authority conflicts

## Related Standards and Sources
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): defines the workflow-boundary and composition rules this module must follow.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): defines the required Markdown structure and section order for this module.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): determines how and when this module is selected or merged during routed execution.
- [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md): provides the repository-wide instruction layer this module operates within.

## Workflow
1. Define the reconciliation boundary.
   - List the implementation surfaces in scope and the companion docs or machine-readable artifacts that make claims about them.
   - Decide which surface is authoritative for each claim type when the repository already defines a canonical source of truth.
2. Capture current implementation evidence.
   - Read the relevant code, tests, CLI help output, schemas, indexes, examples, or generated artifacts.
   - Prefer executable or machine-validated evidence over inferred prose when determining current behavior.
3. Compare companion surfaces to implementation.
   - Check invocations, paths, flags, defaults, output modes, side effects, examples, and described behavior.
   - Check that machine-readable lookup surfaces still point to real files, commands, artifact IDs, or implementation paths.
   - Record exact discrepancies, ambiguous claims, and missing companion coverage explicitly.
4. Resolve or route the discrepancies.
   - Update stale docs and machine-readable companion surfaces when implementation is correct and the drift is documentary.
   - Treat the change as an implementation issue when the docs are canonical and the implementation has drifted instead.
   - Add `documentation_generation.md` when the reconciliation reveals a missing document, or keep `documentation_refresh.md` in scope when the docs already exist but are stale.
5. Validate the reconciled result.
   - Re-run the narrowest meaningful checks, such as CLI help, tests, link or path checks, example invocations, and schema or index validation.
   - Ensure every discrepancy is either resolved in the same change set or recorded as explicit follow-up work.

## Data Structure
- Reconciliation scope
- Authoritative implementation evidence
- Companion documentation surfaces
- Companion machine-readable lookup surfaces
- Discrepancy log with these fields:
  - claim area
  - authoritative source
  - implementation evidence
  - companion source
  - discrepancy type such as `documentation_drift`, `implementation_drift`, `authority_conflict`, or `missing_companion_surface`
  - resolution status such as `resolved_same_change`, `deferred_follow_up`, or `blocked`

## Outputs
- A discrepancy report or updated companion surfaces for the scoped implementation area
- Updated documentation and machine-readable lookup surfaces when the drift is documentary
- Explicit follow-up work for unresolved authority conflicts or deferred fixes

## Done When
- The in-scope companion claims have been checked against the current implementation evidence.
- Silent contradictions between implementation and companion docs or lookup surfaces have been removed or explicitly recorded.
- The task result makes it clear whether the implementation changed, the docs changed, or follow-up work is still required.
