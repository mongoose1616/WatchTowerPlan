from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.schemas import SchemaStore
from watchtower_core.validation.artifact import ArtifactValidationService

REPO_ROOT = Path(__file__).resolve().parents[4]
FRONT_MATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _load_json_object(path: Path) -> dict[str, object]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _load_front_matter(path: Path) -> dict[str, object]:
    match = FRONT_MATTER_PATTERN.search(path.read_text(encoding="utf-8"))
    assert match is not None, f"missing front matter: {path}"
    loaded = yaml.safe_load(match.group(1))
    assert isinstance(loaded, dict)
    return loaded


def test_schema_catalog_records_match_loaded_schema_documents() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    for record in store.catalog.records:
        schema_document = store.load_schema(record.schema_id)
        assert schema_document["$id"] == record.schema_id
        assert record.canonical_path.exists()


def test_control_plane_loader_loads_current_governed_artifacts() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    catalog = loader.load_schema_catalog()
    validators = loader.load_validator_registry()
    path_index = loader.load_repository_path_index()
    command_index = loader.load_command_index()
    foundation_index = loader.load_foundation_index()
    initiative_index = loader.load_initiative_index()
    coordination_index = loader.load_coordination_index()
    reference_index = loader.load_reference_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()
    task_index = loader.load_task_index()

    assert catalog.artifact_id == "registry.schema_catalog"
    assert validators.artifact_id == "registry.validators"
    assert path_index.artifact_id == "index.repository_paths"
    assert command_index.artifact_id == "index.commands"
    assert foundation_index.artifact_id == "index.foundations"
    assert initiative_index.artifact_id == "index.initiatives"
    assert coordination_index.artifact_id == "index.coordination"
    assert reference_index.artifact_id == "index.references"
    assert standard_index.artifact_id == "index.standards"
    assert workflow_index.artifact_id == "index.workflows"
    assert task_index.artifact_id == "index.tasks"


def test_control_plane_loader_validates_current_traceability_artifacts() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    acceptance_contract = loader.load_validated_document(
        "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json"
    )
    traceability_index = loader.load_validated_document(
        "core/control_plane/indexes/traceability/traceability_index.v1.json"
    )
    validation_evidence = loader.load_validated_document(
        "core/control_plane/ledgers/validation_evidence/"
        "core_python_foundation_traceability_validation.v1.json"
    )
    initiative_index = loader.load_validated_document(
        "core/control_plane/indexes/initiatives/initiative_index.v1.json"
    )
    coordination_index = loader.load_validated_document(
        "core/control_plane/indexes/coordination/coordination_index.v1.json"
    )

    assert acceptance_contract["id"] == "contract.acceptance.core_python_foundation"
    assert traceability_index["id"] == "index.traceability"
    assert validation_evidence["id"] == "evidence.core_python_foundation.traceability_baseline"
    assert initiative_index["id"] == "index.initiatives"
    assert coordination_index["id"] == "index.coordination"


def test_live_governed_json_artifacts_have_active_schema_validation_coverage() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ArtifactValidationService(loader)
    target_roots = (
        REPO_ROOT / "core/control_plane/contracts/acceptance",
        REPO_ROOT / "core/control_plane/contracts/compatibility",
        REPO_ROOT / "core/control_plane/contracts/intake",
        REPO_ROOT / "core/control_plane/indexes/commands",
        REPO_ROOT / "core/control_plane/indexes/coordination",
        REPO_ROOT / "core/control_plane/indexes/decisions",
        REPO_ROOT / "core/control_plane/indexes/design_documents",
        REPO_ROOT / "core/control_plane/indexes/foundations",
        REPO_ROOT / "core/control_plane/indexes/initiatives",
        REPO_ROOT / "core/control_plane/indexes/prds",
        REPO_ROOT / "core/control_plane/indexes/references",
        REPO_ROOT / "core/control_plane/indexes/repository_paths",
        REPO_ROOT / "core/control_plane/indexes/standards",
        REPO_ROOT / "core/control_plane/indexes/tasks",
        REPO_ROOT / "core/control_plane/indexes/traceability",
        REPO_ROOT / "core/control_plane/indexes/workflows",
        REPO_ROOT / "core/control_plane/ledgers/migrations",
        REPO_ROOT / "core/control_plane/ledgers/releases",
        REPO_ROOT / "core/control_plane/ledgers/validation_evidence",
        REPO_ROOT / "core/control_plane/manifests",
        REPO_ROOT / "core/control_plane/policies/release",
        REPO_ROOT / "core/control_plane/registries/artifact_types",
        REPO_ROOT / "core/control_plane/registries/policy_catalog",
        REPO_ROOT / "core/control_plane/registries/schema_catalog",
        REPO_ROOT / "core/control_plane/registries/validators",
    )

    for root in target_roots:
        for path in sorted(root.glob("*.json")):
            result = service.validate(path.relative_to(REPO_ROOT).as_posix())
            assert result.passed, f"{path} failed schema validation: {result.issues}"


def test_initiative_index_examples_validate_against_the_schema() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    valid_example = _load_json_object(
        REPO_ROOT / "core/control_plane/examples/valid/indexes/initiative_index.v1.example.json"
    )
    invalid_example = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/invalid/indexes/"
        "initiative_index_missing_phase.v1.example.json"
    )

    store.validate_instance(valid_example)
    with pytest.raises(ValidationError):
        store.validate_instance(invalid_example)


def test_coordination_index_examples_validate_against_the_schema() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    valid_example = _load_json_object(
        REPO_ROOT / "core/control_plane/examples/valid/indexes/coordination_index.v1.example.json"
    )
    invalid_example = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/invalid/indexes/"
        "coordination_index_missing_mode.v1.example.json"
    )

    store.validate_instance(valid_example)
    with pytest.raises(ValidationError):
        store.validate_instance(invalid_example)


def test_governed_document_front_matter_profiles_validate() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)
    governed_families = [
        (
            REPO_ROOT / "docs/references",
            {
                "AGENTS.md",
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/prds",
            {
                "README.md",
                "prd_tracking.md",
            },
            "urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/decisions",
            {
                "README.md",
                "decision_tracking.md",
            },
            "urn:watchtower:schema:interfaces:documentation:decision-record-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/design/features",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/design/implementation",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/tasks/open",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/planning/tasks/closed",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/standards",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:standard-front-matter:v1",
        ),
        (
            REPO_ROOT / "docs/foundations",
            {
                "README.md",
            },
            "urn:watchtower:schema:interfaces:documentation:foundation-front-matter:v1",
        ),
    ]

    for directory, excluded_names, schema_id in governed_families:
        for path in sorted(directory.rglob("*.md")):
            if path.name in excluded_names:
                continue
            store.validate_instance(_load_front_matter(path), schema_id=schema_id)


def test_utc_timestamp_fields_reject_offset_timestamps() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    prd_front_matter = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/valid/documentation/prd_front_matter.v1.example.json"
    )
    prd_front_matter["updated_at"] = "2026-03-09T05:06:54-04:00"
    with pytest.raises(ValidationError):
        store.validate_instance(
            prd_front_matter,
            schema_id="urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
        )

    validation_evidence = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/valid/ledgers/validation_evidence.v1.example.json"
    )
    validation_evidence["recorded_at"] = "2026-03-09T05:06:54+01:00"
    with pytest.raises(ValidationError):
        store.validate_instance(validation_evidence)


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
            and "/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md"
            not in bullet
            for bullet in bullets
        ), (
            f"workflow additional-load section repeats routing-baseline files: {path}"
        )
