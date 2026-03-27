# Phase 3: Build The CTF Runtime

## Purpose

Implement the pack-owned runtime seam that exposes offensive-security behavior through the shared host and reusable-core contracts.

## In-Scope Surfaces

- `PACK_INTEGRATION`
- namespace command registration
- pack query runtime
- pack sync runtime
- pack-owned document-semantics validation
- authored workflow docs and routing

## Exact Planned Files, Schemas, Registries, Ledgers, Workflows, Validators, And Command Surfaces

- `watchtower_offensivesecurity.integration.PACK_INTEGRATION`
- `watchtower_offensivesecurity.query.status`
- `watchtower_offensivesecurity.query.challenges`
- `watchtower_offensivesecurity.query.knowledge`
- `watchtower_offensivesecurity.query.sessions`
- `watchtower_offensivesecurity.query.blockers`
- `watchtower_offensivesecurity.query.artifacts`
- `watchtower_offensivesecurity.query.events`
- `watchtower_offensivesecurity.query.environment`
- `watchtower_offensivesecurity.query.discrepancies`
- `watchtower_offensivesecurity.query.closeout`
- filtered `commands` and `references` views over the reusable-knowledge query surface
- generic family query fallback
- public graph query runtime
- `watchtower_offensivesecurity.sync.registry`
- `offensive_security/.wt/registries/authority_map.json`
- `offensive_security/.wt/registries/query_family_registry.json`
- pack index outputs:
  - `offensive_security/.wt/indexes/challenge_index.json`
  - `offensive_security/.wt/indexes/blocker_index.json`
  - `offensive_security/.wt/indexes/session_index.json`
  - `offensive_security/.wt/indexes/knowledge_index.json`
  - `offensive_security/.wt/indexes/artifact_index.json`
  - `offensive_security/.wt/indexes/graph_index.json`
- rendered visibility outputs:
  - `offensive_security/offensivesecurity_overview.md`
  - `offensive_security/tracking/challenge_tracking.md`
  - `offensive_security/tracking/blocker_tracking.md`
  - `offensive_security/tracking/session_tracking.md`
  - `offensive_security/tracking/knowledge_tracking.md`
- pack query inventory:
  - `status`
  - `challenges`
  - `knowledge`
  - `sessions`
  - `blockers`
  - `artifacts`
  - `events`
  - `environment`
  - `discrepancies`
  - `closeout`
  - `commands`
  - `references`
- pack sync targets:
  - `challenge-index`
  - `knowledge-index`
  - `graph-index`
  - `rendered-views`
  - `all`
- workflow modules:
  - `challenge_intake`
  - `environment_context`
  - `ctf_execution`
  - `blocker_recovery`
  - `knowledge_capture`
  - `challenge_closeout`
  - `safety_review`
  - `discrepancy_reconciliation`
- workflow roles:
  - `ctf_operator`
  - `ctf_reviewer`
  - `ctf_safety_reviewer`
  - `ctf_discrepancy_reviewer`
  - `ctf_knowledge_reviewer`
- first pack-owned document-semantics validation service for challenge and pack docs

## Locked Runtime Rollout Sequence

1. author workflow metadata and workflow docs in parallel with the first machine-record slice;
2. land `challenge_metadata`, `notes_metadata`, `event_stream`, `artifact_index`, `graph_index`, `session_state`, and `environment_context` together;
3. prove a thin vertical slice through `challenge_intake -> challenge_metadata + notes_metadata + event_stream + artifact_index + offsec query challenges + offsec query artifacts` on the real pack root through the real CLI using real schemas and validators;
4. add unit tests and CLI smoke tests immediately after that slice works end-to-end;
5. next prove `session_state + environment_context + offsec query status`;
6. then prove `discrepancy + blockers`;
7. then prove `knowledge`;
8. ship the first public graph query after curated queries and sync targets stabilize and after `knowledge` is also proven;
9. run a short packaging and UX consolidation pass after the first three core vertical slices;
10. run the first real challenge flow on a deliberately small or simple target as soon as those first three core vertical slices are stable.

## Dependencies

- Phase 1 scaffolded python/docs/workflow roots
- Phase 2 schema and validator plan
- working pack patterns from `plan` and `oversight`

## Upstream Assumptions

- host remains responsible only for CLI composition and dispatch
- pack-owned validation services are loaded through the validation provider hook

## Validation And Acceptance Criteria

- query runtime and sync runtime inventories are non-empty and concrete
- workflow inventory and workflow metadata registry match
- initial routing-table task types map only to authored workflow modules or roles in the same slice; `safety_review` and `discrepancy_reconciliation` are standalone routed modules that may also compose as overlays
- workflow metadata, route-index, and route-preview behavior align with `04_contracts/routing_and_runtime_contracts_plan.md`
- challenge, blocker, session, and knowledge index row contracts align with `04_contracts/state_and_index_contracts_plan.md`
- public graph-query behavior and `graph_index` contract align with `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/state_and_index_contracts_plan.md`
- curated query human output, relation-expansion behavior, and grouped-knowledge behavior align with `04_contracts/query_sync_rendered_views_docs_plan.md`
- rendered-surface registry shape and starter tracking-surface posture align with `04_contracts/rendered_surface_contracts_plan.md`
- `status` query output explicitly carries the safety-posture summary and confirmation-gate fields required by `authority.offsec.safety_posture`
- `status`, `challenges`, and `sessions` share a coherent human output structure once human rendering is selected
- the package defines how pack-owned docs route through document-semantics validation
- command docs stay pack-owned under the offensive-security docs root
- query-family overview and graph-guide docs stay pack-owned under the offensive-security command-doc root
- the authority map points to real query outputs, real rendered views, and real shared command or route surfaces

## Risks And Unresolved Questions

- further pack-native command families may appear once the runtime grows beyond the initial surface
- the first document-semantics service must avoid forking reusable core logic that already exists upstream

## Exit Criteria

- the package describes a complete runtime seam from host namespace to pack validation/query/sync/workflow behavior
