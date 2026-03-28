# `core/docs/standards/governance`

## Description
`This directory contains shared governance standards for source hierarchy, citation discipline, and promotion of external guidance into durable repository policy. Use it when the main question is how to separate observed authority from local interpretation, or how outside material should become stable local guidance.`

## Files
| Path | Description |
|---|---|
| `core/docs/standards/governance/README.md` | Describes the purpose of the shared governance-standards family. |
| `core/docs/standards/governance/reference_distillation_standard.md` | Defines how external source material is distilled into durable local references and, when needed, promoted into repository policy. |
| `core/docs/standards/governance/source_and_citation_standard.md` | Defines shared authority order, citation discipline, and fact-versus-inference labeling expectations. |

## Notes
- Use `cd core/python && ./.venv/bin/watchtower-core query standards --category governance --format json` when you need the machine-readable governance-standards lookup surface.
- Use `cd core/python && ./.venv/bin/watchtower-core query authority --query canonical --format json` when the first question is which governed surface is authoritative.
