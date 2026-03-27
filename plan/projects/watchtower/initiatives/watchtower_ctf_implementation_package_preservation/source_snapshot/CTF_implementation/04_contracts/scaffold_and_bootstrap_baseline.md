# Scaffold And Bootstrap Baseline

## Verified Scaffold Command

```sh
cd /home/j/WatchTowerPlan/core/python
PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack scaffold \
  --pack-slug offensivesecurity \
  --pack-root offensive_security \
  --command-namespace offsec \
  --domain-root ctf \
  --domain-root knowledge \
  --format json
```

## Verified Bootstrap And Validation Commands

```sh
cd /home/j/WatchTowerPlan/core/python
PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack bootstrap \
  --pack-settings-path offensive_security/.wt/manifests/pack_settings.json \
  --write \
  --format json

PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack validate \
  --pack-settings-path offensive_security/.wt/manifests/pack_settings.json \
  --format json
```

## Generated Starter Surface Set

- `offensive_security/.wt/manifests/pack_settings.json`
- `offensive_security/.wt/manifests/pack_runtime_manifest.json`
- `offensive_security/.wt/registries/schema_catalog.json`
- `offensive_security/.wt/registries/validation_suite_registry.json`
- `offensive_security/.wt/registries/workflow_metadata_registry.json`
- `offensive_security/.wt/registries/validator_registry.json`
- starter note schema and note artifact
- starter namespace command doc entry page
- pack `README.md`, workflow `README.md`, routing table, tracking `README.md`, python `README.md`

## Manifest Baseline

The package baseline is the current-compatible manifest pair proven in the disposable export:

- `pack_id = pack.offensivesecurity`
- `pack_slug = offensivesecurity`
- `command_namespace = offsec`
- owned roots under `offensive_security/`
- domain roots `ctf` and `knowledge`
- required capabilities:
  - `command_registration`
  - `query_runtime`
  - `sync_targets`
  - `validation_provider`

## Identity Deconfliction Rule

- `pack_slug = offensivesecurity` is the scaffold-compatible pack identity and must not be reused as the rule for challenge, knowledge, or workflow path slugs;
- pack-owned repository paths stay rooted under `offensive_security/`;
- challenge and knowledge slugs follow the pack-owned path/id rules in `04_contracts/path_and_id_generation_plan.md`.

## Immediate Next Slice

1. replace the scaffold starter workflow metadata entry with the real workflow IDs;
2. replace the starter note schema or artifact with challenge metadata, notes metadata, event stream, artifact index, and graph index;
3. replace placeholder query and sync inventories with the real curated, generic, and graph query inventories plus `graph-index`;
4. author `challenge_intake.md`, `environment_context.md`, `ctf_execution.md`, `challenge_closeout.md`, `safety_review.md`, and `discrepancy_reconciliation.md`;
5. add `offensive_security/docs/commands/core_python/README.md`, a query-family overview page, and a graph-query guide alongside `watchtower_core_offsec.md`;
6. add the first real document-semantics validation service for pack-owned docs and challenge artifacts.
