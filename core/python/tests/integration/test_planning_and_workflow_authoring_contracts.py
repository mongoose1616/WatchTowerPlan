from __future__ import annotations

import re

from tests.integration.control_plane_artifact_helpers import FRONT_MATTER_PATTERN, REPO_ROOT


def test_governed_design_docs_explain_applied_reference_implications() -> None:
    governed_sections = [
        (
            REPO_ROOT / "docs/planning/design/features",
            {"README.md"},
            (
                "## Foundations References Applied",
                "## Internal Standards and Canonical References Applied",
            ),
        ),
        (
            REPO_ROOT / "docs/planning/design/implementation",
            {"README.md"},
            ("## Internal Standards and Canonical References Applied",),
        ),
    ]

    for directory, excluded_names, section_headings in governed_sections:
        for path in sorted(directory.rglob("*.md")):
            if path.name in excluded_names:
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
            for heading in section_headings:
                title = heading.removeprefix("## ").strip()
                section = sections.get(title)
                assert section is not None, f"missing applied-reference section {title}: {path}"
                bullets = [
                    line.strip()
                    for line in section.splitlines()
                    if line.strip().startswith("- ")
                ]
                assert bullets, f"missing applied-reference bullets in {title}: {path}"
                assert all(": " in bullet for bullet in bullets), (
                    f"unexplained applied-reference bullet in {title}: {path}"
                )


def test_decision_record_authoring_surfaces_stay_aligned_with_governed_contract() -> None:
    standard_path = REPO_ROOT / "docs/standards/documentation/decision_record_md_standard.md"
    standard_markdown = standard_path.read_text(encoding="utf-8")
    template_path = REPO_ROOT / "docs/templates/decision_record_template.md"
    template_markdown = template_path.read_text(encoding="utf-8")

    assert (
        "| `Applied References and Implications` | Required |" in standard_markdown
    ), "decision-record standard must require Applied References and Implications"
    assert (
        "| `Applied References and Implications` | A cited authority materially shaped"
        not in standard_markdown
    ), "decision-record standard must not list Applied References and Implications as optional"
    assert "## Applied References and Implications" in template_markdown, (
        "decision-record template must include Applied References and Implications"
    )

    optional_sections_match = re.search(
        r"^## Optional Sections\n(.*?)(?=^## |\Z)",
        template_markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert optional_sections_match is not None, "missing decision-template optional sections"
    assert (
        "`Applied References and Implications`" not in optional_sections_match.group(1)
    ), "decision-record template must not list Applied References and Implications as optional"


def test_design_authoring_surfaces_stay_aligned_with_governed_contracts() -> None:
    feature_standard = (
        REPO_ROOT / "docs/standards/documentation/feature_design_md_standard.md"
    ).read_text(encoding="utf-8")
    feature_template = (REPO_ROOT / "docs/templates/feature_design_template.md").read_text(
        encoding="utf-8"
    )
    implementation_standard = (
        REPO_ROOT / "docs/standards/documentation/implementation_plan_md_standard.md"
    ).read_text(encoding="utf-8")
    implementation_template = (
        REPO_ROOT / "docs/templates/implementation_plan_template.md"
    ).read_text(encoding="utf-8")

    for title in (
        "Foundations References Applied",
        "Internal Standards and Canonical References Applied",
    ):
        assert f"| `{title}` | Required |" in feature_standard, (
            f"feature-design standard must require {title}"
        )
        assert f"## {title}" in feature_template, f"feature-design template must include {title}"

    feature_optional_match = re.search(
        r"^## Optional Sections\n(.*?)(?=^## |\Z)",
        feature_template,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert feature_optional_match is not None, "missing feature-design optional sections"
    for title in (
        "Foundations References Applied",
        "Internal Standards and Canonical References Applied",
    ):
        assert f"`{title}`" not in feature_optional_match.group(1), (
            f"feature-design template must not list {title} as optional"
        )

    title = "Internal Standards and Canonical References Applied"
    assert f"| `{title}` | Required |" in implementation_standard, (
        "implementation-plan standard must require applied internal references"
    )
    assert f"## {title}" in implementation_template, (
        "implementation-plan template must include applied internal references"
    )
    implementation_optional_match = re.search(
        r"^## Optional Sections\n(.*?)(?=^## |\Z)",
        implementation_template,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert implementation_optional_match is not None, (
        "missing implementation-plan optional sections"
    )
    assert f"`{title}`" not in implementation_optional_match.group(1), (
        "implementation-plan template must not list applied internal references as optional"
    )


def test_governed_decision_docs_explain_applied_references() -> None:
    for path in sorted((REPO_ROOT / "docs/planning/decisions").rglob("*.md")):
        if path.name in {"README.md", "decision_tracking.md"}:
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
        section = sections.get("Applied References and Implications")
        assert section is not None, f"missing Applied References and Implications section: {path}"
        bullets = [line.strip() for line in section.splitlines() if line.strip().startswith("- ")]
        assert bullets, f"missing applied-reference bullets: {path}"
        assert all(": " in bullet for bullet in bullets), (
            f"unexplained applied-reference bullet: {path}"
        )


def test_workflow_modules_publish_task_specific_additional_load_files() -> None:
    for path in sorted((REPO_ROOT / "workflows/modules").glob("*.md")):
        if path.name == "README.md":
            continue
        markdown = path.read_text(encoding="utf-8")
        sections = {
            title.strip(): body
            for title, body in re.findall(
                r"^## (.+?)\n(.*?)(?=^## |\Z)",
                markdown,
                flags=re.MULTILINE | re.DOTALL,
            )
        }
        section = sections.get("Additional Files to Load")
        if section is None:
            continue
        bullets = [line.strip() for line in section.splitlines() if line.strip().startswith("- ")]
        assert bullets, f"missing workflow additional-load bullets: {path}"
        assert len(bullets) <= 5, f"too many workflow additional-load bullets: {path}"
        assert all(": " in bullet for bullet in bullets), (
            f"unexplained workflow additional-load bullet: {path}"
        )
        assert all(
            "/home/j/WatchTowerPlan/AGENTS.md" not in bullet
            and "/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md" not in bullet
            and "/home/j/WatchTowerPlan/workflows/modules/core.md" not in bullet
            and "/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md"
            not in bullet
            and "/home/j/WatchTowerPlan/docs/standards/workflows/"
            "routing_and_context_loading_standard.md" not in bullet
            and "/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md"
            not in bullet
            for bullet in bullets
        ), (
            f"workflow additional-load section repeats routing-baseline files: {path}"
        )
