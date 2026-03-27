# WatchTower CTF Implementation Package Preservation Implementation Slice

## Summary

This initiative’s execution scope is preservation and normalization, not WatchTower runtime implementation. Its output is a ready-for-execution initiative that carries the imported CTF package’s phases, workflows, contracts, research anchors, standards, and locked defaults forward into the governed WatchTower planning workspace.

## Execution Boundary

- This initiative remains the same-initiative engineer handoff package for downstream WatchTower implementation.
- `/home/j/WatchTower` remains untouched during this hardening pass.
- The transformed mirror remains immutable provenance; engineers should execute from the canonical docs and live task graph first, then reopen mirrored source docs only when deeper narrative context is needed.
- The first real implementation work in the target repo is now represented by the phase-aligned live task chain documented here and in initiative-local task state.

## Engineer Handoff Entry Order

The preserved package’s required read-first order is now canonicalized for follow-on engineers.

1. Read `README.md` first to map the larger initiative root and find the canonical versus support surfaces quickly.
2. Read `initiative_brief.md`, `design_record.md`, and `decision_notes.md` to lock the current-compatible baseline, preserved deltas, reconciled tensions, and known deferrals.
3. Read `implementation_slice.md` front to back before touching `/home/j/WatchTower`; it now restates the phase dependencies, gates, exit criteria, starter human-surface rules, and first ready task.
4. Use `phase_output_manifest.md` and `phase_closeout_checklists.md` as the execution companions for the active phase.
5. Use `starter_surface_blueprint.md` and `starter_registry_exemplars.md` during Phase 1 and Phase 2 so starter docs and starter registries are copy-ready instead of inferred.
6. Use `artifact_specimens.md` and `machine_surface_specimen_index.md` during Phase 2 and Phase 3 so the first machine-record bundle and first indexes do not need to be derived from narrative prose alone.
7. Use `vertical_slice_proof_spec.md` during Phase 3 to prove the first runtime seam exactly once and avoid a vague "runtime works" claim.
8. Use `phase_test_matrix.md` before calling any phase complete; it is the compact validator and smoke-test companion to the phase manifest.
9. Use `promotion_extraction_map.md` during Phase 4 and Phase 5 so candidate extraction and accepted knowledge promotion follow one explicit path.
10. Check `engineer_ambiguity_kill_sheet.md`, `conditional_revisit_queue.md`, and `contradiction_sweep_ledger.md` when something feels ambiguous; do not silently reopen a resolved baseline or deferral.
11. Reopen the mirrored source docs in `04_contracts/` before authoring manifests, schemas, validators, query or sync runtimes, lifecycle policy, or bootstrap behavior.
12. Reopen the mirrored `03_workflows/` docs before authoring workflow docs, roles, routing, or workflow metadata.
13. Keep mirrored `indexes/` companions, canonical docs, and later pack-owned machine surfaces aligned in the same change set whenever a governed contract changes.

Required discipline carried forward from the source execution guide:

- implement phases in order unless this slice explicitly marks an item as parallel-safe;
- do not reintroduce retired `domain_packs/**` topology or `/docs/**` authority assumptions;
- keep the current-compatible scaffold identity until upstream slug handling changes through an explicit live-contract delta;
- record any new live-contract delta before changing a phase or contract boundary; and
- prefer shared-core reuse before pack-local duplication when generic helpers already exist.

## Engineer Handoff Support Surfaces

These support docs make the package more executable without creating a second authority layer.

- `README.md` is the initiative-root navigation surface for the larger preserved package.
- `phase_output_manifest.md` is the per-phase execution companion for outputs, command anchors, validation proof, and closeout evidence.
- `phase_closeout_checklists.md` is the short final-pass closeout companion for each preserved phase.
- `starter_surface_blueprint.md` is the copy-ready README / AGENTS and registry posture companion for the first offsec root.
- `starter_registry_exemplars.md` is the copy-ready machine-registry companion for the first offsec control registries.
- `vertical_slice_proof_spec.md` is the exact proof boundary for the first real Phase 3 runtime slice.
- `artifact_specimens.md` is the example-filled companion for the first governed challenge-local records, `artifact_index`, and minimal lookup registries.
- `phase_test_matrix.md` is the compact validator and smoke-test companion for every preserved phase.
- `machine_surface_specimen_index.md` is the first machine-surface inventory across `.wt/` and `.wt_local/`.
- `engineer_ambiguity_kill_sheet.md` is the compact default-answer companion for likely implementation ambiguities.
- `promotion_extraction_map.md` is the Phase 4 and Phase 5 companion for candidate extraction, review, and accepted knowledge publication.
- `conditional_revisit_queue.md` names the later decisions that remain explicitly deferred until execution evidence forces them back open.
- `contradiction_sweep_ledger.md` records the already-reconciled tensions across source wording, canonical docs, and live task state.

The four canonical docs and live task state remain authoritative. Update these support docs in the same change set whenever canonical phase, starter-surface, or deferred-decision meaning changes materially.

## Phase Plan Preserved From The Source Package

| Phase | Focus | Live Task | Exit Intent |
|---|---|---|---|
| `phase.0` | shared contract adoption | `task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment` | implementation starts from live repo truth instead of workbook assumptions |
| `phase.1` | scaffold and integrate the pack | `task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap` | the recipient repo contains a validated scaffolded pack with starter metadata replaced |
| `phase.2` | author the pack machine contract | `task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract` | machine contract is explicit enough to drive runtime and validation without re-derivation |
| `phase.3` | build the CTF runtime | `task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam` | real CLI behavior proves the first machine-record bundle end to end |
| `phase.4` | build the domain artifacts | `task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout` | challenge execution and closeout artifacts work with governed state and validation |
| `phase.5` | build knowledge, promotion, and retrieval | `task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval` | knowledge capture and retrieval work without weakening provenance or review posture |
| `phase.6` | build environment adapters and safety controls | `task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety` | execution autonomy and transfer behavior are explicit, auditable, and fail closed |
| `phase.7` | release and portability proof | `task.watchtower_ctf_implementation_package_preservation.phase_7_release_and_portability_proof` | implementation is portable and customer-safe by the repo’s existing export/bootstrap contract |

## Same-Initiative Execution Task Chain

The live handoff task graph is phase-aligned and intentionally linear at the phase boundary. Parallel-safe work exists inside some phases, but no later phase starts until its predecessor’s exit criteria are met.

1. `phase.0_shared_contract_adoption_and_alignment`
   - status: `ready`
   - depends on: none
   - governs: live baseline, donor/recipient split, source-precedence, and first engineer read-first order
2. `phase.1_recipient_scaffold_and_bootstrap`
   - status: `planned`
   - depends on: `phase.0_shared_contract_adoption_and_alignment`
3. `phase.2_pack_machine_contract`
   - status: `planned`
   - depends on: `phase.1_recipient_scaffold_and_bootstrap`
4. `phase.3_runtime_query_sync_and_workflow_seam`
   - status: `planned`
   - depends on: `phase.2_pack_machine_contract`
5. `phase.4_challenge_artifacts_and_closeout`
   - status: `planned`
   - depends on: `phase.3_runtime_query_sync_and_workflow_seam`
6. `phase.5_knowledge_promotion_and_retrieval`
   - status: `planned`
   - depends on: `phase.4_challenge_artifacts_and_closeout`
7. `phase.6_environment_adapters_and_safety`
   - status: `planned`
   - depends on: `phase.5_knowledge_promotion_and_retrieval`
8. `phase.7_release_and_portability_proof`
   - status: `planned`
   - depends on: `phase.6_environment_adapters_and_safety`

The bootstrap placeholder task created by `plan bootstrap` is no longer the execution entrypoint. It is retired in live task state so the next engineer action resolves to the real phase chain above.

## Phase Dependencies, Validation, And Exit Criteria

### `phase.0` Shared Contract Adoption

- Dependencies:
  - all Step 1 source docs;
  - current `WatchTowerPlan/core` standards, commands, registries, and pack-context code; and
  - reference pack manifests from `plan` and `oversight`.
- Validation and acceptance:
  - all live-contract deltas are explicit;
  - the current-compatible identity baseline is consistent across canonical docs;
  - target repo state remains recorded as of `2026-03-26`; and
  - `README.md`, `phase_output_manifest.md`, `phase_closeout_checklists.md`, `starter_surface_blueprint.md`, `conditional_revisit_queue.md`, and `contradiction_sweep_ledger.md` reflect the same current baseline; and
  - donor shared core and working reference packs are separated clearly.
- Exit criteria:
  - one unambiguous current baseline exists for identity, topology, authority, and destination.
  - phase support docs no longer leave hidden judgment calls before target-repo mutation begins.
- Parallel-safe boundary:
  - none; no downstream authoring begins until the baseline is locked.

### `phase.1` Recipient Scaffold And Bootstrap

- Dependencies:
  - `phase.0` baseline;
  - current `watchtower-core pack scaffold`, `pack bootstrap`, and `pack validate`; and
  - shared `core/python/pyproject.toml` bootstrap behavior.
- Validation and acceptance:
  - scaffold, bootstrap, and direct pack validation commands are captured exactly as rerun on `2026-03-26`;
  - manifest examples match the current-compatible proof;
  - path normalization, typed ids, placeholder segments, and collision handling are locked before the first real challenge root exists;
  - starter workflow metadata replacement is mandatory before route or index reliance;
  - `offensive_security/docs/commands/core_python/README.md` is explicitly authored before authority-map command lookup depends on it;
  - the immediate next slice is explicit, minimal, and proves a thin real-CLI vertical slice with real schemas and validators.
- Exit criteria:
  - the package shows exactly how to move from an empty target repo to a bootstrap-valid starter pack with no hidden steps.
- Parallel-safe boundary:
  - starter workflow metadata replacement and workflow-doc authoring may proceed in parallel only after the scaffolded pack root exists and the phase-0 baseline is locked.

### `phase.2` Pack Machine Contract

- Dependencies:
  - `phase.0` identity and live-contract baselines;
  - `phase.1` scaffolded machine root; and
  - current typed shared schemas for pack settings and shared governance surfaces.
- Validation and acceptance:
  - all required schema families are assigned concrete paths;
  - governed artifact families inherit shared payload primitives;
  - `event_stream`, `artifact_index`, `environment_context`, `challenge_metadata`, `notes_metadata`, `session_state`, and `discrepancy` field contracts are locked;
  - the first machine-record slice lands `challenge_metadata`, `notes_metadata`, `event_stream`, `artifact_index`, `graph_index`, `session_state`, and `environment_context` together;
  - `source.type`, `trust_state`, and `verification_status` vocabularies are locked;
  - template, documentation-family, human-surface-policy, rendered-surface, and lifecycle-policy registry entry shapes are explicit;
  - the first template, documentation-family, human-surface, rendered-surface, and authority-map artifacts align with `starter_registry_exemplars.md`; and
  - the first governed challenge-local records and first derived indexes are representable without guesswork through `artifact_specimens.md` and `machine_surface_specimen_index.md`; and
  - the baseline validation suite covers `pack_contract`, `front_matter`, `document_semantics`, `artifact`, `graph_index`, `authority_map`, `query_contracts`, and `lifecycle_policy`.
- Exit criteria:
  - the package provides a complete schema, registry, and validation plan for the first real challenge flow.
- Parallel-safe boundary:
  - registry authoring may proceed in parallel across families once the scaffold is validated, but the first machine-record slice does not start until the field-level contracts converge.

### `phase.3` Runtime, Query, Sync, And Workflow Seam

- Dependencies:
  - `phase.1` scaffolded python, docs, and workflow roots;
  - `phase.2` schema and validator plan; and
  - working pack patterns from `plan` and `oversight`.
- Validation and acceptance:
  - query runtime and sync runtime inventories are non-empty and concrete;
  - workflow inventory and workflow metadata registry match;
  - initial routing-table task types map only to authored workflow modules or roles in the same slice;
  - query, graph, sync-target, rendered-view, and document-semantics behavior aligns with the preserved contract docs;
  - `status` explicitly carries the safety-posture summary and confirmation-gate fields; and
  - the authority map points to real query outputs, rendered views, and shared command or route surfaces;
  - phase-specific proof remains aligned with `phase_test_matrix.md`; and
  - the first runtime proof satisfies `vertical_slice_proof_spec.md` exactly, including the mandatory surface set, validation proof, and failure exclusions.
- Exit criteria:
  - the package describes a complete runtime seam from host namespace to pack validation, query, sync, and workflow behavior.
- Parallel-safe boundary:
  - author workflow metadata and workflow docs in parallel with the first machine-record slice;
  - graph-query work waits until curated queries and knowledge are both stable.

### `phase.4` Challenge Artifacts And Closeout

- Dependencies:
  - `phase.2` schema definitions; and
  - `phase.3` document semantics, routing, and runtime hooks.
- Validation and acceptance:
  - `challenge.md` preserves source body text while allowing machine front matter;
  - `notes.md` remains the active, append-preserving working surface with one canonical structure;
  - closeout requires `challenge.md`, `notes.md`, `closeout_record`, extraction output, a passing closeout suite, and no active discrepancy carrying `no_closeout`;
  - `solution/` and `recap.md` obey the locked outcome-based requirements;
  - evidence capture keeps raw files under `artifacts/` and governed records under `.wt_local/evidence/artifacts.json`;
  - command capture, closeout, extraction, challenge metadata, notes metadata, session state, event stream, artifact index, environment context, and discrepancy records all follow their exact preserved contracts; and
  - closeout freezes `.wt_local/` in place instead of relocating or deleting the challenge root.
- Exit criteria:
  - the package defines the full artifact and ledger model for one challenge lifecycle.
- Parallel-safe boundary:
  - challenge, notes, evidence, and closeout surfaces may iterate together after runtime hooks exist, but closeout finalization waits on discrepancy and validation gates.

### `phase.5` Knowledge Promotion And Retrieval

- Dependencies:
  - `phase.2` knowledge-family schema planning;
  - `phase.4` extraction output and closeout behavior; and
  - research anchors for ATT&CK, WSTG, and evidence/reporting patterns.
- Validation and acceptance:
  - every knowledge family has explicit ownership, schema, and template direction;
  - the shared reusable-knowledge envelope and family payload contracts are explicit enough to author schemas without re-derivation;
  - playbooks remain nested beneath tactics;
  - extraction is requestable, runs automatically at closeout, and does not become periodic active-phase promotion by default;
  - promotion and `review_status` remain distinct governed concepts;
  - typed relations are authoritative on source artifacts and `related_artifact_ids` remain derived-only;
  - promotion policy, glossary governance, external references, and deterministic retrieval ranking stay explicit; and
  - challenge-specific detail is stripped or quarantined before promotion; and
  - `promotion_extraction_map.md` stays aligned with the implemented candidate-to-accepted flow.
- Exit criteria:
  - the package provides a full reusable-knowledge and promotion plan from candidate extraction to canonical retrieval.
- Parallel-safe boundary:
  - family-specific knowledge payload authoring may proceed in parallel once the shared envelope and promotion policy are fixed, but promotion and retrieval runtime work waits on the phase-4 extraction contract.

### `phase.6` Environment Adapters And Safety

- Dependencies:
  - `phase.2` environment, session, and discrepancy schemas;
  - `phase.3` runtime hooks and workflow docs; and
  - `phase.4` artifact and event-stream model.
- Validation and acceptance:
  - local, SSH, VPN, and airgapped modes are all addressed explicitly;
  - `note_taker`, `assistant`, `teacher`, and `full_auto` are distinguished clearly;
  - guidance-only stays the baseline until stronger autonomy is explicitly enabled;
  - session state records requested versus effective mode and meaningful mode changes;
  - full-auto observability, confirmation gates, refusal rules, airgapped transfer handling, actor-ref requirements, and provenance expectations remain explicit and auditable; and
  - lifecycle and safety policy artifacts align with the preserved lifecycle and safety contract.
- Exit criteria:
  - the package contains a concrete environment and safety model that can be implemented without reinterpreting policy intent.
- Parallel-safe boundary:
  - adapter-specific implementation may proceed in parallel only after the shared adapter protocol and safety-confirmation matrix are fixed; no environment mode ships without the same safety gates.

### `phase.7` Release And Portability Proof

- Dependencies:
  - `phase.0` through `phase.6` complete; and
  - target repository ready to receive exported core and pack roots.
- Validation and acceptance:
  - donor and recipient roles are explicit;
  - all handoff modes are documented: `core-only`, `core-plus-pack`, and `pack-only`;
  - portability proof uses staged export rather than raw repo snapshots; and
  - the target bootstrap sequence is explicit and reproducible.
- Exit criteria:
  - the package defines the full bootstrap, validation, and portability proof path into `/home/j/WatchTower`.
- Parallel-safe boundary:
  - changed-schema validation and portability verification may fan out once the full pack exists, but final staged export proof waits until all earlier phases are complete.

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

### Human Surface, Template, And Best-Practice Carryover

- The pack machine-contract baseline must require pack-local `template_catalog`, `documentation_family_registry`, and `human_surface_policy_registry` surfaces before the offsec pack is considered documentation-complete.
- Use `starter_surface_blueprint.md` as the engineer-facing starter contract for the first `README.md` and `AGENTS.md` surfaces. If the carried-over posture changes later, update the blueprint and the governing registries in the same change set.
- Required starter `README.md` roots are `offensive_security/`, `offensive_security/docs/`, `offensive_security/workflows/`, `offensive_security/docs/commands/core_python/`, `offensive_security/tracking/`, and `offensive_security/python/`.
- Required starter `AGENTS.md` roots are `offensive_security/`, `offensive_security/workflows/`, and `offensive_security/python/`.
- `offensive_security/docs/AGENTS.md` remains optional unless the docs subtree later needs local behavior that materially differs from the pack root rules.
- Carry the `plan` / `oversight` root-template posture forward:
  - `README.md` stays thin, navigational, and points readers to machine authority or rendered visibility surfaces where applicable.
  - `AGENTS.md` stays narrow, local, and does not restate repository-wide rules.
- Govern recurring human-facing roots through the registries above instead of prose-only convention.
- Keep docs plus indexes, registries, and rendered views aligned in the same change set whenever one depends on the other.
- Name rendered visibility surfaces explicitly and keep them registry-backed rather than ad hoc.
- Use evidence-first readiness and contradiction-sweep discipline for engineer handoff claims.
- Reuse shared core before pack-local duplication whenever a helper is generic.
- Keep domain workflows, templates, terminology, and guidance pack-owned once they become offsec-specific.

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

- execute the `phase.0` task to re-verify live deltas, donor/recipient boundaries, and the current-compatible identity before target-repo mutation;
- execute the `phase.1` task to export, scaffold, bootstrap, and validate the baseline pack in the target repo;
- replace scaffold starter workflow metadata and land the first workflow docs;
- implement the locked authority-map question set and retention or freeze rules;
- land the first real CTF schemas, validators, and document-semantics service.

Near-term preserved work:

- execute `phase.2` through `phase.4` to land the machine contract, runtime seam, and challenge artifact model;
- execute `phase.5` to land knowledge promotion and retrieval;
- execute `phase.6` to land environment adapters and safety controls.

Later preserved work:

- execute `phase.7` portability proof after the full pack works end to end;
- revisit whether `workflow_catalog` is needed after the baseline pack works; and
- revisit pack-slug normalization and optional-segment path collapse after upstream fixes and migration tooling exist.

## First Post-Approval Execution Slice

After this hardening pass, the first ready engineer action is `task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment`. That task should:

1. reopen the canonical docs and mirrored `04_contracts/` surfaces in the read-first order above;
2. re-verify the current-compatible identity, donor/recipient split, and preserved live-contract deltas against current repo truth;
3. confirm no new live-contract delta needs to be recorded before target-repo mutation; and
4. hand off directly into `phase.1_recipient_scaffold_and_bootstrap`.

The first target-repo mutation then occurs in `phase.1`, which should:

1. export shared core from `/home/j/WatchTowerPlan/core`;
2. copy the staged export into `/home/j/WatchTower`;
3. scaffold `offensive_security/` there with the current-compatible baseline identity;
4. run `watchtower-core pack bootstrap --replace-hosted-packs --write` if donor pack wiring must be replaced;
5. run `pack validate`, `validate all`, and changed-schema validation; and
6. continue through the phase-ordered task chain preserved above.

## Gate

- No `/home/j/WatchTower` execution starts until this initiative is approved and marked `ready_for_execution`.
- The initiative stays in `ready_for_execution` until an engineer transitions the first ready task into an execution-starting status, at which point the normal initiative lifecycle will move into `in_progress`.
