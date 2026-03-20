# Domain Pack Integration Workflow

## Purpose
Use this workflow to implement or refactor the reusable-core, host-runtime, and pack-runtime boundary so hosted packs integrate through explicit contracts instead of direct imports or hidden repository coupling.

## Use When
- A task introduces or refactors `watchtower_core`, `watchtower_host`, or `watchtower_<pack>` boundaries.
- A change adds pack discovery, pack command registration, pack manifests, pack-owned command docs, or pack portability work.
- A repository needs to make one pack externalizable without rewriting core code.

## Inputs
- Scoped architecture or implementation brief
- Applicable requirements, decisions, standards, and local references
- Current dependency direction and import-boundary evidence
- Existing pack registry, pack settings, and runtime manifest state
- Command, docs, workflow, and validation surfaces affected by the refactor

## Workflow
1. Define the intended layer split.
   - Confirm what belongs in reusable core, host composition, and the owning pack.
   - Confirm command ownership, docs ownership, and pack portability expectations before editing.
2. Map the integration seam.
   - Identify the typed hooks, manifests, registry entries, and validation surfaces the pack must publish.
   - List the existing direct imports, duplicated helpers, or flat commands that must be removed.
3. Implement the cutover.
   - Move reusable behavior into `watchtower_core`, host composition into `watchtower_host`, and pack-native behavior into the owning pack.
   - Update companion docs, routing, and machine-readable contract surfaces in the same change set.
4. Validate the contract.
   - Run pack-interface validation, import-boundary checks, and targeted command or portability proofs.
   - Fail closed on namespace collisions, missing hooks, invalid manifests, or hidden repository-only assumptions.

## Data Structure
- Layer ownership map
- Integration contract summary
- Direct-import residue list
- Updated companion docs and contract surfaces
- Validation results and remaining risks

## Outputs
- A host-pack integration change with explicit boundaries
- Updated manifests, standards, command docs, and workflow routing when affected
- Validation evidence for the new pack boundary

## Done When
- The changed behavior routes through explicit host-pack integration points.
- Direct reusable-core imports of pack-native runtime are removed or explicitly tracked as follow-up work.
- Companion docs, contract artifacts, and validation surfaces are aligned with the new boundary.
