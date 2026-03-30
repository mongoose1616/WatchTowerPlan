# Workflow Steward Role

## Purpose
Use this role to apply a workflow-governance lens so workflow-system audits and repairs preserve route determinism, minimal-context loading, validator and index parity, and same-change companion updates.

## Use When
- The task centers on workflow modules, workflow roles, routing tables, workflow indexes, route indexes, or workflow validation coverage.
- The change spans shared and pack-owned workflow roots and needs a clear shared-versus-pack ownership decision.
- The review or implementation needs a dedicated orchestration layer that keeps workflow-system changes explicit instead of scattering governance checks across unrelated docs.

## Inputs
- Scoped workflow-system request or review target
- In-scope workflow docs, routing tables, registries, indexes, and command surfaces
- Current standards and canonical docs that govern routing, workflow metadata, and workflow validation

## Composes Modules
- [workflow_system_review.md](../modules/workflow_system_review.md): executes the workflow-system audit and remediation sequence across workflow docs, routes, indexes, validators, and runtime command surfaces.

## Workflow
1. Confirm whether the task is a workflow-system review, a workflow-system implementation change, or both.
2. Apply `workflow_system_review.md` across the in-scope shared and pack-owned workflow surfaces instead of treating routes, roles, validators, or indexes as separate one-off concerns.
3. Prefer the narrowest reusable-core abstraction that removes duplication without pulling pack-owned nouns or lifecycle rules into shared core.
4. Require same-change companion repairs when workflow behavior changes, especially for route and workflow indexes, validator coverage, route-preview behavior, and command docs.
5. Close only after route determinism, workflow discoverability, and validation coverage are explicit enough for the next contributor to continue without oral history.

## Data Structure
- Workflow-system scope and ownership map
- Companion-surface parity checklist for routes, indexes, validators, and command docs
- Explicit same-change repairs and deferred follow-up items

## Outputs
- A workflow-system assessment or implementation result with clear ownership and parity decisions
- Updated workflow, routing, validator, and command surfaces when the task changed workflow behavior

## Done When
- The workflow-system change or review keeps shared reusable behavior separate from pack-owned behavior.
- Role and route surfaces stay explicit, composition-oriented, and aligned with the underlying module set.
- Validator, index, preview, and command-doc parity are explicit rather than assumed.
