# Evidence, Provenance, And Audit Standard

## Purpose

Define the minimum evidence, provenance, and audit posture for challenge execution, closeout, and reusable knowledge extraction.

## Rules

- event streams are append-only audit surfaces;
- current-state provenance may also live on affected artifacts and derived surfaces;
- evidence capture must distinguish raw supporting artifacts from summarized notes and promoted knowledge;
- raw supporting captures live under `artifacts/`, while the authoritative governed evidence inventory lives in `.wt_local/evidence/artifacts.json`;
- command capture must cover both proposed and executed user or agent commands, with timestamps, actor, command summary, and execution metadata when present;
- command history shown in `notes.md`, event streams, query output, and rendered views must stay compact and must not become a raw terminal transcript dump;
- raw or large stdout or stderr should live in artifact captures with governed evidence metadata and artifact refs rather than being embedded inline in routine notes or machine indexes;
- redact clearly player-owned material from routine machine-visible surfaces, including operator credentials, personal tokens, cookies, API keys, SSH keys, workstation-local secrets, and personal account identifiers;
- challenge-issued ephemeral values may remain in governed evidence or routine summaries when operationally useful, but bulk or raw output still belongs in captured artifacts rather than inline notes or indexes;
- governed JSON artifacts carry `contract_version`, UTC whole-second timestamps, pack-relative POSIX paths, and structured checksums where checksums are present;
- closeout always emits a structured extraction output, even when no reusable knowledge is promoted;
- airgapped workflows require explicit provenance notes for manually transferred inputs and outputs;
- closeout, evidence, and extraction records must expose enough metadata to trace claims, command links, event links, transfer provenance, and review posture without relying on nearby notes context;
- scripts and executables produced during challenge work stay under `artifact_kind = file_capture` with typed payload roles such as `generated_script`, `generated_binary`, or `downloaded_binary`;
- discrepancy records may impose governance limits that validators and workflow gates can enforce.

## Acceptance

- artifact handling, evidence capture, and audit expectations are explicit for local, remote, and airgapped workflows;
- the package never treats evidence provenance as optional narrative-only metadata.
