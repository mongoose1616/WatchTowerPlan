# Routing And Metadata Plan

## Routing Table Shape

The offensive-security routing table should stay in the current shared format:

- task type
- trigger keywords
- required workflows

Use authored workflow docs plus metadata registry and route preview. Do not block the first pack on a richer `workflow_catalog`.

`ROUTING_TABLE.md` and `workflow_metadata_registry.json` are co-equal authoritative routing surfaces. Validation fails immediately if they disagree.

## Initial Task Types

- challenge intake
- environment assessment
- active execution
- blocker recovery
- knowledge capture
- challenge closeout
- safety review
- discrepancy reconciliation

## Review And Reconciliation Overlays

- `safety review` is a standalone routed workflow module that may also be invoked as an overlay from `ctf_execution`, `challenge_closeout`, and reviewer flows.
- `discrepancy reconciliation` is a standalone routed workflow module that may also be invoked as an overlay from `blocker_recovery`, `challenge_closeout`, and reviewer flows.
- do not introduce orphan task types into `ROUTING_TABLE.md`; every initial routed task type must map to an authored workflow module or role in the same slice.

## Metadata Registry Expectations

Every workflow metadata entry should include:

- `workflow_id`
- `phase_type`
- `task_family`
- `primary_risks`
- `extra_trigger_tags`
- `companion_workflow_ids`

## Route Preview Expectations

- route preview must remain inspectable through the shared core surface;
- starter metadata must be removed before route preview is treated as trustworthy for pack-owned workflows;
- trigger keywords should bias toward operator intent, challenge state, and risk context rather than static keyword-only matching.

## Review Note

If later implementation genuinely needs `workflow_catalog`, `workflow_surface`, or stronger machine governance over user versus internal workflows, record that as an explicit extension after the baseline routing model is implemented and proven.
