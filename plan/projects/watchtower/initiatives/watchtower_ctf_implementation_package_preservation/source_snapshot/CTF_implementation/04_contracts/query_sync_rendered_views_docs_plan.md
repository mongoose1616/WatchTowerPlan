# Query, Sync, Rendered Views, And Docs Plan

## Curated V1 Query Inventory

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

## Generic Query Fallback

The pack should also expose a generic family-query fallback for every stable pack-owned family that becomes useful for operator or LLM retrieval.

Locked rules:

- curated commands remain the primary operator-facing surface for the highest-value families;
- generic family queries may expose both stable derived indexes and stable raw governed record families;
- generic family query must not degrade into an unbounded file browser over arbitrary `.wt` or `.wt_local` paths;
- command and workflow discovery remain on shared-core route and command lookup surfaces rather than gaining offsec-local aliases.

## Public Graph Query Contract

The pack should expose a public graph query surface for both operators and LLM or agent retrieval.

Locked posture:

- graph traversal operates across every artifact family with typed ids and typed relations, including challenge, knowledge, evidence, event, discrepancy, transfer, closeout, command, protocol, and related governed families;
- graph roots may be any typed artifact id from those relational families;
- traversal defaults to both incoming and outgoing direction;
- graph output supports `--format human|json|both`;
- graph traversal supports:
  - `--from`
  - `--depth`
  - `--direction`
  - `--relation`
  - `--family`
  - `--limit`
  - `--format`
  - `--status`
  - `--review-status`
  - `--trust-state`
  - `--verification-status`

## Query Service Shape

- follow the `plan` and `oversight` pattern of one query service per curated command with typed search-parameter dataclasses;
- use a two-tier model:
  - derived indexes by default
  - stable raw governed records when a family is intentionally queryable without its own derived index
- keep JSON field names stable across commands so rendered and machine consumers do not diverge;
- register query families in one pack-local registry and generate command docs from that registry so CLI, docs, and exposure policy do not drift.

## Curated Query Output Contract

Locked rules:

- curated query commands support `--format human|json|both`, with JSON as the default output posture;
- human output defaults to table-first rendering plus one-line row summaries where summary text materially improves scanability;
- default human columns remain command-specific but should be capped at six visible columns before verbose expansion;
- shared human presets are `compact`, `standard`, and `verbose`, and those preset names keep one pack-wide meaning across curated queries;
- default human row limits are command-specific, but the recommended cap is twenty rows;
- when row limits truncate results, human output shows omitted-count feedback and the exact flag needed to expand;
- zero-result human output shows the applied filters plus one or two likely next queries or flags rather than a bare “No results” message;
- compact trust or provenance cues may appear by default only when they materially affect interpretation;
- unsupported sort fields fail clearly and list the supported fields for that command rather than silently degrading.

## Shared Query Output Baseline

Use one shared baseline across offsec query rows where those fields are meaningful:

- `id`
- `status`
- `summary`
- `path`
- `updated_at_utc`

Treat family-specific row-shape expansion as additive on top of that baseline rather than command-specific drift.

## `status`, `challenges`, And `sessions` Human Contract

Locked rules:

- `status` is the main operator-context command rather than only a light pack summary;
- `status`, `challenges`, and `sessions` should share a visibly similar human structure so operators build muscle memory across the main orientation surfaces;
- `status` includes recommended next actions only when blockers, review gates, or safety limits materially constrain the next step.

## Locked `status` Query Expansion

When the `status` query is used to answer the authority-map safety-posture question, it must add:

- `effective_mode`
- `interaction_mode`
- `environment_type`
- `safety_posture_summary`
- `confirmation_summary`
- `refusal_summary`
- `policy_refs`

Locked rules:

- derive those fields from `safety_confirmation_matrix`, current session or environment context, and active governance limits rather than from freeform narrative;
- keep `policy_refs` pointed at the canonical machine policy and any relevant rendered human policy surface;
- do not advertise `watchtower-core offsec query status` as the preferred safety-posture command until those fields exist in the implemented output contract.

## Curated Relation Expansion Contract

Locked rules:

- curated family queries may expose relation expansion only through one shared `--expand-relations` flag;
- `--expand-relations` means one hop unless `--depth` is also provided;
- curated human expansion shows relation types, target ids, and one-line target summaries instead of fully switching to graph-style rendering;
- root rows and expanded relation targets use separate limits;
- default per-root expansion cap is five related targets;
- when relation expansion truncates, human output shows omitted counts and the exact flag needed to expand further;
- curated expansion reuses the graph-query `--relation`, `--family`, `--trust-state`, and `--review-status` flags rather than inventing family-specific variants;
- relation expansion may apply to every returned root row, subject to the per-root cap;
- graph-query suggestions appear only when relation expansion is truncated, and those suggestions should include a ready-to-run tailored graph command;
- `--focus <id>` is available only on `knowledge`, `artifacts`, `events`, and `discrepancies`;
- `--focus <id>` may target only rows already returned by the base query;
- `--focus <id>` narrows to that root and automatically enables one-hop relation expansion while also expanding row detail even without deeper traversal;
- named graph modes remain graph-query-only and are not accepted on curated family queries;
- curated family queries share one `--sort` flag with command-supported field lists.

## Public Graph Human Contract

Locked rules:

- public graph query is core for agents, but should be documented as advanced for humans while still appearing in pack examples;
- named graph modes are `operator`, `provenance`, `retrieval`, and `review`, and those modes act only as aliases for shared flag bundles;
- human graph traversal defaults to depth two, with aggressive output capping;
- human graph rendering defaults to a short root summary followed by relation-grouped neighbors;
- repeated nodes are deduplicated globally in human output with references back to the first occurrence;
- relation groups are ordered by relevance first, with fixed tie-breaks defined later in implementation docs;
- provenance-style relations remain inline in graph output but carry a visual marker rather than moving into a separate section;
- default node summaries in human graph output appear for the root and immediate neighbors only.

## `knowledge`, `commands`, And `references` Human Contract

Locked rules:

- umbrella `knowledge` human output always labels which family each result belongs to;
- `knowledge` groups results by family only when multiple families actually appear;
- grouped `knowledge` human output uses the fixed family order `tactics`, `playbooks`, `tools`, `commands`, `references`, then everything else;
- JSON output preserves pure retrieval ranking even when human output follows the fixed family order;
- human output shows a short ordering explanation only when multiple families appear and the displayed family order differs materially from pure ranking order;
- tactic groups are always visually distinguished from tool, command, and reference groups, and tactic groups use a stronger section heading style in addition to the family label;
- playbooks get their own visible section heading only when they appear alongside tactics or tool-centric families;
- when both tactics and playbooks appear, show `Tactics` first, then a distinct `Playbooks` section ordered by parent tactic and carrying a visible parent-tactic cue;
- when both tools and commands appear, show `Tools` first, then a distinct `Commands` section ordered by tool and carrying a visible tool cue;
- `References` remain a distinct section ordered by supported artifact family and item, with visible support cues;
- filtered `commands` and `references` stay flat by default instead of inheriting the full grouped-family behavior from umbrella `knowledge`;
- filtered `commands` may still group by tool only when multiple tools actually appear;
- filtered `references` may still group by supported family only when multiple supported families actually appear;
- when those filtered subgroupings are active, the subgroup header may satisfy the visible relationship-cue requirement unless later docs require per-row repetition;
- retrieval-heavy `knowledge`, `commands`, and `references` output reuses one “why this matched” explanation pattern, but only when ranking materially affects interpretation.

## Planned Supporting Machine Indexes

- `offensive_security/.wt/indexes/challenge_index.json`
- `offensive_security/.wt/indexes/blocker_index.json`
- `offensive_security/.wt/indexes/session_index.json`
- `offensive_security/.wt/indexes/knowledge_index.json`
- `offensive_security/.wt/indexes/artifact_index.json`
- `offensive_security/.wt/indexes/graph_index.json`

## Query-Family Registry

Canonical path:

- `offensive_security/.wt/registries/query_family_registry.json`

Locked role:

- register every curated and generic query family in one pack-local machine surface;
- declare whether the family is curated, generic-only, or both;
- declare the backing authoritative surface, output contract reference, and command-doc page;
- drive generated query docs and query-family overview docs from this registry.

## Initial Pack Sync Inventory

| Target | Purpose |
|---|---|
| `challenge-index` | rebuild challenge, blocker, session, artifact, and environment-oriented lookup surfaces |
| `knowledge-index` | rebuild reusable-knowledge indexes and companion summaries |
| `graph-index` | rebuild graph traversal structures from authoritative relations and indexed node metadata |
| `rendered-views` | rebuild pack-owned rendered markdown views |
| `all` | run the full deterministic derived-surface refresh |

## Sync Registry Shape

- implement sync targets through a canonical `watchtower_offensivesecurity.sync.registry` module exposing `SYNC_TARGET_SPECS`, following both reference packs;
- keep `challenge-index`, `knowledge-index`, `graph-index`, `rendered-views`, and `all` as the offsec namespace baseline;
- use generic shared sync surfaces for command, route, workflow, foundation, and reference indexes unless the offsec pack later proves a real need for pack-namespace aliases;
- `challenge-index` rebuilds pack challenge-state and evidence-navigation lookup surfaces;
- `knowledge-index` rebuilds knowledge indexes plus relation and promotion summary inputs;
- `graph-index` rebuilds the traversal-oriented graph index only;
- `rendered-views` rebuilds rendered markdown companions only;
- `all` runs the full deterministic pack-owned derived-surface refresh;
- do not add pack-specific aliases for shared route or workflow lookup in the offsec namespace in v1.

## Sync Versus Rebuild Rule

- keep public operator guidance aligned to the current `sync` family;
- use reusable `rebuild` primitives internally where shared core already exposes them;
- treat a public `rebuild` CLI split as a locked post-v1 deferral, not a first-pack baseline.

## Rendered View Plan

Pack-owned rendered views should include:

- `offensive_security/offensivesecurity_overview.md`
- `offensive_security/tracking/challenge_tracking.md`
- `offensive_security/tracking/blocker_tracking.md`
- `offensive_security/tracking/session_tracking.md`
- `offensive_security/tracking/knowledge_tracking.md`
- human-readable companion views for important machine artifacts where direct JSON browsing would be poor operator UX

## Authority-Map Contract

- author `offensive_security/.wt/registries/authority_map.json` against the shared `authority_map` schema;
- use the exact v1 question set in `04_contracts/authority_map_and_lookup_plan.md`;
- point recurring offsec questions at canonical machine indexes first and rendered overview or tracking docs second;
- keep command and workflow-routing discovery on the shared `command_index` and `route_index` surfaces where those already exist upstream.

## Documentation Plan

Pack-owned durable docs should include:

- namespace command docs under `offensive_security/docs/commands/core_python/`
- a query-family overview page under the same command-doc root
- a graph-query guide page under the same command-doc root
- workflow docs under `offensive_security/workflows/`
- standards and guides under pack-owned docs only once the pack exists in the target repo

## Document-Semantics Plan

The first document-semantics service should validate:

- repo-local markdown link integrity
- required sections and section order
- pack command-doc integrity
- workflow doc integrity
- challenge and recap structure once their templates exist
- query-family overview and graph-guide integrity once those docs are authored

## Reference-Pack Precedent

- both reference packs rebuild rendered visibility and tracking surfaces from machine state rather than treating them as authoritative writable surfaces;
- both reference packs centralize sync target declarations in Python registry modules rather than scattering target knowledge across CLI handlers.
