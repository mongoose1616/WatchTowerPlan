# Current Contract Baseline

## Source Precedence

1. `/home/j/mvp_reference/STEP1_FINAL_v3.md`
2. `/home/j/mvp_reference/STEP1_FINAL_v2.md`
3. `/home/j/mvp_reference/STEP1_FINAL.md`
4. `/home/j/mvp_reference/STEP1.md`
5. `/home/j/mvp_reference/STEP1_PACK_SCAFFOLD_SPEC_v1.md` as the runnable scaffold and bootstrap baseline

## Hosted-Pack Baseline

| Concern | Current Decision |
|---|---|
| pack topology | first-party root pack under `offensive_security/` |
| machine root | `offensive_security/.wt/` |
| docs root | `offensive_security/docs/` |
| workflows root | `offensive_security/workflows/` |
| tracking root | `offensive_security/tracking/` |
| python root | `offensive_security/python/` |
| domain roots | `offensive_security/ctf/`, `offensive_security/knowledge/` |

## Live Shared-Core Surfaces

The following shared-core governance surfaces exist upstream as of `2026-03-26` and should be treated as current contract, not future extension:

- `core/control_plane/registries/governance_surface_map.json`
- `core/control_plane/registries/path_pattern_registry.json`
- `core/control_plane/registries/status_registry.json`
- `core/control_plane/registries/actor_registry.json`

`watchtower_core.control_plane.pack_context.PackContext` now expects those surfaces when the caller needs full pack-context loading.

## Current-Compatible Identity Resolution

`STEP1_FINAL_v3.md` recommends underscore-safe identifiers, but the live scaffold proof confirms the current-compatible baseline is:

- `pack_slug = offensivesecurity`
- `pack_id = pack.offensivesecurity`
- `command_namespace = offsec`
- generated python package = `watchtower_offensivesecurity`
- generated integration module = `watchtower_offensivesecurity.integration`

This is the baseline until upstream scaffold/template propagation fully supports the future-normalized slug/package variant.

## Excluded Legacy Assumptions

Do not use:

- retired `/docs/**` authority assumptions;
- `domain_packs/**` topology;
- implicit future-state workflow-catalog assumptions;
- manual shared-core copying into the target repository.

## Proof Status

The following commands were rerun successfully on `2026-03-26` in a disposable exported core bundle:

- `watchtower-core pack export`
- `watchtower-core pack scaffold`
- `watchtower-core pack bootstrap`
- `watchtower-core pack validate`

The planning package should cite that proof in Phase 1 and in the scaffold baseline doc.
