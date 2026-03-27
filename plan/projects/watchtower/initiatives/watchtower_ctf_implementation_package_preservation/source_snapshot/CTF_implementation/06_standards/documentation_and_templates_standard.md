# Documentation And Templates Standard

## Purpose

Define the minimum human-facing document structure for challenge work, closeout, reusable knowledge, and pack-owned operator docs.

## Rules

- `challenge.md` preserves exact source challenge text in its body.
- `challenge.md` front matter is required, but the front matter may be generated at the next workflow opportunity instead of being forced synchronously at intake.
- `notes.md` is the active working surface and must remain directly editable.
- `notes.md` uses one canonical structure with optional sections and mode-specific rendering overlays rather than multiple unrelated base templates.
- `notes.md` must surface high-level context first, then guidance-critical summaries, then phased work, then durable sequential logs.
- agent edits to `notes.md` must be append-preserving and non-destructive to user-authored prose.
- user-created ad hoc sections are allowed during active work and are normalized or flagged only before closeout.
- `solution/` is the challenge-specific reproducibility surface.
- `solution/` is required when `closeout_record.outcome = solved` and must not be fabricated for `blocked_closeout`, `unresolved`, or `closed_without_attempt` outcomes.
- `solution/` content must stay procedure-first and reproducible, with commands, inputs, outputs, and verification steps where safe.
- `recap.md` is the governed retrospective closeout surface and must capture learning, pivots, and reusable lessons.
- `recap.md` is required for `solved`, `blocked_closeout`, and `unresolved` outcomes, even if guided and full-auto modes draft it differently; `closed_without_attempt` may omit it.
- every closeout must also produce a structured extraction artifact, including explicit no-candidate results.
- reusable knowledge families use strict family-specific templates with shared metadata discipline.
- visible machine-managed metadata should expose state and provenance, but the amount of surfaced metadata may vary by artifact family.
- front matter and hidden machine state must reconcile predictably, with governed hidden records winning on machine-authoritative fields and markdown remaining the operator-facing mirror.
- pack-owned command docs stay under the offensive-security docs root, not shared core docs.
- rendered views are derived and must not silently replace authoritative pack artifacts.

## Locked V1 Minimum Sections

- `challenge.md` required sections: `Source`, `Objective`, `Constraints`, `Environment`
- `notes.md` required sections: `Working Summary`, `Hypotheses`, `Commands`, `Evidence`, `Blockers`, `Next Steps`
- `recap.md` required sections: `Outcome`, `Path`, `Failures`, `Reusable Lessons`
- optional sections, mode-specific overlays, and rendered summaries may extend these baselines, but they must not replace them

## Acceptance

- every human-facing artifact family has an explicit template owner and validation path;
- direct-edit reconciliation rules are explicit wherever markdown is user-editable.
