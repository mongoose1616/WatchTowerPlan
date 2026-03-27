# WatchTower CTF Implementation Package Preservation Implementation Slice

## Summary

This initiative’s execution scope is preservation and normalization, not WatchTower runtime implementation. Its output is a ready-for-execution initiative that carries the imported CTF package’s phases, workflows, contracts, research anchors, standards, and locked defaults forward into the governed WatchTower planning workspace.

## Execution Boundary

- This initiative captures planning inputs only.
- `/home/j/WatchTower` remains untouched during this pass.
- The first real implementation work in the target repo is documented here as the next slice after initiative approval.
- No additional live tasks are created during the capture pass beyond the bootstrap task already created by `plan bootstrap`.

## Phase Plan Preserved From The Source Package

| Phase | Focus | Preserved Scope | Exit Intent |
|---|---|---|---|
| `phase.0` | shared contract adoption | confirm current shared-core contract, hosted-pack topology, path rules, status and actor vocabulary, and authority order | implementation starts from live repo truth instead of workbook assumptions |
| `phase.1` | scaffold and integrate the pack | export core, scaffold `offensive_security/`, bootstrap, validate, replace starter workflow metadata, and establish the first real recipient-repo baseline | the recipient repo contains a validated scaffolded pack with starter metadata replaced |
| `phase.2` | author the pack machine contract | define schemas, registries, ledgers, validation suite, authority map, rendered-surface registry, template governance, lifecycle policy, provenance vocabularies, and glossary surfaces | machine contract is explicit enough to drive runtime and validation without re-derivation |
| `phase.3` | build the CTF runtime | author workflow docs, routing and metadata, route preview posture, query and sync runtimes, graph query, query-family registry, and the first thin CLI vertical slice | real CLI behavior proves the first machine-record bundle end to end |
| `phase.4` | build the domain artifacts | implement `challenge.md`, `notes.md`, `recap.md`, challenge metadata, notes metadata, session state, event stream, evidence inventory, closeout, and discrepancy handling | challenge execution and closeout artifacts work with governed state and validation |
| `phase.5` | build knowledge, promotion, and retrieval | implement reusable knowledge families, relation typing, promotion policy, review status, deterministic retrieval, knowledge query output, and extraction behavior | knowledge capture and retrieval work without weakening provenance or review posture |
| `phase.6` | build environment adapters and safety controls | implement local, SSH, VPN, and airgapped adapters, environment context, confirmation gates, refusal rules, actor refs, transfer ledger, and mode-state projection | execution autonomy and transfer behavior are explicit, auditable, and fail closed |
| `phase.7` | release and portability proof | prove export, bootstrap, validate, and release portability for the intended handoff mode | implementation is portable and customer-safe by the repo’s existing export/bootstrap contract |

## Locked Runtime Rollout Sequence

The source package locks the first executable proof path and this initiative preserves it unchanged.

1. Scaffold and bootstrap the pack in the recipient repo with the current-compatible identity.
2. Replace starter workflow metadata and author workflow docs in parallel.
3. Land the first machine-record bundle of challenge metadata, notes metadata, event stream, artifact index, graph index, session state, and environment context.
4. Prove a thin real-CLI vertical slice on the actual pack root through `challenge_intake -> challenge_metadata + notes_metadata + event_stream + artifact_index + offsec query challenges + offsec query artifacts`.
5. Add unit tests and CLI smoke tests immediately after the vertical slice works end to end.
6. Prove `session_state + environment_context + offsec query status`, then `blockers`, then `knowledge`.
7. Ship the first public graph query after curated queries and sync targets stabilize and after knowledge is proven.
8. Run a short packaging and UX consolidation pass.
9. Run the first deliberately small or simple real challenge flow.

## Workflow Model And Roles

The imported workflow plan remains part of the canonical implementation slice.

- Workflow model: routed workflow docs remain the authored surface, with `ROUTING_TABLE.md` and `workflow_metadata_registry.json` treated as co-equal authorities.
- Initial workflow modules: `challenge_intake`, `environment_context`, `ctf_execution`, `blocker_recovery`, `knowledge_capture`, `challenge_closeout`, `safety_review`, and `discrepancy_reconciliation`.
- Required roles: `ctf_operator`, `ctf_reviewer`, `ctf_safety_reviewer`, `ctf_discrepancy_reviewer`, and `ctf_knowledge_reviewer`.
- Route-preview expectations: preserve the live shared-core route-preview contract and do not introduce offsec-local aliases for shared route or workflow discovery.

## Contract Bundles Preserved For Implementation

### Bootstrap, Identity, And Recipient Handoff

- `04_contracts/scaffold_and_bootstrap_baseline.md`
- `04_contracts/core_export_and_target_bootstrap_plan.md`
- `04_contracts/path_and_id_generation_plan.md`

These docs lock the runnable identity, target bootstrap sequence, path and slug rules, placeholder policy, typed ids, and governed rename behavior.

### Control Plane, Validation, And Visibility

- `04_contracts/schemas_registries_ledgers_validation_plan.md`
- `04_contracts/control_plane_registry_contracts_plan.md`
- `04_contracts/rendered_surface_contracts_plan.md`
- `04_contracts/authority_map_and_lookup_plan.md`
- `04_contracts/lifecycle_and_safety_policy_contracts_plan.md`

These docs lock the baseline validation suite, registry inventory, registry root posture, template governance, rendered surfaces, authority questions, lifecycle policy artifacts, and safety-confirmation policy artifacts.

### Runtime, Query, Sync, And Routing

- `04_contracts/routing_and_runtime_contracts_plan.md`
- `04_contracts/query_sync_rendered_views_docs_plan.md`
- `03_workflows/routing_and_metadata_plan.md`
- `03_workflows/workflow_inventory.md`
- `03_workflows/workflow_topology_and_roles.md`

These docs lock routing authority, workflow metadata, route preview, query-family posture, curated query output, graph query, sync target granularity, rendered visibility, and workflow roles.

### Artifacts, State, Evidence, And Discrepancies

- `04_contracts/state_and_index_contracts_plan.md`
- `04_contracts/artifact_payload_contracts_plan.md`
- `04_contracts/retention_and_cleanup_policy_plan.md`

These docs lock event streams, environment context, artifact index, graph index, challenge metadata, notes metadata, session state, closeout record, evidence inventory, extraction output, discrepancy records, governance limits, retention rules, and closeout admissibility.

### Knowledge, Retrieval, And Promotion

- `04_contracts/knowledge_governance_and_retrieval_plan.md`
- `06_standards/knowledge_taxonomy_and_promotion_standard.md`

These docs lock knowledge family envelopes, family-specific payloads, relation typing, promotion policy, deterministic retrieval ranking, clarification policy, external references, and accepted-versus-candidate lifecycle behavior.

### Environment, Modes, And Safety

- `04_contracts/environment_and_safety_execution_plan.md`
- `06_standards/operator_modes_and_safety_standard.md`
- `06_standards/evidence_provenance_and_audit_standard.md`
- `06_standards/documentation_and_templates_standard.md`

These docs lock adapter protocols, interaction modes, requested versus effective mode handling, actor refs, airgapped transfer behavior, command capture and redaction, and editable markdown reconciliation rules.

## Research And Standards Posture

The imported research and standards remain part of the implementation package and are now preserved in this initiative.

- ATT&CK v18 remains the pinned offensive-security taxonomy reference where used.
- OWASP WSTG remains the community-canonical workflow and coverage reference.
- NIST SP 800-115 informs workflow and reporting posture.
- NIST SP 800-86 informs evidence handling and provenance discipline.
- NIST SP 800-92 Rev.1 IPD remains informative guidance for event-stream and audit design.
- Diataxis remains the reference for separating guides, standards, references, and explanation surfaces.

## Dependencies And Risks Carried Forward

Key dependencies:

- shared-core pack commands and validation hooks;
- current shared governance surfaces and registries;
- donor-pack implementation patterns from `plan` and `oversight`;
- external research anchors for standards and guides, always subordinate to current repo truth.

Key risks:

- scaffold-identity drift if upstream slug normalization changes;
- contract staleness if Step 1 assumptions outrun live shared-core truth;
- doc/index drift if markdown and structured companions are not kept aligned;
- workflow placeholder drift if starter metadata is not replaced early;
- safety under-specification if Phase 6 work is postponed or treated as optional.

## Backlog And Next Slice

The imported backlog remains preserved in the initiative and drives the first post-approval implementation order.

Immediate preserved work:

- confirm locked post-v1 deferrals remain intentional;
- use donor-pack precedent to resolve defaults before inventing offsec-specific shapes;
- implement the locked authority-map question set;
- implement the locked retention and freeze rules;
- scaffold and bootstrap the baseline pack in the target repo;
- replace scaffold starter workflow metadata;
- land first real CTF schemas and validators;
- author first workflow docs and document-semantics service.

Near-term preserved work:

- implement query and sync runtimes;
- implement challenge artifacts and ledgers;
- implement closeout and knowledge-capture flow;
- implement environment adapters and safety controls.

Later preserved work:

- revisit whether `workflow_catalog` is needed after the baseline pack works;
- revisit pack-slug normalization and optional-segment path collapse after upstream fixes and migration tooling exist.

## First Post-Approval Execution Slice

After this preservation initiative is approved, the next execution slice should occur in `/home/j/WatchTower` and should:

1. export shared core from `/home/j/WatchTowerPlan/core`;
2. copy the staged export into `/home/j/WatchTower`;
3. scaffold `offensive_security/` there with the current-compatible baseline identity;
4. run `watchtower-core pack bootstrap --replace-hosted-packs --write` if donor pack wiring must be replaced;
5. run `pack validate`, `validate all`, and changed-schema validation; and
6. begin the phase-ordered implementation sequence preserved above.

## Gate

- No `/home/j/WatchTower` execution starts until this initiative is approved and marked `ready_for_execution`.
