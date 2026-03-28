# Test Suite Optimization Workflow

## Purpose
Use this workflow to reduce test-runtime cost without dropping the active proof that the repository still needs.

## Use When
- A test or validation slice has become slow enough to interfere with routine development or repository validation.
- A contributor needs to refactor tests, fixtures, or harness usage so one broad proof becomes a smaller set of faster targeted proofs.
- A repository needs a periodic pass to remove legacy, migration, transition, or backward-compatibility test coverage that no longer protects an active contract.

## Inputs
- Scoped optimization brief including the slow suites, commands, or harnesses involved
- Current timing evidence such as `--durations`, CI timing output, or repeated local runs
- The active contract the slow tests are supposed to prove
- The documented harness and local path instructions for the affected workspace
- Known transition history, compatibility promises, or deprecation state when trimming tests

## Workflow
1. Establish the optimization boundary and timing baseline.
   - Run the documented harness for the affected slice before editing.
   - Capture the slowest tests, setup hotspots, repeated broad commands, fixture breadth, and duplicate full-repo validation patterns.
   - Keep one baseline command set so the post-change comparison uses the same harness and arguments.
2. Build the hotspot and proof inventory.
   - For each costly test or helper, record the target contract, coverage layer, dependency footprint, and whether another test already proves the same behavior.
   - Distinguish current-product proofs from migration, cutover, transition, deprecated-surface, and backward-compatibility shims.
   - Treat vague historical value as insufficient; identify the live contract that still justifies the cost.
3. Make explicit keep, refactor, or remove decisions.
   - Keep a broad test only when it is the cheapest trustworthy proof of a still-active contract.
   - Refactor when the same contract can be proved faster by narrowing targets, caching fixture baselines, reusing generated state, or moving repeated matrix checks to a lower layer.
   - Replace repeated CLI-envelope coverage with one CLI smoke plus direct service-level or unit coverage when the parser and output envelope are already proven elsewhere.
   - Remove tests that only defend retired migrations, cutovers, transitional scaffolding, or unsupported backward-compatibility promises.
   - Record the reason for every retained expensive test so a later pass does not need to rediscover it.
4. Implement the smallest optimization slice that preserves proof.
   - Prefer reusable fixture builders, focused target sets, and shared helper functions over one-off shortcuts.
   - Keep assertions tied to current behavior rather than incidental internal structure when shrinking integration scope.
   - When deleting a legacy test, confirm another active proof still covers the relevant contract or that the contract itself is retired.
5. Validate behavior and compare runtimes.
   - Rerun the edited file-level tests first, then the same baseline command set captured earlier.
   - Confirm the optimized slice still proves the intended contract, not just that it runs faster.
   - Compare before-and-after timing and note any hotspot that remains expensive on purpose.
6. Close out the optimization pass.
   - Summarize what was trimmed, what was refactored, what stayed expensive, and why.
   - If major hotspots remain, leave the next candidate, blocking reason, and preferred refactor direction explicit for the next periodic pass.

## Data Structure
- Baseline command set and timing sample
- Hotspot inventory with test, helper, or fixture ownership
- Proof map from slow test to active contract
- Keep, refactor, or remove decision register with rationale
- Post-change timing comparison and retained-hotspot list

## Outputs
- Refactored or removed tests, helpers, or fixtures aligned to the active contract
- A before-and-after timing result for the validated slice
- An explicit record of any intentionally retained expensive proofs and their revisit triggers

## Done When
- The slow slice has been narrowed or the retained cost has an explicit current-contract justification.
- Historical, transition-only, or duplicate proofs in scope have been removed or replaced.
- The optimized slice passes the documented harness and the post-change timing has been checked against the baseline.
