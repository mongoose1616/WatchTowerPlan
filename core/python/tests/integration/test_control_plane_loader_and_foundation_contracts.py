from __future__ import annotations

from tests.integration.control_plane_artifact_helpers import REPO_ROOT
from watchtower_core.adapters import extract_sections
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.schemas import SchemaStore


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
