# Adversarial Lens Workflow

## Purpose
Use this workflow to apply a contradiction-oriented, false-green-resistant overlay to the active review, validation, implementation, optimization, or remediation route without replacing that base task family.

## Use When
- The request explicitly asks for an adversarial, contradiction-oriented, false-green, or challenge-style pass.
- The active route should keep a stronger proof posture while it reviews, benchmarks, refactors, optimizes, or fixes findings.
- A remediation loop must preserve the originating adversarial bar instead of silently downgrading to the default fix posture.

## Inputs
- The active routed task type and workflow stack
- The scoped adversarial request or modifier from the starting prompt
- The governing standards, docs, commands, validators, and machine-readable authority that make claims worth challenging
- The current findings set, rerun-ready prompt, or prompt-equivalent when a remediation loop is in scope

## Workflow
1. Confirm the base task family before applying the lens.
   - Keep the dominant routed review, validation, implementation, optimization, or remediation route explicit.
   - Treat the adversarial lens as an overlay on that route, not as a replacement for the base task family unless the request explicitly selected the dedicated adversarial repository-review route.
2. Raise the proof bar for the active route.
   - Treat passing tests, validators, benchmark baselines, coherent docs, or plausible refactors as evidence, not as conclusion.
   - Identify the concrete claims the active route would otherwise accept on trust and turn them into contradiction checks.
3. Challenge the highest-risk claims directly.
   - Prefer the narrowest disposable challenge that can prove whether the claimed protection fails closed.
   - Re-check important claims from more than one angle, including human-readable docs, machine-readable authority, live command behavior, validator coverage, representative workflows, and post-fix reality.
4. Preserve adversarial continuity through fixes and reruns.
   - Keep the starting adversarial prompt or the narrowest rerun-safe prompt-equivalent available for later remediation loops.
   - Do not let findings remediation, optimization work, or benchmark updates silently relax the proof posture that produced the original findings set.
5. Record what the lens changed.
   - Distinguish base-route work from adversarial-only challenge work so later contributors can tell why the task cost more and what extra proof it produced.

## Data Structure
- Active base-route identifier and overlay decision record
- Contradiction map for the claims under challenge
- Proof matrix tying each challenged claim to the checks that exercised it
- Rerun-ready prompt record for downstream remediation loops

## Outputs
- A clear adversarial overlay decision bound to the active route
- Stronger-than-default challenge evidence for the claims that mattered
- A rerun-ready prompt or explicit recovery limitation when later fixes must preserve the same adversarial posture

## Done When
- The active route is still recognizable, and the adversarial lens strengthened it instead of replacing it accidentally.
- The strongest contradiction-prone claims were challenged from enough angles that the result is not a green-path assumption.
- A later remediation or rerun can preserve the same adversarial posture without reconstructing it from memory.
