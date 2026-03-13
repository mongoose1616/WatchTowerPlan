from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError

from watchtower_core.adapters import extract_sections
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.schemas import SchemaStore
from watchtower_core.repo_ops.standards import parse_standard_operationalization
from watchtower_core.repo_ops.validation.example_artifacts import (
    iter_control_plane_example_paths,
    schema_id_for_control_plane_example,
)
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
    authority_map = loader.load_authority_map()
    workflow_metadata_registry = loader.load_workflow_metadata_registry()
    path_index = loader.load_repository_path_index()
    command_index = loader.load_command_index()
    foundation_index = loader.load_foundation_index()
    initiative_index = loader.load_initiative_index()
    planning_catalog = loader.load_planning_catalog()
    coordination_index = loader.load_coordination_index()
    reference_index = loader.load_reference_index()
    route_index = loader.load_route_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()
    task_index = loader.load_task_index()

    assert catalog.artifact_id == "registry.schema_catalog"
    assert validators.artifact_id == "registry.validators"
    assert authority_map.artifact_id == "registry.authority_map"
    assert workflow_metadata_registry.artifact_id == "registry.workflow_metadata"
    assert path_index.artifact_id == "index.repository_paths"
    assert command_index.artifact_id == "index.commands"
    assert foundation_index.artifact_id == "index.foundations"
    assert initiative_index.artifact_id == "index.initiatives"
    assert planning_catalog.artifact_id == "index.planning_catalog"
    assert coordination_index.artifact_id == "index.coordination"
    assert reference_index.artifact_id == "index.references"
    assert route_index.artifact_id == "index.routes"
    assert standard_index.artifact_id == "index.standards"
    assert workflow_index.artifact_id == "index.workflows"
    assert task_index.artifact_id == "index.tasks"


def test_foundation_index_exposes_engineering_stack_reference_metadata() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    foundation = loader.load_foundation_index().get("foundation.engineering_stack_direction")

    assert foundation.uses_external_references is True
    assert "docs/references/uv_reference.md" in foundation.reference_doc_paths
    assert "docs/references/json_schema_2020_12_reference.md" in foundation.reference_doc_paths
    assert "docs/references/pytest_reference.md" in foundation.reference_doc_paths
    assert foundation.external_reference_urls


def test_foundations_context_review_loads_foundation_review_and_discovery_routes() -> None:
    workflow_path = REPO_ROOT / "workflows/modules/foundations_context_review.md"
    markdown = workflow_path.read_text(encoding="utf-8")

    assert "docs/foundations/repository_scope.md" in markdown
    assert "docs/foundations/engineering_design_principles.md" in markdown
    assert "docs/foundations/repository_standards_posture.md" in markdown
    assert "docs/foundations/engineering_stack_direction.md" in markdown
    assert "docs/foundations/product_direction.md" in markdown
    assert "docs/foundations/customer_story.md" in markdown
    assert "docs/planning/coordination_tracking.md" in markdown
    assert "SUMMARY.md" not in markdown
    assert "watchtower-core query foundations" in markdown


def test_foundations_family_entrypoints_expose_human_and_machine_routes() -> None:
    foundations_readme = (REPO_ROOT / "docs/foundations/README.md").read_text(
        encoding="utf-8"
    )
    repository_scope = (REPO_ROOT / "docs/foundations/repository_scope.md").read_text(
        encoding="utf-8"
    )
    foundation_index_readme = (
        REPO_ROOT / "core/control_plane/indexes/foundations/README.md"
    ).read_text(encoding="utf-8")

    assert "docs/commands/core_python/watchtower_core_query_foundations.md" in foundations_readme
    assert "docs/commands/core_python/watchtower_core_sync_foundation_index.md" in (
        foundations_readme
    )
    assert "docs/commands/core_python/watchtower_core_query_foundations.md" in repository_scope
    assert "docs/foundations/README.md" in foundation_index_readme
    assert "docs/commands/core_python/watchtower_core_query_foundations.md" in (
        foundation_index_readme
    )
    assert "docs/commands/core_python/watchtower_core_sync_foundation_index.md" in (
        foundation_index_readme
    )


def test_core_python_command_readme_exposes_foundations_entrypoints() -> None:
    markdown = (REPO_ROOT / "docs/commands/core_python/README.md").read_text(encoding="utf-8")

    assert "docs/commands/core_python/watchtower_core_query.md" in markdown
    assert "docs/commands/core_python/watchtower_core_query_foundations.md" in markdown
    assert "docs/commands/core_python/watchtower_core_sync.md" in markdown
    assert "docs/commands/core_python/watchtower_core_sync_foundation_index.md" in markdown


def test_foundation_index_standard_operationalizes_foundation_family_surfaces() -> None:
    markdown = (
        REPO_ROOT / "docs/standards/data_contracts/foundation_index_standard.md"
    ).read_text(encoding="utf-8")

    assert "core/python/src/watchtower_core/repo_ops/sync/foundation_index.py" in markdown
    assert "core/python/src/watchtower_core/repo_ops/query/foundations.py" in markdown
    assert "docs/commands/core_python/watchtower_core_query_foundations.md" in markdown
    assert "docs/commands/core_python/watchtower_core_sync_foundation_index.md" in markdown
    assert "core/control_plane/indexes/foundations/README.md" in markdown


def test_foundation_document_standard_operationalizes_governed_docs_only() -> None:
    markdown = (
        REPO_ROOT / "docs/standards/documentation/foundation_md_standard.md"
    ).read_text(encoding="utf-8")
    operationalization = extract_sections(markdown)["Operationalization"]

    expected_paths = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "docs" / "foundations").glob("*.md")
        if path.name != "README.md"
    )

    for value in expected_paths:
        assert value in operationalization

    assert "docs/foundations/README.md" not in operationalization
    assert "`docs/foundations/`" not in operationalization


def test_root_review_entrypoints_route_to_current_tracking_surfaces() -> None:
    root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    foundations_readme = (REPO_ROOT / "docs/foundations/README.md").read_text(
        encoding="utf-8"
    )
    repository_scope = (
        REPO_ROOT / "docs/foundations/repository_scope.md"
    ).read_text(encoding="utf-8")

    assert "docs/planning/coordination_tracking.md" in root_readme
    assert "docs/planning/coordination_tracking.md" in foundations_readme
    assert (
        "[coordination_tracking.md]"
        "(/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)"
    ) in repository_scope
    assert "SUMMARY.md" not in root_readme
    assert "SUMMARY.md" not in foundations_readme
    assert "SUMMARY.md" not in repository_scope


def test_repo_local_query_and_sync_command_docs_point_to_repo_ops_owners() -> None:
    query_docs = sorted(
        (REPO_ROOT / "docs/commands/core_python").glob("watchtower_core_query_*.md")
    )
    for path in query_docs:
        markdown = path.read_text(encoding="utf-8")
        assert "core/python/src/watchtower_core/query/" not in markdown, path

    sync_docs = sorted(
        (REPO_ROOT / "docs/commands/core_python").glob("watchtower_core_sync_*.md")
    )
    for path in sync_docs:
        markdown = path.read_text(encoding="utf-8")
        assert "core/python/src/watchtower_core/sync/" not in markdown, path


def test_workspace_and_github_docs_publish_current_repo_ops_ownership_model() -> None:
    workspace_standard = (
        REPO_ROOT / "docs/standards/engineering/python_workspace_standard.md"
    ).read_text(encoding="utf-8")
    best_practices_standard = (
        REPO_ROOT / "docs/standards/engineering/engineering_best_practices_standard.md"
    ).read_text(encoding="utf-8")

    assert "core/python/src/watchtower_core/repo_ops/query/" in workspace_standard
    assert "core/python/src/watchtower_core/repo_ops/sync/" in workspace_standard
    assert "Compatibility query namespace" in workspace_standard
    assert "Compatibility sync namespace" in workspace_standard
    assert "A repo-local query helper" in workspace_standard
    assert (
        "core/python/src/watchtower_core/query/` | Index-backed retrieval and structured query "
        "helpers."
    ) not in workspace_standard
    assert "core/python/src/watchtower_core/repo_ops/query/" in best_practices_standard

    for relative_path in (
        "docs/standards/governance/github_collaboration_standard.md",
        "docs/standards/governance/github_task_sync_standard.md",
        "docs/references/github_collaboration_reference.md",
        "docs/commands/core_python/watchtower_core_sync_github_tasks.md",
    ):
        markdown = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert "core/python/src/watchtower_core/repo_ops/sync/github_tasks.py" in markdown
        assert "core/python/src/watchtower_core/sync/github_tasks.py" not in markdown


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
        REPO_ROOT / "core/control_plane/indexes/planning",
        REPO_ROOT / "core/control_plane/indexes/prds",
        REPO_ROOT / "core/control_plane/indexes/references",
        REPO_ROOT / "core/control_plane/indexes/repository_paths",
        REPO_ROOT / "core/control_plane/indexes/routes",
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
        REPO_ROOT / "core/control_plane/registries/authority_map",
        REPO_ROOT / "core/control_plane/registries/policy_catalog",
        REPO_ROOT / "core/control_plane/registries/schema_catalog",
        REPO_ROOT / "core/control_plane/registries/validators",
        REPO_ROOT / "core/control_plane/registries/workflows",
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


def test_live_governed_applies_to_directory_paths_are_canonical() -> None:
    markdown_roots = (
        REPO_ROOT / "docs/references",
        REPO_ROOT / "docs/foundations",
        REPO_ROOT / "docs/standards",
        REPO_ROOT / "docs/planning/prds",
        REPO_ROOT / "docs/planning/decisions",
        REPO_ROOT / "docs/planning/design/features",
        REPO_ROOT / "docs/planning/design/implementation",
        REPO_ROOT / "docs/planning/tasks/open",
        REPO_ROOT / "docs/planning/tasks/closed",
    )

    for root in markdown_roots:
        for path in sorted(root.rglob("*.md")):
            if path.name in {"README.md", "AGENTS.md"}:
                continue
            if FRONT_MATTER_PATTERN.search(path.read_text(encoding="utf-8")) is None:
                continue
            front_matter = _load_front_matter(path)
            applies_to = front_matter.get("applies_to")
            if not isinstance(applies_to, list):
                continue
            for value in applies_to:
                assert isinstance(value, str)
                if "/" not in value or "*" in value or "<" in value:
                    continue
                target = REPO_ROOT / value.rstrip("/")
                assert target.exists(), f"{path} applies_to path does not exist: {value}"
                if target.is_dir():
                    assert value.endswith("/"), (
                        f"{path} directory applies_to path must end in '/': {value}"
                    )
                else:
                    assert not value.endswith("/"), (
                        f"{path} file applies_to path must not end in '/': {value}"
                    )

    for path in sorted((REPO_ROOT / "core/control_plane/examples").rglob("*.json")):
        payload = _load_json_object(path)
        applies_to = payload.get("applies_to")
        if not isinstance(applies_to, list):
            continue
        for value in applies_to:
            assert isinstance(value, str)
            if "/" not in value or "*" in value or "<" in value:
                continue
            target = REPO_ROOT / value.rstrip("/")
            assert target.exists(), f"{path} applies_to path does not exist: {value}"
            if target.is_dir():
                assert value.endswith("/"), (
                    f"{path} directory applies_to path must end in '/': {value}"
                )
            else:
                assert not value.endswith("/"), (
                    f"{path} file applies_to path must not end in '/': {value}"
                )


def test_all_valid_control_plane_examples_validate_against_their_schemas() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    for relative_path in iter_control_plane_example_paths(REPO_ROOT, validity="valid"):
        payload = _load_json_object(REPO_ROOT / relative_path)
        store.validate_instance(
            payload,
            schema_id=schema_id_for_control_plane_example(REPO_ROOT, relative_path),
        )


def test_all_invalid_control_plane_examples_fail_against_their_schemas() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    for relative_path in iter_control_plane_example_paths(REPO_ROOT, validity="invalid"):
        payload = _load_json_object(REPO_ROOT / relative_path)
        with pytest.raises(ValidationError):
            store.validate_instance(
                payload,
                schema_id=schema_id_for_control_plane_example(REPO_ROOT, relative_path),
            )


def test_planning_catalog_examples_validate_against_the_schema() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    valid_example = _load_json_object(
        REPO_ROOT / "core/control_plane/examples/valid/indexes/planning_catalog.v1.example.json"
    )
    invalid_example = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/invalid/indexes/"
        "planning_catalog_missing_coordination.v1.example.json"
    )

    store.validate_instance(valid_example)
    with pytest.raises(ValidationError):
        store.validate_instance(invalid_example)


def test_route_index_examples_validate_against_the_schema() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    valid_example = _load_json_object(
        REPO_ROOT / "core/control_plane/examples/valid/indexes/route_index.v1.example.json"
    )
    invalid_example = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/invalid/indexes/"
        "route_index_missing_workflow_ids.v1.example.json"
    )

    store.validate_instance(valid_example)
    with pytest.raises(ValidationError):
        store.validate_instance(invalid_example)


def test_workflow_metadata_registry_examples_validate_against_the_schema() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    valid_example = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/valid/registries/"
        "workflow_metadata_registry.v1.example.json"
    )
    invalid_example = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/invalid/registries/"
        "workflow_metadata_registry_missing_phase_type.v1.example.json"
    )

    store.validate_instance(valid_example)
    with pytest.raises(ValidationError):
        store.validate_instance(invalid_example)


def test_authority_map_examples_validate_against_the_schema() -> None:
    store = SchemaStore.from_repo_root(REPO_ROOT)

    valid_example = _load_json_object(
        REPO_ROOT / "core/control_plane/examples/valid/registries/authority_map.v1.example.json"
    )
    invalid_example = _load_json_object(
        REPO_ROOT
        / "core/control_plane/examples/invalid/registries/"
        "authority_map_missing_command.v1.example.json"
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
    assert "> Use `# \\`.\\`` when the template is instantiated at the repository root." in markdown
    assert "<Directory Name>" not in markdown
    assert "<current-directory>/README.md" not in markdown
    assert "<repo-relative-path-to-this-readme>" in markdown
    assert markdown.index("## Files") < markdown.index("## Boundaries")
    assert markdown.index("## Files") < markdown.index("## Notes")


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
