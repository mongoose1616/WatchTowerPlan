# WatchTower CTF Implementation Package Preservation

## Summary

This initiative absorbs `/home/j/mvp_reference/CTF_implementation` into the governed WatchTower planning workspace so the implementation package survives independently of that external directory. The preserved initiative includes a validator-safe transformed mirror of all `62` source files, parity manifests that prove nothing was dropped, and canonical initiative documents that capture the package purpose, baseline, design rationale, implementation sequencing, and locked decisions needed to build WatchTower.

## Identity

- `initiative_id`: `initiative.watchtower_ctf_implementation_package_preservation`
- `trace_id`: `trace.watchtower_ctf_implementation_package_preservation`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `source_root`: `/home/j/mvp_reference/CTF_implementation`
- `target_repo`: `/home/j/WatchTower`
- `transformed_mirror_root`: `source_snapshot/CTF_implementation/`

## Problem Statement

- The CTF planning package is implementation-ready, but it currently lives outside the governed WatchTower project initiative tree.
- Deleting `/home/j/mvp_reference/CTF_implementation` before transfer would remove implementation-critical planning detail, including phase sequencing, contract baselines, locked defaults, research anchors, and Step 1 coverage evidence.
- A raw copy of the package into the initiative root would introduce unmanaged `*.json` files that the plan validator would attempt to treat as governed initiative artifacts.

## Goals

- Preserve every implementation-supporting detail from the source package inside this initiative.
- Keep the preserved package recoverable and auditable through source inventory, digests, and reversible JSON restoration.
- Normalize the source package into repo-native initiative surfaces so follow-on implementation can begin from this initiative alone.
- Keep the initiative approval and readiness path compatible with the current `plan/.wt` validation contract.

## Non-Goals

- Do not mutate `/home/j/WatchTower` during this preservation initiative.
- Do not alter repo-wide readiness rules, artifact validation behavior, or validator selection.
- Do not replace the transformed mirror with a reauthored summary; the source snapshot remains the frozen provenance layer.

## Governing Inputs And Authority Order

1. Current repo machine-readable authority in `plan/.wt/**` and `core/control_plane/**`
2. Current foundations, standards, and command docs under `core/docs/**` and `plan/docs/**`
3. The imported CTF planning package preserved under `source_snapshot/CTF_implementation/**`
4. Step 1 workbook source precedence retained by the package:
   - `STEP1_FINAL_v3.md`
   - `STEP1_FINAL_v2.md`
   - `STEP1_FINAL.md`
   - `STEP1.md`
   - `STEP1_PACK_SCAFFOLD_SPEC_v1.md` as the runnable scaffold and bootstrap baseline
5. Working donor-pack references at `/home/j/WatchTowerPlan/plan` and `/home/j/WatchTowerOversight/oversight` as implementation-pattern references, not higher authority

## Verified Current Baseline

| Concern | Locked Baseline |
|---|---|
| package purpose | planning-only bundle for the first WatchTower offensive-security / CTF hosted pack |
| pack root | `offensive_security` |
| workspace root | `offensive_security/` |
| pack slug | `offensivesecurity` |
| pack id | `pack.offensivesecurity` |
| command namespace | `offsec` |
| domain roots | `ctf`, `knowledge` |
| canonical challenge path | `offensive_security/ctf/<platform>/<event>/<challenge>/` with stable placeholders such as `unknown_platform` and `unknown_event` |
| live shared-core additions to adopt | `governance_surface_map`, `path_pattern_registry`, `status_registry`, and `actor_registry` |
| locked v1 deferral | `workflow_catalog` remains a post-v1 deferral rather than a baseline requirement |
| destination repo state as of `2026-03-26` | `/home/j/WatchTower` contains only `.git` metadata and is treated as empty |

## Source Package Scope And Inventory

The source package is preserved in full and accounted for through both the transformed mirror and support manifests.

| Source Family | File Count |
|---|---|
| `00_context` | `10` |
| `01_capability_map` | `3` |
| `02_phases` | `8` |
| `03_workflows` | `3` |
| `04_contracts` | `15` |
| `05_research` | `2` |
| `06_standards` | `4` |
| `07_guides` | `3` |
| `08_tracking` | `5` |
| `README.md` | `1` |
| `indexes` | `8` |

The package acceptance standard retained by this initiative requires:

- every required document to exist;
- every JSON file under the source `indexes/` family to parse cleanly;
- every workbook section `A-J`, every `Q01-Q70`, and every `R01-R90` to be mapped explicitly, with `R69-R72` recorded as absent from the source set;
- every non-`Q/R` Step 1 source range to be accounted for through the line-by-line audit and machine companion indexes; and
- all omissions, adaptations, supersessions, and deferrals to remain explicit.

## Durable Requirements

- `req.watchtower_ctf_package_preservation.001`: preserve all `62` source files inside this initiative with deterministic stored paths and reversible JSON restoration.
- `req.watchtower_ctf_package_preservation.002`: preserve source provenance through `source_original_inventory.txt`, `source_stored_inventory.txt`, `source_sha256.tsv`, and `source_coverage_matrix.md`.
- `req.watchtower_ctf_package_preservation.003`: capture the current-compatible baseline identity, authority order, live contract deltas, and donor/recipient split in canonical initiative docs.
- `req.watchtower_ctf_package_preservation.004`: preserve both human-readable source docs and machine-companion indexes so implementation does not depend on reopening the external source directory.
- `req.watchtower_ctf_package_preservation.005`: keep the preserved package validator-safe by storing mirrored JSON as `.raw` files rather than raw initiative-root `*.json` artifacts.
- `req.watchtower_ctf_package_preservation.006`: leave this initiative sufficient to bootstrap and implement WatchTower in `/home/j/WatchTower` after approval, without executing that implementation here.

## Acceptance Criteria

- `ac.watchtower_ctf_package_preservation.001`: the initiative mirror contains exactly `62` stored files corresponding to the `62` source files.
- `ac.watchtower_ctf_package_preservation.002`: the transformed mirror preserves source bytes exactly, as proven by `source_sha256.tsv` and restore proof for mirrored JSON files.
- `ac.watchtower_ctf_package_preservation.003`: every source file appears in `source_coverage_matrix.md` with a canonical target and explicit status.
- `ac.watchtower_ctf_package_preservation.004`: the canonical initiative docs absorb the package purpose, baseline, phase plan, contracts, research posture, standards, tracking surfaces, and locked decision set.
- `ac.watchtower_ctf_package_preservation.005`: after sync, confirm-inputs, and approval, the initiative reaches `ready_for_execution=true`.

## Risks And Dependencies

Primary dependencies preserved from the source package:

- current shared pack commands for `pack export`, `pack scaffold`, `pack bootstrap`, `pack validate`, and release proof;
- current shared governance surfaces for pack context, status vocabulary, actor vocabulary, and path rules;
- donor-pack implementation patterns from `plan` and `oversight`;
- research anchors from ATT&CK, OWASP WSTG, NIST guidance, and Diataxis, always subordinate to current repo truth.

Primary risks carried forward from the package:

- slug normalization drift could invalidate the current-compatible scaffold identity;
- Step 1 workbook assumptions can drift from live shared-core truth;
- workflow starter metadata could remain in place too long after scaffold;
- markdown docs and structured indexes can diverge if not synchronized in one change set;
- environment and safety behavior can be implemented unsafely if the Phase 6 contract is treated as optional.

## Initial Task Set

- `task.watchtower_ctf_implementation_package_preservation.bootstrap_watchtower_ctf_implementation_package_preservation`: Bootstrap WatchTower CTF Implementation Package Preservation live initiative package.
