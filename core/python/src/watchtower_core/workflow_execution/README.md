# `watchtower_core.workflow_execution`

## Summary
Export-safe workflow execution harness primitives built on governed route selection and workflow metadata.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.workflow_execution` and explicit reusable execution modules such as `engine` and related typed execution helpers.
- `Non-Goals`: Repo-local planning mutations, CLI formatting, command registration, or pack-specific event persistence and step-runner semantics.

## Key Surfaces
- `engine.py`: Turns routed workflow selections into ordered executable workflow steps.
- Execution helpers: Apply callback-based mode checks, gate checks, and typed execution events without owning repo-local workflow mutations.

## Notes
- Keep reusable workflow execution semantics here.
- Keep repo-local planning mutations and package-specific side effects out of this namespace.
