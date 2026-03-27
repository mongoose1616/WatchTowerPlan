# WatchTower CTF Implementation Package Preservation Design Record

## Summary

This initiative uses a two-layer preservation design: an immutable transformed mirror for source fidelity and canonical initiative docs for repo-native authority. The design keeps every implementation-supporting detail inside the WatchTower project initiative while avoiding validator collisions from raw mirrored JSON.

## Design Goals

- make the initiative self-sufficient if `/home/j/mvp_reference/CTF_implementation` disappears;
- preserve the source package byte-for-byte wherever practical;
- keep canonical implementation guidance in the initiative’s four governed authored docs;
- avoid creating parallel plan-artifact families or validator drift; and
- preserve the donor/recipient boundary so the preservation initiative does not begin implementing `/home/j/WatchTower`.

## Preservation Architecture

### 1. Transformed Mirror Layer

- The source snapshot lives under `source_snapshot/CTF_implementation/`.
- Non-JSON files retain the same relative path and filename.
- Source `*.json` files retain the same relative path, but add a `.raw` suffix.
- The transformed mirror is frozen after capture and may only be replaced through an explicit recapture pass.

### 2. Proof And Coverage Layer

- `source_original_inventory.txt` records the sorted original relative paths.
- `source_stored_inventory.txt` records the sorted stored relative paths after the `.json.raw` transform.
- `source_sha256.tsv` records the source digest plus original and stored paths for every mirrored file.
- `source_coverage_matrix.md` forces every source file to name a canonical initiative surface or explicit mirror-only reference target.
- `source_capture_notes.md` records mirror policy, counts, and restore expectations.

### 3. Canonical Authored Layer

- `initiative_brief.md` carries package purpose, authority order, baseline identity, package inventory, and acceptance expectations.
- `design_record.md` carries preservation rationale, validator-safe storage rules, authority boundaries, and donor/recipient split.
- `implementation_slice.md` carries phases, workflow topology, contract bundles, research posture, standards, tracking surfaces, and the first post-approval execution slice.
- `decision_notes.md` carries the locked default set, live deltas, post-v1 deferrals, and the source normalization rule for the decision register.

### 4. Live Machine State Layer

- `.wt/**` remains the authoritative machine state for the initiative.
- Support files remain ordinary initiative-root material and are referenced by the canonical docs, but are not inserted into `authored_inputs` because the initiative-state schema only accepts the four canonical doc kinds.

## Why The Mirror Uses `.json.raw`

The plan validator recursively inspects `*.json` files under an initiative root and expects them to conform to governed artifact families. The imported package contains donor-package JSON companions such as `indexes/package_manifest.json`, `indexes/phases.json`, and `indexes/open_decisions.json` that are not initiative-governed artifacts. Storing them as raw `*.json` inside the initiative root would create false validation failures and readiness noise.

The `.json.raw` suffix is therefore a deliberate storage shim with three properties:

- it preserves source bytes exactly;
- it is reversible by stripping the trailing `.raw` suffix during restore proof; and
- it keeps the initiative validator focused on actual governed artifacts.

## Authority And Ownership Boundaries

The imported package does not override live repo authority when they disagree. The preserved authority order is:

1. current plan-pack and core machine-readable contract surfaces;
2. current repo standards and command docs;
3. the preserved CTF planning package as the implementation-planning input;
4. donor-pack precedents from `plan` and `oversight`; and
5. the empty recipient repo at `/home/j/WatchTower`, which remains a destination only until execution starts.

This initiative also preserves the donor/recipient split:

- donor shared core and source contract: `/home/j/WatchTowerPlan/core`
- donor working hosted-pack references: `/home/j/WatchTowerPlan/plan`, `/home/j/WatchTowerOversight/oversight`
- recipient implementation repo: `/home/j/WatchTower`

## Source Normalization Allocation

| Canonical Surface | Source Families Normalized Into It |
|---|---|
| `initiative_brief.md` | `README.md`, baseline context docs, source-of-truth map, Step 1 source and trace surfaces, capability maps, package acceptance standard, inventory counts |
| `design_record.md` | preservation rationale, transformed-mirror rule, donor/recipient split, live contract deltas, reference-pack precedent review, support-file placement rationale |
| `implementation_slice.md` | phase docs, workflow docs, contract bundles, research anchors, standards posture, guides, backlog, dependency register, risk register, next execution slice |
| `decision_notes.md` | `indexes/open_decisions.json`, implementation gap audit, deferred review register, decision-to-contract propagation rules, live contract deltas that lock defaults |

## Live Contract Delta Adoption

The design preserves the package’s explicit delta handling so future implementation does not silently regress to workbook-era assumptions.

- Keep the scaffold-proof identity baseline: `pack_slug = offensivesecurity`, `pack_id = pack.offensivesecurity`, `command_namespace = offsec`.
- Adopt live shared-core surfaces now present upstream: `actor_registry`, `governance_surface_map`, `path_pattern_registry`, and `status_registry`.
- Adapt challenge and session lifecycle subsets to shared status vocabulary rather than inventing pack-only lifecycle statuses such as `solved` or `unresolved`.
- Reject retired `domain_packs/**` topology and retired docs-root authority assumptions.
- Keep the fixed-root challenge path with placeholder segments in v1 and defer optional-segment collapse beyond v1.
- Treat the empty recipient repo as a real implementation constraint rather than assuming existing WatchTower content.
- Keep `workflow_catalog` as a deliberate post-v1 deferral rather than a missing v1 prerequisite.

## Reference-Pack Precedent Rationale

The source package correctly relies on `plan` and `oversight` as implementation-pattern references. This initiative preserves the same precedent reasoning:

- keep the four-capability pack integration seam of command registration, query runtime, sync targets, and validation provider;
- keep `ROUTING_TABLE.md` as an authored routing authority and pair it with workflow metadata rather than inventing a new runtime entry model;
- reuse the donor-pack baseline validation suite shape before adding offsec-specific suites;
- adopt pack-local control registries for artifact families, documentation families, templates, rendered surfaces, authority routing, lifecycle policy, and promotion policy;
- preserve rendered visibility as governed surfaces rather than ad hoc markdown; and
- keep environment adapters, offensive-security safety taxonomy, redaction rules, and challenge-specific evidence behavior as pack-native work with no false donor precedent.

## Failure Modes And Mitigations

| Failure Mode | Mitigation |
|---|---|
| source directory is deleted after capture | the transformed mirror plus support manifests preserve all source files and restore proof inputs inside the initiative |
| source markdown and structured companions drift from canonical docs | `source_coverage_matrix.md`, source inventories, and repeated sync/query validation make drift visible |
| raw donor JSON is mistaken for initiative-governed artifacts | `.json.raw` storage keeps donor companions outside validator selection |
| follow-on implementation re-derives already-locked defaults | `decision_notes.md` captures the normalized decision set and the mirror preserves the full raw register |
| preservation work accidentally mutates recipient implementation state | the initiative records the first `/home/j/WatchTower` execution slice but does not execute it |
