# Plan Status Transition and Relation Rule Registries Design Record

## Summary
Adds the missing status transition rules and relation type registries so lifecycle policy and cross-artifact relations stop living only in code and prose.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_status_transition_and_relation_rule_registries/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
