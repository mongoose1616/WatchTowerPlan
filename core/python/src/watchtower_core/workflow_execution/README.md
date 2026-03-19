# `watchtower_core.workflow_execution`

## Summary
Export-safe workflow execution harness primitives built on governed route selection and workflow metadata.

## Use It For
- turning routed workflow selections into ordered executable workflow steps
- applying callback-based mode checks and gate checks before execution
- running callback-based workflow step handlers while emitting typed execution events

## Keep Out
- repo-local planning mutations
- CLI formatting and command registration
- pack-specific event persistence or step-runner semantics
