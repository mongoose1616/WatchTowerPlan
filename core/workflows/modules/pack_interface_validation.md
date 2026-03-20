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
   - Check schema validity, required fields, owned-root consistency, and declared validation-suite coverage.
   - Check namespace uniqueness and registry-manifest consistency.
3. Validate Python integration hooks.
   - Confirm the integration module imports cleanly.
   - Confirm declared hooks exist and return the expected typed runtime surfaces.
4. Validate portability expectations.
   - Check that pack-owned docs, workflows, tracking, and Python surfaces exist where declared.
   - Check that reusable core does not import the pack and the pack does not import host internals.
   - When the host-pack contract changed materially, prove it against at least one non-default or synthetic second-pack fixture instead of validating only the current default pack.

## Data Structure
- In-scope pack list
- Contract surfaces checked
- Hook validation results
- Portability findings
- Residual risks or follow-up work

## Outputs
- A structured validation result for the scoped pack interface
- Explicit findings for manifest, hook, namespace, or portability drift
- Follow-up work when the contract is not yet satisfied

## Done When
- The in-scope pack interface has been validated against its declared contract.
- Failures are resolved or explicitly recorded.
- The result distinguishes machine-contract issues from runtime, docs, or portability issues.
