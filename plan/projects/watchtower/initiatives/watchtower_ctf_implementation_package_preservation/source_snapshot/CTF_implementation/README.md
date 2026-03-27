# WatchTower CTF Planning Package

## Purpose

This package is the implementation-ready planning bundle for the first WatchTower offensive-security / CTF hosted pack. It is intentionally planning-only and does not modify `/home/j/WatchTower` yet.

The package is built from the Step 1 document chain in `/home/j/mvp_reference`, current shared-core and hosted-pack contract surfaces in `/home/j/WatchTowerPlan/core`, working pack patterns in `/home/j/WatchTowerPlan/plan` and `/home/j/WatchTowerOversight/oversight`, and target-repository integration requirements for `/home/j/WatchTower`.

## Current Baseline

- Source precedence: `STEP1_FINAL_v3.md` > `STEP1_FINAL_v2.md` > `STEP1_FINAL.md` > `STEP1.md`.
- Runnable scaffold baseline: `STEP1_PACK_SCAFFOLD_SPEC_v1.md`.
- Verified current-compatible identity:
  - `pack_root = offensive_security`
  - `workspace_root = offensive_security/`
  - `pack_slug = offensivesecurity`
  - `pack_id = pack.offensivesecurity`
  - `command_namespace = offsec`
- Shared core now exposes `governance_surface_map`, `path_pattern_registry`, `status_registry`, and `actor_registry` and those surfaces should be adopted in the pack machine contract.
- As of `2026-03-26`, `/home/j/WatchTower` contains only `.git` metadata and should be treated as the empty destination repository.

## Navigation

- `00_context/`: source map, line-by-line Step 1 audit, decision-to-contract trace checklist, live contract baseline, reference implementation map, precedent review, and conflict log.
- `01_capability_map/`: capability classifications and coverage mapping for workbook sections and refinement groups.
- `02_phases/`: phase-by-phase execution docs for Phase 0 through Phase 7.
- `03_workflows/`: workflow topology, workflow inventory, and routing/metadata plan.
- `04_contracts/`: scaffold baseline, path/id generation plan, schema/registry/ledger/validation plan, artifact payload contracts, state/index/reconciliation contracts, routing/runtime contracts, control-plane registry contracts, rendered-surface contracts, lifecycle/safety policy contracts, knowledge governance/retrieval plan, environment/safety execution plan, authority-map and lookup plan, query/sync/rendered-view plan, retention/cleanup policy, and core export/bootstrap plan.
- `05_research/`: authoritative research register and distilled implications.
- `06_standards/`: package-derived implementation standards.
- `07_guides/`: operator-facing and implementer-facing execution guides.
- `08_tracking/`: backlog, dependencies, risks, implementation gap audit, and deferred review register.
- `indexes/`: lightweight machine-readable package indexes.

## Acceptance Standard

The package is complete only when:

- every required document exists;
- every JSON file under `indexes/` parses cleanly;
- every workbook section `A-J`, every `Q01-Q70`, and every `R01-R90` is mapped explicitly, with `R69-R72` marked as absent from the source set;
- every non-`Q/R` Step 1 source range is accounted for in `00_context/step1_line_by_line_deconfliction_audit.md` and `indexes/step1_source_audit.json`;
- every omission, adaptation, supersession, or deferment is explicit; and
- the docs and indexes agree on phases, artifact paths, research metadata, and capability classifications.

## Verified Proof Inputs

The runnable scaffold baseline was revalidated on `2026-03-26` in a disposable exported core bundle using:

```sh
cd /home/j/WatchTowerPlan/core/python
PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack export --output-root /tmp/<proof> --overwrite --format json

cd /tmp/<proof>/core/python
PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack scaffold \
  --pack-slug offensivesecurity \
  --pack-root offensive_security \
  --command-namespace offsec \
  --domain-root ctf \
  --domain-root knowledge \
  --format json

PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack bootstrap \
  --pack-settings-path offensive_security/.wt/manifests/pack_settings.json \
  --write \
  --format json

PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack validate \
  --pack-settings-path offensive_security/.wt/manifests/pack_settings.json \
  --format json
```

## Recommended First Execution Slice

After planning, the first execution slice should:

1. scaffold and bootstrap the pack with the runnable identity above;
2. replace starter workflow metadata and author workflow docs in parallel;
3. land the first machine-record bundle of challenge metadata, notes metadata, event stream, artifact index, graph index, session state, and environment context;
4. prove a thin real-CLI vertical slice on the actual pack root through `challenge_intake -> challenge_metadata + notes_metadata + event_stream + artifact_index + offsec query challenges + offsec query artifacts`;
5. add unit tests and CLI smoke tests immediately after that slice works end-to-end;
6. then prove `session_state + environment_context + offsec query status`, then `discrepancy + blockers`, then `knowledge`;
7. ship the first public graph query after curated queries and sync targets stabilize and after `knowledge` is proven;
8. run a short packaging/UX consolidation pass; and
9. run the first real challenge flow on a deliberately small or simple target.
