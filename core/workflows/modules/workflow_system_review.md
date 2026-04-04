# Workflow System Review Workflow

## Purpose
Use this workflow to audit the workflow system across shared and pack-owned roots so workflow modules, roles, routing tables, indexes, validators, and runtime query surfaces stay deterministic and aligned.

## Use When
- The main task is reviewing workflow coverage, workflow quality, routing behavior, role-model clarity, or workflow-system standards drift.
- A change touched workflow docs, routing tables, workflow metadata, route or workflow indexes, validator coverage, or route-preview or query behavior.
- The review needs explicit findings on shared-versus-pack ownership, context-loading discipline, or workflow-system companion drift.

## Inputs
- Scoped workflow-system review request
- In-scope workflow roots, routing tables, and companion machine-readable surfaces
- Current standards, command docs, and authoritative guidance for routing, workflow indexes, and validation
- Known workflow gaps, drift symptoms, or implementation changes under review

## Additional Files to Load
- [workflow_index_standard.md](/core/docs/standards/data_contracts/workflow_index_standard.md): defines the machine-readable workflow coverage and role-composition contract this review must verify.
- [route_index_standard.md](/core/docs/standards/data_contracts/route_index_standard.md): defines the routing-surface contract and required route-to-workflow integrity checks.
- [watchtower_core_query_workflows.md](/core/docs/commands/core_python/watchtower_core_query_workflows.md): defines the workflow-query runtime behavior that should stay aligned with the indexed workflow corpus.
- [watchtower_core_route_preview.md](/core/docs/commands/core_python/watchtower_core_route_preview.md): defines the route-preview behavior this review should confirm when routing changes are in scope.
- [watchtower_core_validate_document_semantics.md](/core/docs/commands/core_python/watchtower_core_validate_document_semantics.md): defines workflow-validation coverage expectations for modules and roles.

## Workflow
1. Define the workflow-system boundary.
   - List the workflow roots, route tables, standards, command surfaces, registries, and indexes that are in scope.
   - Separate shared reusable workflow concerns from pack-owned workflow behavior before assessing reuse or drift.
2. Build the current-state workflow map.
   - Inventory the in-scope modules, roles, routing rows, workflow metadata, route-index coverage, workflow-index coverage, validator coverage, and query or preview behavior.
   - Record which surfaces are authoritative, which are derived, and which docs merely describe runtime behavior.
   - Treat the workflow system as one coherent runtime and documentation surface, not as isolated markdown files. Verify route behavior through the repository's route-preview and workflow-query surfaces where available.
3. Review route and role design quality.
   - Check trigger specificity, overlap, route determinism, minimum-context loading, and whether broad role routes stay composition-oriented instead of duplicating module logic.
   - Check whether reusable behavior belongs in shared core and whether pack-owned workflow docs stay owner-specific instead of re-copying shared logic.
4. Review machine-readable and validation parity.
   - Check that workflow metadata, workflow index, route index, validator coverage, and pack target enumeration include the same active workflow corpus.
   - Check that route-preview, query, and validation command docs still describe current runtime behavior precisely.
5. Synthesize findings and remediation.
   - Distinguish observed gaps, overlapping routes, missing roles, stale validators, index drift, command-doc drift, and ownership-boundary problems explicitly.
   - Record each issue with severity, affected workflow or machine surfaces, observed evidence, why it matters, recommended repair, and whether it is same-change repair, follow-up work, or an intentional exception with rationale.
   - If a workflow-system gap reveals a missing standard, reference, or template, create or repair it in the correct owning surface using the repository's existing authoring rules.
   - Update companion validators, indexes, preview docs, and command docs when workflow behavior changes.
6. Close with proof of the revised workflow posture.
   - Confirm the narrowest meaningful route-preview, workflow-query, validation, and index rebuild checks for the touched workflow-system surfaces.
   - Summarize how the resulting workflow system is clearer, deeper, and less ambiguous than the prior state.

## Data Structure
- Workflow-system inventory covering modules, roles, routes, validators, indexes, and runtime query surfaces
- Findings register with ownership, drift type, and same-change versus follow-up disposition
- Validation and route-preview proof for the touched workflow-system surfaces

## Outputs
- A findings-first workflow-system review with explicit gaps, overlaps, and standards drift
- A remediation sequence for workflow docs, routes, validators, indexes, or command surfaces
- Validation and route-behavior proof for the reviewed workflow-system changes

## Done When
- Workflow modules, roles, routes, validators, indexes, and runtime docs have been reviewed as one coherent system.
- Reusable-core versus pack-owned workflow boundaries are explicit and defensible.
- Same-change repairs versus deferred follow-up work are explicit.
- Route determinism, validation coverage, and query or preview parity are confirmed or the remaining gaps are named directly.
