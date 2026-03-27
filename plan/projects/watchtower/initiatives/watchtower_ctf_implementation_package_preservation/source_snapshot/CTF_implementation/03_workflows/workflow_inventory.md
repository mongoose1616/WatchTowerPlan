# Workflow Inventory

## Modules

| Path | Workflow ID | Phase Type | Task Family | Purpose |
|---|---|---|---|---|
| `offensive_security/workflows/modules/challenge_intake.md` | `workflow.offensivesecurity.challenge_intake` | `scoping` | `offsec_challenge_intake` | create or normalize challenge root, collect initial context, start state |
| `offensive_security/workflows/modules/environment_context.md` | `workflow.offensivesecurity.environment_context` | `inspection` | `offsec_environment_context` | confirm local, SSH, VPN, or airgapped assumptions and mode constraints |
| `offensive_security/workflows/modules/ctf_execution.md` | `workflow.offensivesecurity.ctf_execution` | `execution` | `offsec_ctf_execution` | active challenge loop, command capture, evidence capture, note updates |
| `offensive_security/workflows/modules/blocker_recovery.md` | `workflow.offensivesecurity.blocker_recovery` | `reconciliation` | `offsec_blocker_recovery` | blocked-state handling, recovery strategy, pause/resume, unresolved next steps |
| `offensive_security/workflows/modules/knowledge_capture.md` | `workflow.offensivesecurity.knowledge_capture` | `reconciliation` | `offsec_knowledge_capture` | extract reusable candidates and strip challenge-specific detail |
| `offensive_security/workflows/modules/challenge_closeout.md` | `workflow.offensivesecurity.challenge_closeout` | `closeout` | `offsec_challenge_closeout` | finalize solution, recap, closeout records, extraction output, and closeout validation |
| `offensive_security/workflows/modules/safety_review.md` | `workflow.offensivesecurity.safety_review` | `review` | `offsec_safety_review` | explicit safety, scope, and confirmation review before higher-risk action or escalation |
| `offensive_security/workflows/modules/discrepancy_reconciliation.md` | `workflow.offensivesecurity.discrepancy_reconciliation` | `reconciliation` | `offsec_discrepancy_reconciliation` | resolve governance drift, discrepancy status, exceptions, and release of active limits |

## Roles

| Path | Workflow ID | Phase Type | Task Family | Purpose |
|---|---|---|---|---|
| `offensive_security/workflows/roles/ctf_operator.md` | `workflow.offensivesecurity.ctf_operator` | `execution` | `offsec_ctf_operator` | primary operator persona over live challenge work |
| `offensive_security/workflows/roles/ctf_reviewer.md` | `workflow.offensivesecurity.ctf_reviewer` | `review` | `offsec_ctf_review` | review persona for closeout and reusable-knowledge generalization |
| `offensive_security/workflows/roles/ctf_safety_reviewer.md` | `workflow.offensivesecurity.ctf_safety_reviewer` | `review` | `offsec_ctf_safety_review` | safety-specific reviewer persona for execution admissibility and escalation decisions |
| `offensive_security/workflows/roles/ctf_discrepancy_reviewer.md` | `workflow.offensivesecurity.ctf_discrepancy_reviewer` | `review` | `offsec_ctf_discrepancy_review` | reviewer persona for discrepancy, exception, and governance-limit handling |
| `offensive_security/workflows/roles/ctf_knowledge_reviewer.md` | `workflow.offensivesecurity.ctf_knowledge_reviewer` | `review` | `offsec_ctf_knowledge_review` | reviewer persona for candidate quality, provenance, and reusable-knowledge acceptance |

## Metadata Rules

- replace the starter scaffold workflow metadata entry immediately;
- keep every pack-owned workflow ID in `workflow.offensivesecurity.*` space;
- keep `primary_risks`, `extra_trigger_tags`, and `companion_workflow_ids` explicit for every entry;
- initial routed task types must map to the eight authored workflow modules above;
- `safety_review` and `discrepancy_reconciliation` are standalone routed modules and may also be invoked as overlays from `ctf_execution`, `challenge_closeout`, and reviewer flows;
- use the workflow inventory as the source input for the pack-owned `workflow_metadata_registry`.
