# WatchTower CTF Implementation Package Preservation Decision Notes

## Summary

The imported package no longer carries open phase-gated implementation decisions. All `86` rows in the preserved decision register are `locked_in_package`, and this initiative preserves that outcome as the canonical basis for follow-on WatchTower implementation. The full raw register remains mirrored at `source_snapshot/CTF_implementation/indexes/open_decisions.json.raw`.

## Preservation Decisions Locked By This Initiative

- Preserve the full donor package rather than summarizing it externally.
- Use a transformed mirror so donor JSON companions remain byte-identical but validator-safe inside the initiative.
- Keep the mirror immutable after capture; changes to imported meaning happen in canonical initiative docs or in a future explicit recapture.
- Keep support manifests beside the canonical docs rather than forcing them into initiative-state `authored_inputs`, because the initiative schema only accepts the four canonical doc kinds.
- Treat the initiative as the new durable planning authority for this package, while still keeping current repo machine-readable surfaces above imported workbook history when conflicts exist.

## Locked Current-Compatible Baseline

- `pack_root = offensive_security`
- `workspace_root = offensive_security/`
- `pack_slug = offensivesecurity`
- `pack_id = pack.offensivesecurity`
- `command_namespace = offsec`
- `domain_roots = ctf, knowledge`
- canonical challenge path remains `offensive_security/ctf/<platform>/<event>/<challenge>/` with stable placeholder segments in v1
- shared-core surfaces `governance_surface_map`, `path_pattern_registry`, `status_registry`, and `actor_registry` are adopted rather than treated as future work
- challenge and session lifecycle artifacts adapt to the shared status vocabulary, carrying solve and unresolved semantics in closeout outcome rather than pack-only status values
- the first implementation target remains the empty `/home/j/WatchTower` repo, reached through export, copy, scaffold, bootstrap, and validate rather than manual donor copying

## Locked Decision Set By Implementation Area

### Identity, Lifecycle, And Recipient Bootstrap

- `decision.slug_id_generation` and `decision.challenge_path_fallback_policy` lock slug rules, typed ids, collision handling, placeholders, and governed rename behavior.
- `decision.challenge_lifecycle_statuses`, `decision.session_lifecycle_statuses`, `decision.lifecycle_transition_policy`, and `decision.status_transition_rules_contract` lock the current-compatible lifecycle model and explicit transition-policy artifacts.
- `decision.runtime_rollout_sequence` locks the first real implementation proof path and keeps it phase ordered.
- `decision.pentest_pack_split` locks v1 to one hosted pack rooted at `offensive_security/`.

### Workflow, Routing, Query, Sync, And Visibility

- `decision.routing_contract` locks `ROUTING_TABLE.md` and `workflow_metadata_registry.json` as co-equal routing authorities with fail-closed validation on drift.
- `decision.route_preview_output_contract`, `decision.workflow_metadata_contract`, and `decision.route_index_contract` lock the shared-core route-preview, workflow-metadata, and route-index posture.
- `decision.query_output_contracts`, `decision.query_human_output_contract`, `decision.curated_relation_expansion_contract`, and `decision.graph_human_output_contract` lock curated query output, graph output, and expansion behavior.
- `decision.challenge_index_row_contract`, `decision.blocker_index_row_contract`, `decision.session_index_row_contract`, and `decision.knowledge_index_row_contract` lock rich derived query rows rather than minimal lookup rows.
- `decision.shared_query_helper_contract` and `decision.route_workflow_query_alias_policy` keep offsec query surfaces layered on shared helpers and reject offsec-local aliases for shared route and workflow lookup.
- `decision.sync_target_outputs`, `decision.sync_surface_granularity`, and `decision.rendered_visibility_surfaces` lock sync-target split and starter rendered visibility surfaces.
- `decision.public_rebuild_cli` locks public operator guidance to `sync` in v1.

### Control Plane, Validation, Templates, And Authority Routing

- `decision.pack_control_registries` locks the starter registry inventory and the later-phase provenance, review, relation, and promotion registries that must land as implementation progresses.
- `decision.controlled_registry_shape`, `decision.template_catalog_contract`, `decision.documentation_family_registry_contract`, `decision.human_surface_policy_registry_contract`, and `decision.rendered_surface_registry_contract` lock registry root posture and entry contracts.
- `decision.authority_question_set` locks the v1 authority questions for pack state, challenge state, blockers, knowledge, session or environment context, routing, command lookup, and safety posture.
- `decision.validation_suite_layout` locks the baseline validation suite to `pack_contract`, `front_matter`, `document_semantics`, `artifact`, `graph_index`, `authority_map`, `query_contracts`, and `lifecycle_policy`.
- `decision.review_status_registry` and `decision.glossary_term_registry_contract` lock review vocabulary and pack vocabulary governance.

### Artifacts, State, Evidence, Closeout, And Discrepancies

- `decision.event_stream_contract` and `decision.event_type_registry_contract` lock the event envelope and starter event taxonomy.
- `decision.artifact_index_contract`, `decision.challenge_metadata_contract`, `decision.notes_metadata_contract`, `decision.session_state_contract`, and `decision.environment_context_contract` lock governed state and derived index contracts.
- `decision.artifact_payload_primitives`, `decision.closeout_record_contract`, `decision.evidence_storage_layout`, `decision.evidence_artifact_contract`, and `decision.extraction_output_contract` lock artifact-level payload expectations.
- `decision.closeout_gate` and `decision.retention_cleanup_policy` lock admissible closeout and retention behavior.
- `decision.discrepancy_record_contract`, `decision.discrepancy_policy`, `decision.discrepancy_registry_contract`, and `decision.discrepancy_exception_limits_contract` lock the discrepancy model, severities, resolutions, governance limits, and enforcement posture.
- `decision.command_capture_redaction` locks evidence capture summaries, raw-output handling, and redaction posture.
- `decision.markdown_reconciliation_policy`, `decision.template_contracts`, and `decision.notes_template_profile_model` lock direct-edit markdown behavior and required sections for `challenge.md`, `notes.md`, and `recap.md`.

### Knowledge, Promotion, Retrieval, And Provenance

- `decision.knowledge_relation_model` locks a typed relation registry with authoritative `relations[]` on source artifacts and derived-only `related_artifact_ids` in indexes.
- `decision.promotion_policy_registry`, `decision.promotion_state_machine`, and `decision.candidate_knowledge_representation` lock promotion behavior, lifecycle states, and candidate-at-final-path behavior.
- `decision.retrieval_ranking_contract`, `decision.knowledge_human_output_contract`, and `decision.query_human_output_contract` lock deterministic ranking and human-output expectations.
- `decision.shared_knowledge_envelope`, `decision.command_payload_contract`, `decision.tool_profile_payload_contract`, `decision.protocol_payload_contract`, `decision.reference_payload_contract`, `decision.tactic_payload_contract`, and `decision.playbook_payload_contract` lock family-level knowledge contracts.
- `decision.source_trust_model`, `decision.source_clarification_policy`, and `decision.external_references_schema` lock provenance vocabulary, clarification behavior, and external-reference structure.
- `decision.extraction_trigger_policy` locks extraction to explicit requests plus automatic closeout, with no periodic active-phase extraction by default.

### Environment, Modes, Transfers, And Safety

- `decision.environment_adapter_protocol` locks the shared adapter method set for local, VPN-reachable, SSH, and airgapped contexts.
- `decision.safety_confirmation_matrix` and `decision.safety_confirmation_matrix_contract` lock confirmation triggers, action classifications, and refusal posture.
- `decision.mode_state_projection` and `decision.full_auto_observability_contract` lock requested versus effective mode behavior and the visibility posture for `full_auto`.
- `decision.airgapped_transfer_contract` locks the transfer ledger and lower-trust quarantine rules for manually transferred material.
- `decision.actor_ref_requirement` locks mandatory actor refs for confirmations, approvals, remote execution, transfers, closeout, promotion, and destructive or retention actions.
- `decision.actor_bootstrap_day_one` locks reuse of the shared `actor_registry` while deferring explicit actor bootstrap unless the implementation needs it immediately.

## Decision Register Summary

The mirrored decision register remains authoritative preserved input and is normalized here by area. The largest locked clusters are:

| Area | Locked Decisions |
|---|---|
| `query_runtime` | `9` |
| `knowledge_contracts` | `7` |
| `control_plane_surfaces` | `5` |
| `workflow_routing` | `4` |
| `discrepancy_governance` | `4` |
| `evidence_capture` | `3` |
| `knowledge_promotion` | `3` |
| `actor_validation` | `2` |
| `closeout` | `2` |
| `event_stream` | `2` |
| `identity_and_paths` | `2` |
| `knowledge_retrieval` | `2` |
| `lifecycle_model` | `2` |
| `lifecycle_policy` | `2` |
| `provenance` | `2` |
| `rendered_surfaces` | `2` |
| `safety_policy` | `2` |
| `sync_runtime` | `2` |

All remaining areas have one locked decision each. `69` decisions are fully pack-owned, with the remaining subset explicitly recording dependencies on shared runtime hooks, shared registries, shared route-preview and sync primitives, target-repo integration, or deliberate post-v1 product-scope review.

## Locked Post-V1 Deferrals

The preserved intentional deferral set remains:

- `decision.workflow_catalog`: defer a richer workflow catalog beyond routing-table plus workflow-metadata baseline.
- `decision.actor_bootstrap_day_one`: reuse shared `actor_registry` and defer actor bootstrap unless needed immediately.
- `decision.public_rebuild_cli`: keep public operator guidance centered on `sync`.
- `decision.pentest_pack_split`: keep one `offensive_security` hosted pack for v1.
- `decision.saved_query_views`: defer saved query views beyond v1, with pack-owned defaults first and user-local views outside the governed pack root later.
- `decision.provenance_review_impact_surface`: defer richer provenance-triggered downstream review tooling beyond v1.

## Propagation Rule

The imported package already normalized its workshop decisions into contracts, phases, workflows, standards, and indexes. This initiative preserves that rule:

- no standalone workshop log is resurrected as an authority surface;
- the canonical record of each locked default remains the directly affected contract, phase, workflow, standard, or canonical initiative doc; and
- if future implementation overrides any locked default, the change must be recorded as a new live-contract delta plus an update to the preserved decision register and its canonical initiative reflections.
