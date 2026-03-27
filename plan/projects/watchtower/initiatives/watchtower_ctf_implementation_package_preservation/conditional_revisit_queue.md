# WatchTower CTF Conditional Revisit Queue

## Summary

The preserved package does not currently have blocking open decisions. This queue captures the non-blocking decisions that should only be reopened if later execution evidence forces a revisit. If a trigger does not fire, the current locked default remains in force.

## Revisit Rules

- Treat this queue as a trigger-based supplement to `decision_notes.md`, not as a second open-decision register.
- Do not reopen an item just because implementation reaches the listed phase; reopen it only if the specific trigger condition is met.
- When a trigger fires, record the change as a new live-contract delta and then update the affected canonical docs, task state, acceptance evidence, and registry or policy surfaces in the same change set.

## Conditional Revisit Items

| Revisit ID | Current Default | Reopen If | Earliest Phase | Keep-Default Behavior If Trigger Does Not Fire |
|---|---|---|---|---|
| `revisit.workflow_catalog` | keep `ROUTING_TABLE.md` plus `workflow_metadata_registry.json` as the v1 routing baseline | route discovery, workflow search, or workflow composition becomes too ambiguous to manage through the existing pair | `phase.3` | keep `workflow_catalog` deferred and avoid building a second workflow authority surface |
| `revisit.actor_bootstrap_day_one` | reuse shared `actor_registry` and defer pack-specific actor bootstrap | strict actor-ref validation proves impossible or misleading without pack-local seed actors immediately | `phase.2` | keep actor bootstrap deferred and rely on shared actor surfaces plus explicit actor-ref rules |
| `revisit.public_rebuild_cli` | keep operator-facing guidance centered on `sync` rather than a separate rebuild CLI | operator evidence shows `sync` cannot express needed rebuild scopes clearly enough | `phase.3` | keep public guidance on `sync` and avoid parallel rebuild-only verbs |
| `revisit.saved_query_views` | defer saved query views beyond v1 | real offsec query usage shows repeated manual query composition is a material operator burden | `phase.3` or `phase.5` | keep queries stateless and governed by command flags plus rendered trackers |
| `revisit.provenance_review_impact_surface` | defer richer downstream provenance-impact tooling beyond v1 | accepted knowledge routinely needs downstream review sweeps that current review status and provenance fields cannot express clearly | `phase.5` or `phase.6` | keep provenance-triggered review handling narrow and explicit on affected artifacts only |
| `revisit.pentest_pack_split` | keep one `offensive_security` hosted pack for v1 | product scope or runtime boundaries prove that CTF and later pentest behavior cannot coexist cleanly in one pack | `phase.5` or later | keep one hosted pack and pack-owned internal domain roots |
| `revisit.challenge_path_optional_segments` | keep fixed challenge paths with placeholder `platform` and `event` segments in v1 | real challenge intake evidence shows placeholder segments cause unacceptable path churn or operator confusion | `phase.4` | keep fixed-root paths with governed rename handling rather than optional-segment collapse |
| `revisit.docs_agents_root` | keep `offensive_security/docs/AGENTS.md` optional | the docs subtree gains local behavior that materially differs from the pack root rules | `phase.1` or `phase.2` | keep the docs root governed only by the pack root `AGENTS.md` plus pack-local registries |

## Governing Surfaces When A Revisit Fires

- `decision_notes.md`
- `implementation_slice.md`
- `initiative_brief.md`
- `phase_output_manifest.md`
- `phase_closeout_checklists.md`
- `starter_surface_blueprint.md` when starter-surface posture changes
- `starter_registry_exemplars.md` when starter-registry posture changes
- `contradiction_sweep_ledger.md` when a resolved tension must be reopened or superseded
- the affected live task records under `.wt/tasks/**/task.json`
