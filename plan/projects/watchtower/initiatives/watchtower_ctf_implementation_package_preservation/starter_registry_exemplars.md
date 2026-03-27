# WatchTower CTF Starter Registry Exemplars

## Summary

This support surface turns the preserved registry contract into copy-ready starter shapes for the first `offensive_security/` implementation pass. It adapts the current `plan` and `oversight` posture into offsec-local examples without claiming that the donor registry ids or wording should be copied verbatim.

## How To Use These Exemplars

1. Read `starter_surface_blueprint.md` first for the human-surface intent and required starter roots.
2. Use these JSON excerpts when authoring the first offsec registries in `/home/j/WatchTower`.
3. Keep ids, titles, and clarifying rules offsec-local even when the field shape follows a donor pattern.
4. Update the real registries, matching docs, rendered views, and validators in the same change set.

## `template_catalog.json` Exemplar

Use the donor root-template posture from `plan/.wt/registries/template_catalog.json` and the shared section-order rule from the preserved source contract.

```json
{
  "$schema": "urn:watchtower:schema:artifacts:offensivesecurity:template-catalog:v1",
  "id": "registry.template_catalog",
  "title": "Offensive-Security Template Catalog",
  "status": "active",
  "entries": [
    {
      "template_id": "template.offsec.root.readme",
      "surface_id": "surface.readme.root_navigation",
      "entry_status": "active",
      "authorship_mode": "authored",
      "template_path": "offensive_security/.wt/templates/roots/README.md",
      "required_section_ids": [
        "start_here",
        "workspace_map",
        "notes"
      ],
      "optional_section_ids": [],
      "section_order": [
        "start_here",
        "workspace_map",
        "notes"
      ],
      "allowed_roots": [
        "offensive_security",
        "offensive_security/docs",
        "offensive_security/workflows",
        "offensive_security/tracking",
        "offensive_security/python"
      ],
      "llm_guidance": {
        "authoring_goal": "Create a thin navigation surface for one offsec human root.",
        "hard_requirements": [
          "Keep the file focused on navigation and machine-aware routing.",
          "Do not restate deeper pack contracts when a registry, policy, or query surface already owns them."
        ],
        "advisory_notes": [
          "Prefer one short opening table over prose-heavy introduction.",
          "Use the same root-template posture across the first offsec roots."
        ]
      },
      "llm_guidance_mode": "advisory"
    },
    {
      "template_id": "template.offsec.root.agents",
      "surface_id": "surface.agents.local_instructions",
      "entry_status": "active",
      "authorship_mode": "authored",
      "template_path": "offensive_security/.wt/templates/roots/AGENTS.md",
      "required_section_ids": [
        "role",
        "scope",
        "routing_or_behavior_differences",
        "local_instructions",
        "exclusions_or_constraints"
      ],
      "optional_section_ids": [
        "do",
        "do_not"
      ],
      "section_order": [
        "role",
        "scope",
        "routing_or_behavior_differences",
        "local_instructions",
        "exclusions_or_constraints",
        "do",
        "do_not"
      ],
      "allowed_roots": [
        "offensive_security",
        "offensive_security/workflows",
        "offensive_security/python"
      ]
    }
  ]
}
```

## `documentation_family_registry.json` Exemplar

Use the donor family-registry pattern from `plan/.wt/registries/documentation_family_registry.json` and keep family roots explicit from day one.

```json
{
  "$schema": "urn:watchtower:schema:artifacts:offensivesecurity:documentation-family-registry:v1",
  "id": "registry.documentation_family",
  "title": "Offensive-Security Documentation Family Registry",
  "status": "active",
  "entries": [
    {
      "family_id": "workflow",
      "entry_status": "active",
      "summary": "Pack-owned workflow modules and workflow roles for offsec execution.",
      "allowed_roots": [
        "offensive_security/workflows/modules",
        "offensive_security/workflows/roles"
      ],
      "authorship_mode": "authored",
      "required_index_ids": [
        "index.workflows"
      ],
      "template_ids": [
        "template.offsec.workflow.module"
      ]
    },
    {
      "family_id": "command_doc",
      "entry_status": "active",
      "summary": "Offsec namespace command documentation under the pack-owned command-doc root.",
      "allowed_roots": [
        "offensive_security/docs/commands/core_python"
      ],
      "authorship_mode": "authored",
      "required_index_ids": [
        "index.guidance"
      ],
      "template_ids": [
        "template.offsec.command_doc"
      ]
    },
    {
      "family_id": "standard",
      "entry_status": "active",
      "summary": "Pack-owned standards for operations, evidence, and knowledge behavior.",
      "allowed_roots": [
        "offensive_security/docs/standards"
      ],
      "authorship_mode": "authored",
      "required_index_ids": [
        "index.guidance"
      ],
      "template_ids": [
        "template.offsec.guidance.standard"
      ]
    }
  ]
}
```

## `human_surface_policy_registry.json` Exemplar

Use the donor shape from `plan/.wt/registries/human_surface_policy_registry.json` and `/home/j/WatchTowerOversight/oversight/.wt/registries/human_surface_policy_registry.json`.

```json
{
  "$schema": "urn:watchtower:schema:artifacts:offensivesecurity:human-surface-policy-registry:v1",
  "id": "registry.human_surface_policy",
  "title": "Offensive-Security Human Surface Policy Registry",
  "status": "active",
  "entries": [
    {
      "policy_id": "policy.human_surface.offsec_root",
      "path_pattern": "offensive_security",
      "match_mode": "exact",
      "root_kind": "domain_root",
      "entry_status": "active",
      "governing_surfaces": [
        "human_surface_policy_registry",
        "rendered_surface_registry"
      ],
      "clarifying_rule": "The pack root is the main offsec start-here surface and routes readers into tracking, docs, workflows, and python roots.",
      "surfaces": [
        {
          "relative_path": "README.md",
          "entity_shape": "file",
          "surface_role": "readme",
          "mode": "required",
          "authorship_mode": "authored"
        },
        {
          "relative_path": "AGENTS.md",
          "entity_shape": "file",
          "surface_role": "agents",
          "mode": "required",
          "authorship_mode": "authored"
        },
        {
          "relative_path": "offensivesecurity_overview.md",
          "entity_shape": "file",
          "surface_role": "rendered_visibility",
          "mode": "required",
          "authorship_mode": "rendered"
        }
      ]
    },
    {
      "policy_id": "policy.human_surface.offsec_workflows_root",
      "path_pattern": "offensive_security/workflows",
      "match_mode": "exact",
      "root_kind": "workflow_root",
      "entry_status": "active",
      "governing_surfaces": [
        "human_surface_policy_registry",
        "workflow_metadata_registry"
      ],
      "clarifying_rule": "The workflows root is the local routing and module entrypoint for offsec behavior.",
      "surfaces": [
        {
          "relative_path": "README.md",
          "entity_shape": "file",
          "surface_role": "readme",
          "mode": "required",
          "authorship_mode": "authored"
        },
        {
          "relative_path": "AGENTS.md",
          "entity_shape": "file",
          "surface_role": "agents",
          "mode": "required",
          "authorship_mode": "authored"
        },
        {
          "relative_path": "ROUTING_TABLE.md",
          "entity_shape": "file",
          "surface_role": "routing_table",
          "mode": "required",
          "authorship_mode": "authored"
        },
        {
          "relative_path": "modules/README.md",
          "entity_shape": "file",
          "surface_role": "workflow_modules_router",
          "mode": "required",
          "authorship_mode": "authored"
        }
      ]
    }
  ]
}
```

## `rendered_surface_registry.json` Exemplar

Keep rendered visibility named and registry-backed from day one, matching the donor rendered-surface posture.

```json
{
  "$schema": "urn:watchtower:schema:artifacts:offensivesecurity:rendered-surface-registry:v1",
  "id": "registry.rendered_surface",
  "title": "Offensive-Security Rendered Surface Registry",
  "status": "active",
  "surfaces": [
    {
      "surface_id": "surface.offsec.overview",
      "entry_status": "active",
      "rendered_path": "offensive_security/offensivesecurity_overview.md",
      "surface_role": "overview",
      "source_artifact_paths": [
        "offensive_security/.wt/indexes/challenge_index.json",
        "offensive_security/.wt/indexes/blocker_index.json",
        "offensive_security/.wt/indexes/session_index.json"
      ]
    },
    {
      "surface_id": "surface.offsec.challenge_tracking",
      "entry_status": "active",
      "rendered_path": "offensive_security/tracking/challenge_tracking.md",
      "surface_role": "rendered_tracker",
      "source_artifact_paths": [
        "offensive_security/.wt/indexes/challenge_index.json"
      ]
    }
  ]
}
```

## `authority_map.json` Exemplar

Keep the question-driven lookup posture from the preserved authority-map contract.

```json
{
  "$schema": "urn:watchtower:schema:artifacts:registries:authority-map:v1",
  "id": "registry.authority_map",
  "title": "Offensive-Security Authority Map",
  "status": "active",
  "entries": [
    {
      "question_id": "authority.offsec.current_state",
      "domain": "planning",
      "question": "What is the current offensive-security pack state and next action?",
      "artifact_kind": "challenge_index",
      "canonical_path": "offensive_security/.wt/indexes/challenge_index.json",
      "preferred_command": "watchtower-core offsec query status",
      "preferred_human_path": "offensive_security/offensivesecurity_overview.md",
      "fallback_paths": [
        "offensive_security/tracking/challenge_tracking.md",
        "offensive_security/tracking/blocker_tracking.md"
      ]
    },
    {
      "question_id": "authority.offsec.challenge_lookup",
      "domain": "planning",
      "question": "Which challenges exist and what state is each challenge in?",
      "artifact_kind": "challenge_index",
      "canonical_path": "offensive_security/.wt/indexes/challenge_index.json",
      "preferred_command": "watchtower-core offsec query challenges",
      "preferred_human_path": "offensive_security/tracking/challenge_tracking.md",
      "fallback_paths": [
        "offensive_security/offensivesecurity_overview.md",
        "offensive_security/.wt/indexes/artifact_index.json",
        "offensive_security/ctf/"
      ]
    }
  ]
}
```

## Cross-Registry Checks

- Every `template_id` referenced from `documentation_family_registry.json` must exist in `template_catalog.json`.
- Every rendered surface required by `human_surface_policy_registry.json` must exist in `rendered_surface_registry.json`.
- Every root named in `starter_surface_blueprint.md` must also be governed by `human_surface_policy_registry.json`.
- `authority_map.json` must point to implemented commands and real rendered surfaces, not placeholders.
- Use these exemplars to remove guesswork, then tighten the actual registry content against the real offsec implementation state.
