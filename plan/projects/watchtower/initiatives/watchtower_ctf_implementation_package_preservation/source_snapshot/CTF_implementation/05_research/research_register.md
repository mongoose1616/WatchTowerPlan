# Research Register

| Research ID | Title | URL | Authority Level | Accessed On | Why It Matters | Package Use |
|---|---|---|---|---|---|---|
| `research.attack.enterprise_tactics` | MITRE ATT&CK Enterprise Tactics | `https://attack.mitre.org/tactics/enterprise/` | `primary` | `2026-03-25` | tactic taxonomy and version-pinned offensive-security knowledge alignment; cite as ATT&CK v18 where used | knowledge taxonomy and promotion standard |
| `research.attack.updates` | ATT&CK Updates | `https://attack.mitre.org/resources/updates/` | `primary` | `2026-03-25` | live ATT&CK version changes, including the October 28, 2025 v18 release that introduced the asset-centric defensive model and deprecated older detection-centric surfaces | research notes and version-pin policy |
| `research.owasp.wstg` | OWASP Web Security Testing Guide | `https://owasp.org/www-project-web-security-testing-guide/` | `canonical_community` | `2026-03-25` | practical offensive-security workflow coverage and versioned testing taxonomy; cite pinned WSTG v4.2 sections instead of floating links | workflow and operator guidance |
| `research.nist.800_115` | NIST SP 800-115, Technical Guide to Information Security Testing and Assessment | `https://csrc.nist.gov/pubs/sp/800/115/final` | `primary` | `2026-03-25` | testing engagement structure, planning, execution, and reporting expectations | operator workflow guide and safety standard |
| `research.nist.800_86` | NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response | `https://csrc.nist.gov/pubs/sp/800/86/final` | `primary` | `2026-03-25` | evidence capture, forensic handling, and documentation discipline | evidence/provenance/audit standard |
| `research.nist.800_92r1_ipd` | NIST SP 800-92 Rev.1 IPD, Guide to Security Log Management | `https://csrc.nist.gov/pubs/sp/800/92/r1/ipd` | `informative_draft` | `2026-03-25` | modernized logging and event management guidance | event stream and audit planning |
| `research.diataxis` | Diátaxis | `https://diataxis.fr/` | `informative` | `2026-03-25` | separation of tutorial/how-to/reference/explanation doc types | guide and reference structure decisions |

## Citation Rules

- pin ATT&CK references by version and date when cited in package docs;
- pin ATT&CK references as v18 plus access date unless a later reviewed version is intentionally adopted;
- pin OWASP references to explicit WSTG release material such as v4.2 section URLs or repository tags;
- avoid `stable` or `latest` OWASP links inside the package;
- mark draft or informative sources explicitly and never treat them as higher authority than current repo contract or primary sources.
