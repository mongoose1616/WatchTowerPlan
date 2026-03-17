# Plan Status Transition and Relation Rule Registries

## Summary
Adds the missing status transition rules and relation type registries so lifecycle policy and cross-artifact relations stop living only in code and prose.

## Identity
- `initiative_id`: `initiative.plan_status_transition_and_relation_rule_registries`
- `trace_id`: `trace.plan_status_transition_and_relation_rule_registries`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_status_transition_and_relation_rule_registries.publish_rule_registry_schemas`: Add governed schema contracts for the status transition and relation type registries.
- `task.plan_status_transition_and_relation_rule_registries.seed_rule_registry_entries`: Seed the initial plan-pack status transition and relation type registry entries.
- `task.plan_status_transition_and_relation_rule_registries.validate_rule_registry_coverage`: Add validation coverage proving the new rule registries remain aligned with live plan artifact families.
