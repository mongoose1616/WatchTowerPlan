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

### Routing Table Shape

- The offensive-security routing table stays in the current shared format with `task type`, `trigger keywords`, and `required workflows`.
- The v1 routing model is authored workflow docs plus a pack-owned `workflow_metadata_registry` and shared route preview; do not block the first pack on a richer `workflow_catalog`.
- `ROUTING_TABLE.md` and `workflow_metadata_registry.json` are co-equal authoritative routing surfaces and validation fails immediately if they disagree.

### Initial Task Types And Modules

| Task Type | Workflow Module | Purpose |
|---|---|---|
| `challenge intake` | `challenge_intake` | create or normalize challenge root, collect initial context, and start state |
| `environment assessment` | `environment_context` | confirm local, SSH, VPN, or airgapped assumptions and mode constraints |
| `active execution` | `ctf_execution` | run the active challenge loop, command capture, evidence capture, and note updates |
| `blocker recovery` | `blocker_recovery` | handle blocked-state recovery, pause/resume, and unresolved next steps |
| `knowledge capture` | `knowledge_capture` | extract reusable candidates and strip challenge-specific detail |
| `challenge closeout` | `challenge_closeout` | finalize solution, recap, closeout records, extraction output, and closeout validation |
| `safety review` | `safety_review` | run explicit safety, scope, and confirmation review before higher-risk action or escalation |
| `discrepancy reconciliation` | `discrepancy_reconciliation` | resolve governance drift, discrepancy status, exceptions, and release active limits |

- Do not introduce orphan task types into `ROUTING_TABLE.md`; every initial routed task type must map to an authored workflow module or role in the same slice.
- `safety_review` is a standalone routed module and may also be invoked as an overlay from `ctf_execution`, `challenge_closeout`, and reviewer flows.
- `discrepancy_reconciliation` is a standalone routed module and may also be invoked as an overlay from `blocker_recovery`, `challenge_closeout`, and reviewer flows.

### Workflow Metadata Rules

- Replace the starter scaffold workflow metadata entry immediately.
- Keep every pack-owned workflow id in `workflow.offensivesecurity.*` space.
- Every workflow metadata entry includes `workflow_id`, `phase_type`, `task_family`, `primary_risks`, `extra_trigger_tags`, and `companion_workflow_ids`.
- Starter metadata must be removed before route preview is treated as trustworthy for pack-owned workflows.
- Trigger keywords should bias toward operator intent, challenge state, and risk context rather than static keyword-only matching.
- Use the workflow inventory as the source input for the pack-owned `workflow_metadata_registry`.

### Roles And Shared Modules

| Role | Semantics |
|---|---|
| `ctf_operator` | main execution persona across intake, environment assessment, execution, blocker handling, and closeout |
| `ctf_reviewer` | review lens for extraction quality, closeout completeness, and reusable-knowledge generalization |
| `ctf_safety_reviewer` | escalation and admissibility reviewer for higher-risk execution paths |
| `ctf_discrepancy_reviewer` | discrepancy-resolution and governance-limit reviewer |
| `ctf_knowledge_reviewer` | candidate-quality, provenance, and acceptance reviewer for reusable knowledge |

- Role docs must include explicit `Composes Modules` sections that stay aligned with workflow metadata and route/index surfaces.
- Pack routes may compose shared workflow modules `core.md`, `task_scope_definition.md`, `current_state_inspection.md`, `internal_context_review.md`, `external_guidance_research.md`, and `task_handoff_review.md`.
- Keep CTF domain logic in pack-owned workflow docs rather than moving it into shared modules.

## Exact Query, Sync, Rendered, And Docs Contract

### Curated V1 Query Inventory

| Command | Purpose |
|---|---|
| `status` | pack health, active contract, runtime summary, and safety posture |
| `challenges` | challenge discovery and challenge-state lookup |
| `knowledge` | promoted and candidate reusable-knowledge lookup |
| `sessions` | active and recent session-state lookup |
| `blockers` | blocked or unresolved challenge-state lookup |
| `artifacts` | evidence and broad artifact lookup |
| `events` | challenge-local and pack-derived event history lookup |
| `environment` | environment-context lookup |
| `discrepancies` | raw governance or drift lookup |
| `closeout` | closeout records plus extraction outputs |
| `commands` | filtered command-oriented view over `knowledge` |
| `references` | filtered reference-oriented view over `knowledge` |

### Generic Family Query And Graph Surface

- Curated commands remain the primary operator-facing surface for the highest-value families.
- Generic family query may expose both stable derived indexes and stable raw governed record families.
- Generic family query must not degrade into an unbounded file browser over arbitrary `.wt` or `.wt_local` paths.
- Command and workflow discovery remain on shared-core route and command lookup surfaces rather than gaining offsec-local aliases.
- Public graph query traverses typed relations across challenge, knowledge, evidence, event, discrepancy, transfer, closeout, command, protocol, and related governed families.
- Graph roots may be any typed artifact id from those relational families.
- Traversal defaults to both incoming and outgoing direction.
- Graph traversal must support `--from`, `--depth`, `--direction`, `--relation`, `--family`, `--limit`, `--format`, `--status`, `--review-status`, `--trust-state`, and `--verification-status`.
- Graph output must support `human`, `json`, and `both`.

### Query Service And Human Output Contract

- Follow the `plan` and `oversight` pattern of one query service per curated command with typed search-parameter dataclasses.
- Use a two-tier retrieval model: derived indexes by default, then stable raw governed records only when a family is intentionally queryable without its own derived index.
- Keep JSON field names stable across commands so rendered and machine consumers do not diverge.
- Register query families in one pack-local registry and generate command docs from that registry so CLI, docs, and exposure policy do not drift.
- Curated query commands support `--format human|json|both`, with JSON as the default posture.
- Human output defaults to table-first rendering plus one-line row summaries only when the summary materially improves scanability.
- Default human columns are command-specific and capped at six visible columns before verbose expansion.
- Shared human presets are `compact`, `standard`, and `verbose`, and those preset names keep one pack-wide meaning across curated queries.
- Default human row limits are command-specific, with a recommended cap of twenty rows.
- When row limits truncate results, human output shows omitted-count feedback and the exact flag needed to expand.
- Zero-result human output shows the applied filters plus one or two likely next queries or flags rather than a bare "No results" message.
- Compact trust or provenance cues may appear by default only when they materially affect interpretation.
- Unsupported sort fields fail clearly and list the supported fields for that command rather than silently degrading.
- Use one shared baseline across offsec query rows where fields are meaningful: `id`, `status`, `summary`, `path`, and `updated_at_utc`.

### Status, Relation Expansion, And Knowledge Output

- `status` is the main operator-context command rather than only a light pack summary.
- `status`, `challenges`, and `sessions` share a visibly similar human structure so operators build muscle memory across the main orientation surfaces.
- `status` includes recommended next actions only when blockers, review gates, or safety limits materially constrain the next step.
- When `status` answers the authority-map safety-posture question, it must add `effective_mode`, `interaction_mode`, `environment_type`, `safety_posture_summary`, `confirmation_summary`, `refusal_summary`, and `policy_refs`.
- Derive those safety-posture fields from `safety_confirmation_matrix`, current session/environment context, and active governance limits rather than freeform narrative.
- Keep `policy_refs` pointed at the canonical machine policy and any relevant rendered human policy surface.
- Do not advertise `watchtower-core offsec query status` as the preferred safety-posture command until those fields exist in the implemented output contract.
- Curated family queries may expose relation expansion only through one shared `--expand-relations` flag.
- `--expand-relations` means one hop unless `--depth` is also provided.
- Curated human expansion shows relation types, target ids, and one-line target summaries instead of fully switching to graph-style rendering.
- Root rows and expanded relation targets use separate limits.
- Default per-root expansion cap is five related targets.
- When relation expansion truncates, human output shows omitted counts and the exact flag needed to expand further.
- Curated expansion reuses the graph-query `--relation`, `--family`, `--trust-state`, and `--review-status` flags rather than inventing family-specific variants.
- Relation expansion may apply to every returned root row, subject to the per-root cap.
- Graph-query suggestions appear only when relation expansion is truncated, and those suggestions should include a ready-to-run tailored graph command.
- `--focus <id>` is available only on `knowledge`, `artifacts`, `events`, and `discrepancies`.
- `--focus <id>` may target only rows already returned by the base query.
- `--focus <id>` narrows to that root, automatically enables one-hop relation expansion, and expands row detail even without deeper traversal.
- Named graph modes remain graph-query-only and are not accepted on curated family queries.
- Curated family queries share one `--sort` flag with command-supported field lists.
- Umbrella `knowledge` human output always labels which family each result belongs to.
- `knowledge` groups results by family only when multiple families actually appear.
- Grouped `knowledge` human output uses the fixed family order `tactics`, `playbooks`, `tools`, `commands`, `references`, then everything else.
- JSON output preserves pure retrieval ranking even when human output follows the fixed family order.
- Human output shows a short ordering explanation only when multiple families appear and the displayed family order differs materially from pure ranking order.
- Tactic groups are always visually distinguished from tool, command, and reference groups, and tactic groups use a stronger section heading style in addition to the family label.
- Playbooks get their own visible section heading only when they appear alongside tactics or tool-centric families.
- When both tactics and playbooks appear, show `Tactics` first and then a distinct `Playbooks` section ordered by parent tactic with a visible parent-tactic cue.
- When both tools and commands appear, show `Tools` first and then a distinct `Commands` section ordered by tool with a visible tool cue.
- `References` remain a distinct section ordered by supported artifact family and item, with visible support cues.
- Filtered `commands` and `references` stay flat by default instead of inheriting the full grouped-family behavior from umbrella `knowledge`.
- Filtered `commands` may still group by tool only when multiple tools actually appear.
- Filtered `references` may still group by supported family only when multiple supported families actually appear.
- When those filtered subgroupings are active, the subgroup header may satisfy the visible relationship-cue requirement unless later docs require per-row repetition.
- Retrieval-heavy `knowledge`, `commands`, and `references` output reuses one "why this matched" explanation pattern, but only when ranking materially affects interpretation.
- Public graph query is core for agents, but should be documented as advanced for humans while still appearing in pack examples.
- Named graph modes are `operator`, `provenance`, `retrieval`, and `review`, and those modes act only as aliases for shared flag bundles.
- Human graph traversal defaults to depth two, with aggressive output capping.
- Human graph rendering defaults to a short root summary followed by relation-grouped neighbors.
- Repeated nodes are deduplicated globally in human output with references back to the first occurrence.
- Relation groups are ordered by relevance first, with fixed tie-breaks defined later in implementation docs.
- Provenance-style relations remain inline in graph output but carry a visual marker rather than moving into a separate section.
- Default node summaries in human graph output appear for the root and immediate neighbors only.

### Machine Indexes, Registry, Sync Targets, And Rendered Views

- Planned supporting machine indexes are `offensive_security/.wt/indexes/challenge_index.json`, `offensive_security/.wt/indexes/blocker_index.json`, `offensive_security/.wt/indexes/session_index.json`, `offensive_security/.wt/indexes/knowledge_index.json`, `offensive_security/.wt/indexes/artifact_index.json`, and `offensive_security/.wt/indexes/graph_index.json`.
- The query-family registry canonical path is `offensive_security/.wt/registries/query_family_registry.json`.
- The query-family registry registers every curated and generic query family, declares whether the family is curated, generic-only, or both, declares the backing authoritative surface, output-contract reference, and command-doc page, and drives generated query docs plus query-family overview docs.

| Sync Target | Purpose |
|---|---|
| `challenge-index` | rebuild challenge, blocker, session, artifact, and environment-oriented lookup surfaces |
| `knowledge-index` | rebuild reusable-knowledge indexes and companion summaries |
| `graph-index` | rebuild graph traversal structures from authoritative relations and indexed node metadata |
| `rendered-views` | rebuild pack-owned rendered markdown views |
| `all` | run the full deterministic derived-surface refresh |

- Implement sync targets through the canonical `watchtower_offensivesecurity.sync.registry` module exposing `SYNC_TARGET_SPECS`, following both reference packs.
- Keep `challenge-index`, `knowledge-index`, `graph-index`, `rendered-views`, and `all` as the offsec namespace baseline.
- Use generic shared sync surfaces for command, route, workflow, foundation, and reference indexes unless the offsec pack later proves a real need for pack-namespace aliases.
- `challenge-index` rebuilds pack challenge-state and evidence-navigation lookup surfaces.
- `knowledge-index` rebuilds knowledge indexes plus relation and promotion summary inputs.
- `graph-index` rebuilds the traversal-oriented graph index only.
- `rendered-views` rebuilds rendered markdown companions only.
- `all` runs the full deterministic pack-owned derived-surface refresh.
- Public operator guidance remains aligned to the current `sync` family.
- Reusable `rebuild` primitives may be used internally where shared core already exposes them, but a public `rebuild` CLI split remains a locked post-v1 deferral.
- Pack-owned rendered views include `offensive_security/offensivesecurity_overview.md`, `offensive_security/tracking/challenge_tracking.md`, `offensive_security/tracking/blocker_tracking.md`, `offensive_security/tracking/session_tracking.md`, `offensive_security/tracking/knowledge_tracking.md`, plus human-readable companion views for important machine artifacts where direct JSON browsing would be poor operator UX.
- Author `offensive_security/.wt/registries/authority_map.json` against the shared `authority_map` schema.
- Use the exact v1 question set in `04_contracts/authority_map_and_lookup_plan.md`.
- Point recurring offsec questions at canonical machine indexes first and rendered overview/tracking docs second.
- Keep command and workflow-routing discovery on the shared `command_index` and `route_index` surfaces where those already exist upstream.
- Pack-owned durable docs include namespace command docs under `offensive_security/docs/commands/core_python/`, a query-family overview page, a graph-query guide page, workflow docs under `offensive_security/workflows/`, and standards/guides under pack-owned docs only once the pack exists in the target repo.
- The first document-semantics service validates repo-local markdown link integrity, required sections and section order, pack command-doc integrity, workflow doc integrity, challenge and recap structure once their templates exist, and query-family overview plus graph-guide integrity once those docs are authored.

## Exact State, Index, And Discrepancy Contract

### Event Stream And Event Types

- Canonical event stream path: `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/event_stream.ndjson`.
- Locked shared envelope fields are `event_id`, `event_type`, `timestamp_utc`, and `challenge_id`.
- Conditionally present envelope fields are `session_id`, `actor_ref`, `requested_mode`, `effective_mode`, `interaction_mode`, `artifact_id`, `artifact_family`, `workflow_id`, `route_id`, `reason`, and `payload`.
- Reconciliation rule: the field-level authority for event-stream cardinality is the preserved state/index contract and the package’s implementation-gap audit, both of which define `session_id` and `actor_ref` as conditional; the mirrored decision-register wording with required `actor` and `session_id` is preserved as source history but is not the canonical v1 schema.
- In this initiative, `actor` is not a second event-envelope field. Actor-linked event audit behavior is implemented through conditional `actor_ref`, aligned with the shared actor vocabulary and the pack’s actor-ref requirement.
- Keep one stable top-level event envelope and use `payload` for event-type-specific detail.
- Keep event payloads compact and searchable rather than turning the envelope into a catch-all field dump.
- Keep command-related payload detail to summaries, execution metadata, and artifact refs; raw stdout/stderr belongs in evidence artifacts, not inline event payloads.
- Use `event_stream` as the append-only audit surface, not as the sole source of current state.
- Current-state provenance still lives on the affected artifact or index surface when relevant.
- Event-type registry canonical path: `offensive_security/.wt/registries/event_type_registry.json`.
- Locked starter event types are lifecycle `challenge_created`, `status_changed`, `mode_changed`, `closeout_created`, `closeout_completed`; session `session_started`, `session_resumed`, `session_completed`, `session_closed`; command/execution `command_activity`, `command_refused`; workflow/routing `workflow_started`, `workflow_completed`, `workflow_routed`, `workflow_handoff`, `workflow_escalated`; review/promotion/reconciliation `review_requested`, `review_completed`, `knowledge_promoted`, `discrepancy_detected`, `discrepancy_resolved`; transfer/evidence `airgapped_import`, `airgapped_export`, `evidence_captured`; validation/sync/rebuild `validation_started`, `validation_completed`, `sync_started`, `sync_completed`, `rebuild_started`, `rebuild_completed`.
- Command events use one base `command_activity` family, require `payload.stage = planned | executed | imported`, require `payload.execution_context_type = local | ssh | vpn_reachable | airgapped`, and allow compact payload fields such as `command_summary`, `exit_code`, `related_evidence_refs`, `transfer_ref`, and `safety_classification`.
- Each event-type-registry entry includes event name, description, required top-level fields beyond the shared envelope, allowed payload fields, and lifecycle status.

### Artifact, Graph, And Environment Context

- Artifact index canonical path: `offensive_security/.wt/indexes/artifact_index.json`.
- Required artifact-index core fields are `artifact_id`, `artifact_family`, `path`, `pack`, `status`, `authoritative`, `hidden`, `derived`, `created_at_utc`, and `updated_at_utc`.
- Conditionally required artifact-index fields are `subdomain`, `challenge_id`, `session_id`, flattened `source_*` fields when source metadata exists, `title`, `summary`, `review_status`, `trust_state`, `verification_status`, discrepancy cues, and family-specific visibility fields such as `workflow_surface`.
- Standard optional artifact-index relationship/navigation fields are `parent_artifact_id`, `related_artifact_ids`, `route`, and `rendered_view_path`.
- Keep `artifact_index` broad enough for machine lookup rather than reducing it to a minimal metadata list.
- Keep family-specific extension fields optional rather than globally required.
- Keep `related_artifact_ids` derived-only in the index rather than the primary relation authority.
- Keep the machine `artifact_index` richer than its human-rendered summary view.
- Graph index canonical path: `offensive_security/.wt/indexes/graph_index.json`.
- Keep authoritative typed `relations[]` on source artifacts and derive a separate traversal-oriented `graph_index` for public graph queries and relation-heavy retrieval.
- Refresh `graph_index` through a dedicated sync target and through `all`.
- Required graph-index root fields are `generated_at_utc`, `nodes`, `edges`, and `adjacency`.
- Locked node model fields are `node_id`, `family`, `artifact_kind`, `title_or_summary`, `canonical_path`, `status`, `updated_at_utc`, `review_status`, `trust_state`, `verification_status`, and `rendered_view_path`, with conditionally useful fields `challenge_id`, `parent_refs`, and `family_context`.
- Locked edge model baseline fields are `source_id`, `target_id`, and `relation_type`; standard denormalized edge fields are `source_family`, `source_status`, `target_family`, `target_status`, `evidence_refs`, `provenance_refs`, `created_at_utc`, `review_status`, `trust_state`, `verification_status`, `challenge_id`, `environment_type`, and `edge_summary`.
- Environment context canonical path: `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/environment_context.json`.
- Use one governed root record plus nested `environment_context`, always require `environment_context.summary` and `environment_context.type`, and recommend nested fields `os_family`, `shell`, `runtime`, `execution_location`, `transport`, `remote_host`, `constraints`, `capabilities`, `user_controls_execution`, `agent_can_execute`, and `requires_human_transfer`.
- Locked starter `environment_context.type` values are `local`, `ssh`, `vpn_reachable`, and `airgapped`.
- Locked normalized `constraints` starter values are `no_bash`, `read_only_filesystem`, `no_direct_execution`, `airgapped_transfer_required`, `vpn_required`, `no_root`, `no_outbound_internet`, and `limited_tooling`.
- Locked normalized `capabilities` starter values are `bash_available`, `python_available`, `ssh_available`, `vpn_reachable`, `artifact_capture_available`, `checksum_available`, `can_execute_locally`, `can_execute_remotely`, `can_transfer_files`, and `can_copy_paste_batches`.
- Locked flattened index fields are `environment_type`, `environment_summary`, `environment_os_family`, `environment_shell`, `environment_runtime`, `environment_execution_location`, `environment_transport`, `environment_remote_host`, `environment_user_controls_execution`, `environment_agent_can_execute`, and `environment_requires_human_transfer`.

### Lifecycle, Metadata, Session, And Discrepancy Records

- Locked challenge `status` subset is `active`, `blocked`, `in_review`, `needs_review`, `completed`, and `closed`; use `completed` for successful solve completion at the artifact `status` layer, carry `solved`, `blocked_closeout`, and `unresolved` semantics in `closeout_record.outcome`, and use `closed` for terminal challenge closure regardless of closeout outcome.
- Locked session `status` subset is `active`, `blocked`, `in_review`, `needs_review`, `completed`, `closed`, and `cancelled`; use `blocked` for paused/waiting session states that cannot safely continue, model handoff readiness through explicit fields such as `handoff_ready` and `handoff_notes`, allow only one `active` session per challenge, use `completed` when a session reaches its intended execution or handoff goal, and use `closed` when the session is terminal.
- Challenge metadata canonical path: `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/challenge_metadata.json`.
- Required challenge-metadata fields are `challenge_id`, `challenge_slug`, `canonical_path`, `challenge_path`, `notes_path`, `source`, `status`, `created_at_utc`, and `updated_at_utc`.
- Conditionally required challenge-metadata fields are `platform_slug`, `event_slug`, `display_title`, `review_required`, `review_status`, `current_session_id`, `active_blocker_count`, `unresolved_discrepancy_count`, `last_activity_at_utc`, `rendered_view_path`, and `latest_closeout_ref`.
- Keep identity and provenance compact, structured, and machine-governed; keep authored challenge body content authoritative in `challenge.md`; use the nested `source` shape from `04_contracts/artifact_payload_contracts_plan.md`; and use the locked challenge `status` subset above.
- Notes metadata canonical path: `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/notes_metadata.json`.
- Required notes-metadata fields are `challenge_id`, `notes_path`, `reconciliation_state`, `updated_at_utc`, `unresolved_blocker_count`, and `unresolved_discrepancy_count`.
- Conditionally required notes-metadata fields are `content_checksum`, `last_user_edit_at_utc`, `last_agent_edit_at_utc`, `last_reconciled_at_utc`, `current_session_id`, `last_editor_actor_ref`, and `visible_summary_present`.
- `notes.md` remains authoritative for working narrative and sequential capture; `ctf_notes_metadata` exists only to support reconciliation, summaries, and aggregate views; metadata must stay append-safe and must not become a second competing notes surface.
- Session-state canonical path: `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/session_state.json`.
- Required session-state fields are `session_id`, `challenge_id`, `status`, `requested_mode`, `effective_mode`, `interaction_mode`, `environment_context_ref`, `started_at_utc`, and `last_activity_at_utc`.
- Conditionally required session-state fields are `current_workflow_id`, `current_route_id`, `current_summary`, `recent_command_refs`, `recent_evidence_refs`, `blocker_ref`, `pause_reason`, `handoff_ready`, `handoff_notes`, `resumed_from_session_id`, `closed_at_utc`, `close_reason`, `review_notes`, `operator_actor_ref`, and `reviewer_actor_ref`.
- Use the locked current-compatible session `status` subset above, capture handoff and pause semantics through explicit fields instead of unsupported session-only lifecycle values, allow only one active session per challenge, and treat notes plus event history as fallback reconstruction surfaces when `session_state` is incomplete or flagged for review.
- Discrepancy canonical challenge-local path is `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/discrepancies/<discrepancy_id>.json`.
- Discrepancy canonical pack-level path when promoted is `offensive_security/.wt/discrepancies/<discrepancy_id>.json`.
- Required discrepancy fields are `discrepancy_id`, `artifact_family`, `discrepancy_type`, `severity`, `detected_at`, `detected_by`, `status`, `source_artifact_ref`, and `summary`.
- Conditionally required discrepancy fields are `challenge_id`, `session_id`, `affected_field`, `machine_value`, `observed_value`, `expected_value`, `related_artifact_refs`, `related_event_refs`, `forces_needs_review`, `resolution`, `resolved_at`, `resolved_by`, `resolution_notes`, and `governance_limits`.
- Locked discrepancy `status` values are `open`, `in_review`, `resolved`, and `dismissed`.
- Locked discrepancy workflow is detect discrepancy, create discrepancy record, emit `discrepancy_detected`, force `needs_review` when severity or semantics require it, reconcile or review, resolve/dismiss/exception the discrepancy, then emit `discrepancy_resolved`.
- Mirror active discrepancy state into `artifact_index` for query and filtering, keep discrepancy `status` separate from `resolution`, treat `event_stream` as the audit trail of discrepancy activity rather than the active discrepancy surface, and use governed `status`, `forces_needs_review`, and `governance_limits` instead of ad hoc severity names such as `policy_block`.
- Canonical discrepancy-registry paths are `offensive_security/.wt/registries/discrepancy_type_registry.json`, `offensive_security/.wt/registries/severity_registry.json`, `offensive_security/.wt/registries/discrepancy_resolution_registry.json`, and `offensive_security/.wt/registries/governance_limit_registry.json`.
- Locked starter `discrepancy_type` values are `sync_conflict`, `validation_error`, `unknown_value`, `invalid_transition`, `status_mismatch`, `review_state_mismatch`, `provenance_gap`, `trust_mismatch`, `verification_gap`, `missing_required_field`, `invalid_relation`, `registry_violation`, `route_drift`, `workflow_metadata_drift`, and `preview_contract_drift`.
- Locked starter `severity` values are `informational`, `low`, `medium`, `high`, and `critical`.
- Locked starter `resolution` values are `resolved`, `dismissed`, and `exceptioned`.
- Locked starter `governance_limits` values are `read_only_only`, `no_remote_execution`, `no_closeout`, `review_required`, `no_promotion`, `no_full_auto`, and `no_transfer`.
- Discrepancy types define default severity and whether `forces_needs_review` is implied by default, `exceptioned` is allowed only for types that explicitly permit exceptions, exception-imposed `governance_limits` live on the discrepancy record and may be mirrored onto affected artifacts while active, and validators plus workflow gates must enforce active `governance_limits`.

### Derived Pack Index Row Contracts

- `challenge_index.json` canonical path is `offensive_security/.wt/indexes/challenge_index.json`, with baseline fields `challenge_id`, `status`, `summary`, `canonical_path`, and `last_activity_at_utc`, standard rich fields `platform`, `event`, `challenge_slug`, `challenge_title`, `current_workflow_id`, `current_session_id`, `blocker_count`, `unresolved_discrepancy_count`, `active_governance_limits`, `latest_closeout_ref`, `closeout_outcome`, `evidence_count`, `knowledge_candidate_count`, and `rendered_view_path`, and rules that keep the row rich enough to answer challenge/workflow/blocker/closeout questions without forcing raw challenge-local lookups first.
- `blocker_index.json` canonical path is `offensive_security/.wt/indexes/blocker_index.json`, with baseline fields `blocker_id`, `challenge_id`, `status`, `severity`, and `summary`, standard rich fields `blocker_type`, `discrepancy_id`, `active_governance_limits`, `requires_review`, `resolution_status`, `opened_at_utc`, `last_updated_at_utc`, `canonical_path`, `rendered_view_path`, `source_artifact_ref`, and `owner_role`, and rules that keep blocker lookup independent from raw discrepancy traversal while mirroring active governance limits when they materially affect operator action.
- `session_index.json` canonical path is `offensive_security/.wt/indexes/session_index.json`, with baseline fields `session_id`, `challenge_id`, `status`, `requested_mode`, `effective_mode`, `environment_type`, `started_at_utc`, `last_activity_at_utc`, and `canonical_path`, standard rich fields `interaction_mode`, `current_workflow_id`, `environment_summary`, `handoff_ready`, `operator_actor_ref`, `reviewer_actor_ref`, `active_governance_limits`, `recent_evidence_count`, and `last_command_summary`, and rules that answer session, execution-context, and handoff questions without forcing a raw `session_state` open first.
- `knowledge_index.json` canonical path is `offensive_security/.wt/indexes/knowledge_index.json`, with baseline fields `knowledge_id`, `family`, `title`, `status`, `review_status`, `trust_state`, `verification_status`, `canonical_path`, and `updated_at_utc`, standard rich fields `summary`, `tactic_refs`, `source_count`, `evidence_count`, `relation_count`, `parent_refs`, `freshness_bucket`, and `rendered_view_path`, and rules that keep reusable-knowledge review plus provenance posture visible without duplicating the full artifact payload.

## Exact Research, Standards, Citation, And Safety Rules

### Research And Citation Rules

- ATT&CK remains pinned by version and date when cited, and current package usage pins to ATT&CK v18 with access date unless a later reviewed version is intentionally adopted.
- OWASP references stay pinned to explicit WSTG release material such as v4.2 section URLs or repository tags.
- Avoid `stable` or `latest` OWASP links inside the package.
- Mark draft or informative sources explicitly and never treat them as higher authority than the current repo contract or primary sources.
- The current anchor set remains MITRE ATT&CK Enterprise Tactics and ATT&CK Updates, OWASP WSTG, NIST SP 800-115, NIST SP 800-86, NIST SP 800-92 Rev.1 IPD, and Diataxis.

### Template, Knowledge, And Evidence Standards

- `challenge.md` required sections are `Source`, `Objective`, `Constraints`, and `Environment`.
- `notes.md` required sections are `Working Summary`, `Hypotheses`, `Commands`, `Evidence`, `Blockers`, and `Next Steps`.
- `recap.md` required sections are `Outcome`, `Path`, `Failures`, and `Reusable Lessons`.
- Use one canonical notes template with optional sections and mode-specific rendering overlays rather than multiple unrelated base templates.
- Keep `challenge.md` body source-faithful and locked, allow required front matter to be added at the next workflow opportunity, keep `notes.md` directly editable, require append-preserving agent edits, allow ad hoc user sections during active work, and normalize or flag them only before closeout; hidden machine records remain authoritative for governed fields.
- Reusable-knowledge lifecycle is `candidate`, `accepted`, `deprecated`, and `archived`, with promotion expressed as the governed `candidate -> accepted` transition.
- `review_status` remains a separate governed vocabulary with `not_required`, `pending_review`, `in_review`, `approved`, `rejected`, and `approved_with_exception`, allowing per-family subsets.
- Ship one canonical human-readable glossary standard, one pack-facing glossary surface, and one machine-readable term registry with deprecation and replacement fields.
- Allow explicit extraction at any time, run automatic extraction at closeout, and do not run periodic active-phase extraction by default.
- Always capture proposed or executed command metadata and summaries, keep raw or large stdout/stderr in artifact captures instead of inline notes or event payloads, redact clearly player-owned material from routine machine-visible surfaces while allowing challenge-issued ephemeral values when operationally useful, and use artifact refs for bulky or sensitive outputs.

### Operator Modes, Interaction Modes, And Safety Rules

- User-visible modes are `note_taker`, `assistant`, `teacher`, and `full_auto`.
- `interaction_mode` is a separate overlay vocabulary with `shared_workspace`, `guided_user_execution`, `delegated_agent_execution`, `airgapped_exchange`, `observer_review`, `async_handoff`, and `pairing`.
- `assistant` and `note_taker` remain non-executing by default.
- Local, SSH, and VPN-reachable contexts all keep guidance-only as the baseline until the operator explicitly selects a stronger autonomy level.
- `teacher` is a distinct explanatory operating mode, not merely an overlay on `assistant`, and it must not weaken the same safety or provenance requirements that apply in other modes.
- `note_taker` remains a passive structured recorder and does not infer reusable candidates by default during active work.
- Session state must distinguish `requested_mode` from `effective_mode` when safety rules or environment constraints narrow what the system may actually do.
- Every mode or autonomy change must be explicitly confirmed, written to the event stream, and mirrored into visible session context on meaningful changes.
- Stronger execution requires explicit confirmation and must be auditable.
- Environment adapters remain pack-owned.
- All adapters expose `describe_context`, `check_capability`, `execute_command`, `capture_artifact`, `stage_transfer`, and `record_provenance`, with `airgapped` omitting live execution.
- Local, SSH, VPN-reachable, and airgapped contexts all require explicit mode and provenance handling.
- Airgapped work uses a structured exchange protocol; malformed pasted output must trigger re-paste before machine-state updates.
- Every claims-bearing manual transfer must record transfer id, direction, checksum when practical, operator, source system, destination system, timestamp, purpose, and artifact refs.
- `full_auto` must show planned commands before execution, concise results after execution, grouped checkpoints, and a live journal, and must pause at risk or scope boundaries.
- Full-auto observability detail remains operator-selectable rather than fixed.
- Confirmation is mandatory for credential use, privilege escalation, remote state-changing actions, long-running automation, external transfer, destructive cleanup, and every mode or autonomy change.
- Destructive unattended `full_auto` is refused outright.
- `full_auto` must also refuse scope-ambiguous actions, actions exceeding the active safety class, actions with insufficient environment context, claims-bearing actions with unresolved provenance gaps, and repeated-failure situations where notes or state are too stale.
- Actor refs are mandatory for confirmations, approvals, promotion approvals, closeout approvals/finalization, remote or delegated execution, airgapped transfers, and destructive or retention actions, with only narrow low-risk note-only and derived-refresh exceptions.
- Prohibited or out-of-scope actions must fail closed rather than degrade silently.

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
