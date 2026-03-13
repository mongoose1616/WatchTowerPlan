from __future__ import annotations

import re

from tests.integration.control_plane_artifact_helpers import FRONT_MATTER_PATTERN, REPO_ROOT
from watchtower_core.adapters import extract_sections
from watchtower_core.repo_ops.standards import parse_standard_operationalization


def test_governed_standards_and_planning_docs_publish_references_sections() -> None:
    governed_families = [
        (
            REPO_ROOT / "docs/standards",
            {"README.md"},
        ),
        (
            REPO_ROOT / "docs/planning/design/features",
            {"README.md"},
        ),
        (
            REPO_ROOT / "docs/planning/design/implementation",
            {"README.md"},
        ),
        (
            REPO_ROOT / "docs/planning/prds",
            {"README.md", "prd_tracking.md"},
        ),
        (
            REPO_ROOT / "docs/planning/decisions",
            {"README.md", "decision_tracking.md"},
        ),
        (
            REPO_ROOT / "docs/foundations",
            {"README.md"},
        ),
    ]

    for directory, excluded_names in governed_families:
        for path in sorted(directory.rglob("*.md")):
            if path.name in excluded_names:
                continue
            body = FRONT_MATTER_PATTERN.sub("", path.read_text(encoding="utf-8"), count=1)
            assert "## References" in body, f"missing References section: {path}"


def test_governed_standards_explain_related_sources() -> None:
    for path in sorted((REPO_ROOT / "docs/standards").rglob("*.md")):
        if path.name == "README.md":
            continue
        markdown = FRONT_MATTER_PATTERN.sub("", path.read_text(encoding="utf-8"), count=1)
        sections = {
            title.strip(): body
            for title, body in re.findall(
                r"^## (.+?)\n(.*?)(?=^## |\Z)",
                markdown,
                flags=re.MULTILINE | re.DOTALL,
            )
        }
        section = sections.get("Related Standards and Sources")
        assert section is not None, f"missing Related Standards and Sources section: {path}"
        bullets = [line.strip() for line in section.splitlines() if line.strip().startswith("- ")]
        assert bullets, f"missing related-source bullets: {path}"
        assert all(": " in bullet for bullet in bullets), (
            f"unexplained related-source bullet: {path}"
        )


def test_reference_authoring_surfaces_stay_aligned_with_governed_contract() -> None:
    standard_markdown = (
        REPO_ROOT / "docs/standards/documentation/reference_md_standard.md"
    ).read_text(encoding="utf-8")
    template_markdown = (REPO_ROOT / "docs/templates/reference_template.md").read_text(
        encoding="utf-8"
    )

    assert "`Canonical Upstream`" in standard_markdown
    assert "| `Canonical Upstream` |" not in standard_markdown
    assert "must include\n  `Canonical Upstream`" in standard_markdown or (
        "must include `Canonical Upstream`" in standard_markdown
    )
    assert "## Canonical Upstream" in template_markdown, (
        "reference template must include Canonical Upstream"
    )
    assert "does not belong in the governed `docs/references/**` family" in template_markdown


def test_standard_document_template_stays_aligned_with_governed_contract() -> None:
    path = REPO_ROOT / "docs/templates/standard_document_template.md"
    markdown = path.read_text(encoding="utf-8")

    required_sections = (
        "Summary",
        "Purpose",
        "Scope",
        "Use When",
        "Related Standards and Sources",
        "Guidance",
        "Operationalization",
        "Validation",
        "Change Control",
        "References",
        "Updated At",
    )
    for title in required_sections:
        assert f"## {title}" in markdown, f"missing required standard-template section: {title}"

    related_section_match = re.search(
        r"^## Related Standards and Sources\n(.*?)(?=^## |\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert related_section_match is not None, "missing Related Standards and Sources section"
    related_bullets = [
        line.strip()
        for line in related_section_match.group(1).splitlines()
        if line.strip().startswith("- ")
    ]
    assert related_bullets, "missing related-source bullets in standard template"
    assert all(": " in bullet for bullet in related_bullets), (
        "standard template related-source bullets must use source: implication form"
    )

    operationalization_section_match = re.search(
        r"^## Operationalization\n(.*?)(?=^## |\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert operationalization_section_match is not None, "missing Operationalization section"
    operationalization_section = operationalization_section_match.group(1)
    assert "- `Modes`:" in operationalization_section
    assert "- `Operational Surfaces`:" in operationalization_section
    assert "directory paths ending in `/`" in markdown

    optional_sections_match = re.search(
        r"^## Optional Sections\n(.*?)(?=^## |\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert optional_sections_match is not None, "missing Optional Sections guidance"
    optional_sections = optional_sections_match.group(1)
    for title in required_sections:
        assert f"`{title}`" not in optional_sections, (
            f"required standard-template section incorrectly listed as optional: {title}"
        )


def test_generic_documentation_template_stays_narrowed_to_fallback_guidance() -> None:
    template_markdown = (REPO_ROOT / "docs/templates/documentation_template.md").read_text(
        encoding="utf-8"
    )
    templates_readme = (REPO_ROOT / "docs/templates/README.md").read_text(encoding="utf-8")

    assert "Use this template only when no narrower family-specific template applies." in (
        template_markdown
    )
    assert (
        "Use this template for standards, guides, design docs, reference docs"
        not in template_markdown
    ), "generic documentation template must not advertise governed family docs"
    assert (
        "fallback template for repository docs without a narrower family-specific"
        in templates_readme.casefold()
    )


def test_document_family_standards_publish_precise_operationalization_coverage() -> None:
    cases = (
        (
            REPO_ROOT / "docs/standards/documentation/agents_md_standard.md",
            ("`AGENTS.md`", "`**/AGENTS.md`"),
        ),
        (
            REPO_ROOT / "docs/standards/documentation/readme_md_standard.md",
            ("`README.md`", "`**/README.md`"),
        ),
        (
            REPO_ROOT / "docs/standards/documentation/reference_md_standard.md",
            ("`docs/references/*_reference.md`",),
        ),
        (
            REPO_ROOT / "docs/standards/documentation/standard_md_standard.md",
            ("`docs/standards/*/*_standard.md`",),
        ),
    )

    for path, expected_values in cases:
        markdown = path.read_text(encoding="utf-8")
        operationalization_match = re.search(
            r"^## Operationalization\n(.*?)(?=^## |\Z)",
            markdown,
            flags=re.MULTILINE | re.DOTALL,
        )
        assert operationalization_match is not None, f"missing Operationalization section: {path}"
        operationalization_section = operationalization_match.group(1)
        for value in expected_values:
            assert value in operationalization_section, (
                f"missing operationalization surface {value} in {path}"
            )


def test_data_contract_standards_publish_family_example_operationalization_coverage() -> None:
    cases = (
        (
            REPO_ROOT / "docs/standards/data_contracts/acceptance_contract_standard.md",
            (
                "`core/control_plane/examples/valid/contracts/acceptance_contract*.example.json`",
                "`core/control_plane/examples/invalid/contracts/acceptance_contract*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/authority_map_standard.md",
            (
                "`core/control_plane/examples/valid/registries/authority_map*.example.json`",
                "`core/control_plane/examples/invalid/registries/authority_map*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/command_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/command_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/command_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/coordination_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/coordination_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/coordination_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/decision_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/decision_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/decision_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/design_document_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/design_document_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/design_document_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/foundation_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/foundation_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/foundation_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/initiative_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/initiative_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/initiative_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/planning_catalog_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/planning_catalog*.example.json`",
                "`core/control_plane/examples/invalid/indexes/planning_catalog*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/prd_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/prd_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/prd_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/reference_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/reference_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/reference_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/repository_path_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/repository_path_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/repository_path_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/route_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/route_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/route_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/schema_catalog_standard.md",
            (
                "`core/control_plane/examples/valid/registries/schema_catalog*.example.json`",
                "`core/control_plane/examples/invalid/registries/schema_catalog*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/standard_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/standard_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/standard_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/task_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/task_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/task_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/traceability_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/traceability_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/traceability_index*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/validation_evidence_standard.md",
            (
                "`core/control_plane/examples/valid/ledgers/validation_evidence*.example.json`",
                "`core/control_plane/examples/invalid/ledgers/validation_evidence*.example.json`",
            ),
        ),
        (
            REPO_ROOT / "docs/standards/data_contracts/workflow_index_standard.md",
            (
                "`core/control_plane/examples/valid/indexes/workflow_index*.example.json`",
                "`core/control_plane/examples/invalid/indexes/workflow_index*.example.json`",
            ),
        ),
    )

    for path, expected_values in cases:
        markdown = path.read_text(encoding="utf-8")
        operationalization_match = re.search(
            r"^## Operationalization\n(.*?)(?=^## |\Z)",
            markdown,
            flags=re.MULTILINE | re.DOTALL,
        )
        assert operationalization_match is not None, f"missing Operationalization section: {path}"
        operationalization_section = operationalization_match.group(1)
        for value in expected_values:
            assert value in operationalization_section, (
                f"missing operationalization surface {value} in {path}"
            )


def test_live_standard_operationalization_paths_are_canonical() -> None:
    for path in sorted((REPO_ROOT / "docs/standards").rglob("*_standard.md")):
        relative_path = path.relative_to(REPO_ROOT).as_posix()
        markdown = FRONT_MATTER_PATTERN.sub("", path.read_text(encoding="utf-8"), count=1)
        sections = extract_sections(markdown)
        _, operationalization_paths = parse_standard_operationalization(
            relative_path,
            sections.get("Operationalization"),
            REPO_ROOT,
        )

        canonical_forms = {value.casefold().rstrip("/") for value in operationalization_paths}
        assert len(canonical_forms) == len(operationalization_paths), (
            f"semantically duplicate operationalization paths published in {relative_path}"
        )

        for value in operationalization_paths:
            if any(token in value for token in "*?["):
                continue
            candidate = REPO_ROOT / value.rstrip("/")
            if candidate.is_dir():
                assert value.endswith("/"), (
                    "directory operationalization path must end with '/': "
                    f"{relative_path} -> {value}"
                )
            else:
                assert not value.endswith("/"), (
                    "file operationalization path must not end with '/': "
                    f"{relative_path} -> {value}"
                )


def test_readme_template_stays_aligned_with_governed_contract() -> None:
    markdown = (REPO_ROOT / "docs/templates/readme_template.md").read_text(encoding="utf-8")

    assert markdown.startswith("# `<repo-relative-directory-path>`\n")
    assert "> Use `# \\`.\\`` when the template is instantiated at the repository root." in (
        markdown
    )
    assert "<Directory Name>" not in markdown
    assert "<current-directory>/README.md" not in markdown
    assert "<repo-relative-path-to-this-readme>" in markdown
    assert markdown.index("## Files") < markdown.index("## Boundaries")
    assert markdown.index("## Files") < markdown.index("## Notes")
