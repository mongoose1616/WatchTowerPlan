# WatchTower CTF Promotion And Extraction Map

## Summary

This support surface maps challenge closeout outputs to extraction candidates, review gates, and promoted reusable knowledge. Its purpose is to make Phase 5 implementation concrete before the first real promotion pass exists.

## Pipeline

1. A challenge reaches closeout with governed `challenge.md`, `notes.md`, `closeout_record`, evidence inventory, and recap or solution material.
2. `extraction_output` is created under `.wt_local/extractions/` and records candidate families, source coverage, and review posture.
3. Candidate artifacts are represented with stable ids and provenance back to the closed challenge.
4. The required review workflow gates promotion according to `promotion_policy_registry.json`.
5. Accepted artifacts land in the reusable knowledge root and appear in `knowledge_index.json`.
6. Candidate artifacts remain visible only when the operator explicitly asks for them.

## Required Provenance For Promotion

Every promoted reusable-knowledge artifact keeps:

- `challenge_id`
- `closeout_id`
- `extraction_id`
- `source_artifact_refs`
- `evidence_refs`

Those fields are mandatory even when a candidate becomes highly reusable, because offsec promotion does not sever provenance.

## Source-To-Candidate Map

| Source Surface | What To Extract | Candidate Family Targets | Strip Or Quarantine Before Promotion | Review / Promotion Notes |
|---|---|---|---|---|
| `notes.md` | concrete commands, protocol cues, tool behavior, blocker patterns, tactic hints | `command_pattern`, `tool_profile`, `protocol`, `tactic` | challenge-only hostnames, flags, credentials, ephemeral timestamps, challenge prompt text copied verbatim | treat `notes.md` as high-value raw source but not directly reusable without review |
| `recap.md` | concise approach, pivot summary, reusable lesson | `tactic`, `playbook`, `reference` | challenge-only identifiers and non-generalized solution trivia | good source for clean reusable summaries once challenge-specific detail is stripped |
| `solution/` | solved workflow, exact command sequence, tool usage | `playbook`, `command_pattern`, `tool_profile`, `protocol` | challenge-secret material, puzzle-specific filenames, transient environment details | stronger review gate because it often contains overfit or too-specific execution detail |
| evidence artifacts | command proofs, packet captures, screenshots, file captures | evidence refs for other candidates, sometimes `reference` support | raw sensitive data, pasted secrets, irrelevant challenge-local noise | evidence usually supports promotion rather than becoming accepted knowledge by itself |
| `closeout_record.json` | outcome, pivot, completeness, review cues | usually provenance only, not a promoted family | none; keep as provenance context | use as promotion context, not as reusable knowledge payload |
| `challenge_metadata.json` | provenance, source context, path identity | provenance only, not a promoted family | none; keep compact | never promote directly as reusable knowledge |

## Family-Specific Promotion Guidance

### `command_pattern`

- Best source inputs: `notes.md`, `solution/`, command-output evidence.
- Promote only when the command is generalized enough to be useful outside the original challenge.
- Keep exact challenge-only parameters out of the accepted artifact unless they are clearly marked as placeholders.

### `tool_profile`

- Best source inputs: `notes.md`, `solution/`, `recap.md`.
- Promote when the challenge proves stable tool behavior, options, tradeoffs, or constraints that apply more broadly.
- Keep tool behavior separate from one-off command transcripts.

### `protocol`

- Best source inputs: `notes.md`, evidence artifacts, `solution/`.
- Promote when protocol-level behavior or observations matter beyond the specific challenge.
- Keep wire-level evidence as provenance rather than bloating the accepted artifact.

### `tactic`

- Best source inputs: `recap.md`, distilled notes, repeated blocker or pivot patterns.
- Promote when the extracted lesson is conceptual and reusable across targets.
- Keep tactics above tool-specific detail in the conceptual ladder.

### `playbook`

- Best source inputs: `solution/`, `recap.md`, distilled notes.
- Promote when the workflow is reusable and belongs under a tactic.
- Keep playbooks nested under tactics rather than collapsing them into tactic prose.

### `reference`

- Best source inputs: curated citations added during closeout and any high-quality supporting material discovered along the way.
- Promote when the reference materially supports future work and is worth preserving in the knowledge corpus.
- Keep `reference_kind` and reusable citation metadata explicit.

## Candidate-To-Accepted Flow

| Stage | Artifact Posture | Expected Record |
|---|---|---|
| extraction created | candidate set assembled | `extraction_output` with `candidate_refs` and `families_found` |
| review requested | candidate ready for governed review | review workflow event plus candidate review state |
| accepted | reusable artifact published | promoted knowledge artifact plus `knowledge_index` row |
| rejected | candidate retained only as historical extraction outcome | candidate remains in extraction history and does not appear in default retrieval |
| superseded | older extraction or candidate replaced by newer outcome | `superseded` extraction or candidate lineage remains explicit |

## Do Not Promote Directly

- `challenge.md` body prose as reusable knowledge by itself
- raw `closeout_record.json`
- unresolved discrepancy content
- challenge-only secrets or puzzle answers
- malformed or partial pasted material that has not been manually verified or reproduced
