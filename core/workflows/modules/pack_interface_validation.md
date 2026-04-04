# Pack Interface Validation Workflow

## Purpose
Use this workflow to validate that a hosted pack publishes the required machine contracts, Python hooks, owned roots, and portability guarantees expected by reusable core and host composition.

## Use When
- A task adds or changes `pack_registry`, `pack_runtime_manifest`, or typed pack integration hooks.
- A review needs explicit pack-interface validation beyond general code testing.
- A portability or extensibility change could break future hosted packs or copied-out pack roots.

## Inputs
- Scoped validation brief
- Pack registry and runtime manifest surfaces in scope
- Typed integration contracts and declared capabilities
- Command namespace expectations
- Pack-owned docs, workflows, tracking, and Python roots

## Workflow
1. Define the validation boundary.
   - Confirm which pack or packs are in scope and which capabilities they declare.
   - Confirm the authoritative registry, manifest, and package surfaces.
2. Validate machine contracts.
   - Check schema validity, required fields, owned-root consistency, named `domain_roots`, and declared validation-suite coverage.
   - Check namespace uniqueness and registry-manifest consistency.
   - Check that shared `core/python/pyproject.toml` registers the hosted-pack distribution in optional dev dependencies and `tool.uv.sources`.
   - Check that manifest paths stay under `machine_root/manifests/` and that pack-settings surfaces remain either pack-local or explicitly shared under `core/control_plane/`.
3. Validate Python integration hooks.
   - Confirm the integration module imports cleanly.
   - Confirm the integration module stays under the declared pack python package.
   - Confirm declared hooks exist and return the expected typed runtime surfaces.
4. Validate portability expectations.
   - Check that pack-owned docs, workflows, tracking, and Python surfaces exist where declared.
   - Check that the pack-owned docs root publishes the namespace command entry page for the pack.
   - Check that reusable core does not import the pack and the pack does not import host internals.
   - Check that the pack is importable from its own `<pack>/python/src` path or installed package root rather than only from repository-root import assumptions.
   - When the host-pack contract changed materially, prove it against at least one non-default or synthetic second-pack fixture instead of validating only the current default pack.
   - Treat clean-room interoperability and staged artifacts as first-class proof surfaces, not optional extras.
   - Check for hidden coupling to local paths, local caches, donor pack sets, or repo-specific state that would break portability.
   - Build staged exports or disposable copies and inspect them for leaked caches, local paths, stale copied core, machine-state contamination, or missing owned surfaces.
   - Distinguish `baseline_core`, `repo_core_drift`, `pack_owned`, and `cross_boundary` issues when reporting portability findings.

## Data Structure
- In-scope pack list
- Contract surfaces checked
- Hook validation results
- Portability findings
- Residual risks or follow-up work

## Outputs
- A structured validation result for the scoped pack interface
- Explicit findings for manifest, hook, namespace, or portability drift
- Explicit confirmation that the pack-owned Python root and namespace command docs satisfy the externalization contract
- Follow-up work when the contract is not yet satisfied

## Done When
- The in-scope pack interface has been validated against its declared contract.
- Failures are resolved or explicitly recorded.
- The result distinguishes machine-contract issues from runtime, docs, or portability issues.
