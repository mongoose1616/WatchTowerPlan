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
    rendered_surface_registry = loader.load_rendered_surface_registry()
    workflow_metadata_registry = loader.load_workflow_metadata_registry()
    path_index = loader.load_repository_path_index()
    command_index = loader.load_command_index()
    foundation_index = loader.load_foundation_index()
    initiative_index = loader.load_initiative_index()
    coordination_index = loader.load_coordination_index()
    artifact_index = loader.load_artifact_index()
    reference_index = loader.load_reference_index()
    route_index = loader.load_route_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()
    task_index = loader.load_task_index()

    assert catalog.artifact_id == "registry.schema_catalog"
    assert validators.artifact_id == "registry.validators"
    assert authority_map.artifact_id == "registry.authority_map"
    assert rendered_surface_registry.artifact_id == "registry.rendered_surfaces"
    assert workflow_metadata_registry.artifact_id == "registry.workflow_metadata"
    assert path_index.artifact_id == "index.repository_paths"
    assert command_index.artifact_id == "index.commands"
    assert foundation_index.artifact_id == "index.foundations"
    assert initiative_index.artifact_id == "index.initiatives"
    assert coordination_index.artifact_id == "index.coordination"
    assert artifact_index.surface_name == "artifact_index"
    assert artifact_index.get("index.artifacts").path == "plan/.wt/indexes/artifact_index.json"
    assert reference_index.artifact_id == "index.references"
    assert route_index.artifact_id == "index.routes"
    assert standard_index.artifact_id == "index.standards"
    assert workflow_index.artifact_id == "index.workflows"
    assert task_index.artifact_id == "index.plan_tasks"


def test_foundation_index_exposes_engineering_stack_reference_metadata() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    foundation = loader.load_foundation_index().get("foundation.engineering_stack_direction")

    assert foundation.uses_external_references is True
    assert "core/docs/references/uv_reference.md" in foundation.reference_doc_paths
    assert "core/docs/references/json_schema_2020_12_reference.md" in foundation.reference_doc_paths
    assert "core/docs/references/pytest_reference.md" in foundation.reference_doc_paths
    assert foundation.external_reference_urls


def test_foundations_context_review_loads_foundation_review_and_discovery_routes() -> None:
    workflow_path = REPO_ROOT / "core/workflows/modules/foundations_context_review.md"
    markdown = workflow_path.read_text(encoding="utf-8")

    assert "core/docs/foundations/repository_scope.md" in markdown
    assert "core/docs/foundations/engineering_design_principles.md" in markdown
    assert "core/docs/foundations/repository_standards_posture.md" in markdown
    assert "core/docs/foundations/engineering_stack_direction.md" in markdown
    assert "core/docs/foundations/product_direction.md" in markdown
    assert "core/docs/foundations/customer_story.md" in markdown
    assert "plan/tracking/coordination_tracking.md" in markdown
    assert "SUMMARY.md" not in markdown
    assert "watchtower-core query foundations" in markdown


def test_foundations_family_entrypoints_expose_human_and_machine_routes() -> None:
    foundations_readme = (REPO_ROOT / "core/docs/foundations/README.md").read_text(
        encoding="utf-8"
    )
    repository_scope = (REPO_ROOT / "core/docs/foundations/repository_scope.md").read_text(
        encoding="utf-8"
    )
    foundation_index_readme = (
        REPO_ROOT / "core/control_plane/indexes/foundations/README.md"
    ).read_text(encoding="utf-8")

    assert "core/docs/commands/core_python/watchtower_core_query_foundations.md" in foundations_readme
    assert "core/docs/commands/core_python/watchtower_core_plan_sync_foundation_index.md" in (
        foundations_readme
    )
    assert "core/docs/commands/core_python/watchtower_core_query_foundations.md" in repository_scope
    assert "core/docs/foundations/README.md" in foundation_index_readme
    assert "core/docs/commands/core_python/watchtower_core_query_foundations.md" in (
        foundation_index_readme
    )
    assert "core/docs/commands/core_python/watchtower_core_plan_sync_foundation_index.md" in (
        foundation_index_readme
    )


def test_core_python_command_readme_exposes_foundations_entrypoints() -> None:
    markdown = (REPO_ROOT / "core/docs/commands/core_python/README.md").read_text(encoding="utf-8")

    assert "core/docs/commands/core_python/watchtower_core_query.md" in markdown
    assert "core/docs/commands/core_python/watchtower_core_query_foundations.md" in markdown
    assert "core/docs/commands/core_python/watchtower_core_sync.md" in markdown
    assert "core/docs/commands/core_python/watchtower_core_plan_sync_foundation_index.md" in markdown


def test_foundation_index_standard_operationalizes_foundation_family_surfaces() -> None:
    markdown = (
        REPO_ROOT / "core/docs/standards/data_contracts/foundation_index_standard.md"
    ).read_text(encoding="utf-8")

    assert "plan/python/src/watchtower_plan/sync/foundation_index.py" in markdown
    assert "core/python/src/watchtower_core/query/foundations.py" in markdown
    assert "core/docs/commands/core_python/watchtower_core_query_foundations.md" in markdown
    assert "core/docs/commands/core_python/watchtower_core_plan_sync_foundation_index.md" in markdown
    assert "core/control_plane/indexes/foundations/README.md" in markdown


def test_foundation_document_standard_operationalizes_governed_docs_only() -> None:
    markdown = (
        REPO_ROOT / "core/docs/standards/documentation/foundation_md_standard.md"
    ).read_text(encoding="utf-8")
    operationalization = extract_sections(markdown)["Operationalization"]

    expected_paths = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "core" / "docs" / "foundations").glob("*.md")
        if path.name != "README.md"
    )

    for value in expected_paths:
        assert value in operationalization

    assert "core/docs/foundations/README.md" not in operationalization
    assert "`core/docs/foundations/`" not in operationalization


def test_root_review_entrypoints_route_to_current_tracking_surfaces() -> None:
    root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    foundations_readme = (REPO_ROOT / "core/docs/foundations/README.md").read_text(
        encoding="utf-8"
    )
    repository_scope = (
        REPO_ROOT / "core/docs/foundations/repository_scope.md"
    ).read_text(encoding="utf-8")

    assert "plan/plan_overview.md" in root_readme
    assert "plan/plan_overview.md" in foundations_readme
    assert (
        "[plan_overview.md]"
        "(/plan/plan_overview.md)"
    ) in repository_scope
    assert "SUMMARY.md" not in root_readme
    assert "SUMMARY.md" not in foundations_readme
    assert "SUMMARY.md" not in repository_scope


def test_query_and_sync_command_docs_follow_current_boundary_owners() -> None:
    shared_query_docs = sorted(
        (REPO_ROOT / "core/docs/commands/core_python").glob("watchtower_core_query_*.md")
    )
    reusable_core_query_docs = {
        "watchtower_core_query_acceptance.md",
        "watchtower_core_query_commands.md",
        "watchtower_core_query_evidence.md",
        "watchtower_core_query_foundations.md",
        "watchtower_core_query_paths.md",
        "watchtower_core_query_references.md",
        "watchtower_core_query_standards.md",
        "watchtower_core_query_workflows.md",
    }
    for path in shared_query_docs:
        markdown = path.read_text(encoding="utf-8")
        if path.name in reusable_core_query_docs:
            assert "core/python/src/watchtower_core/query/" in markdown, path
        else:
            assert "core/python/src/watchtower_core/query/" not in markdown, path

    plan_query_docs = sorted(
        (REPO_ROOT / "core/docs/commands/core_python").glob("watchtower_core_plan_query*.md")
    )
    plan_query_docs_with_reusable_core_query_helpers = {
        "watchtower_core_plan_query_authority.md",
        "watchtower_core_plan_query_trace.md",
    }
    for path in plan_query_docs:
        markdown = path.read_text(encoding="utf-8")
        if path.name in plan_query_docs_with_reusable_core_query_helpers:
            assert "core/python/src/watchtower_core/query/" in markdown, path
        else:
            assert "core/python/src/watchtower_core/query/" not in markdown, path

    sync_docs = sorted(
        (REPO_ROOT / "core/docs/commands/core_python").glob("watchtower_core_sync_*.md")
    )
    reusable_core_sync_docs = {
        "watchtower_core_sync.md",
        "watchtower_core_sync_command_index.md",
        "watchtower_core_sync_repository_paths.md",
        "watchtower_core_sync_route_index.md",
    }
    for path in sync_docs:
        markdown = path.read_text(encoding="utf-8")
        if path.name in reusable_core_sync_docs:
            assert "core/python/src/watchtower_core/sync/" in markdown, path
        else:
            assert "core/python/src/watchtower_core/sync/" not in markdown, path


def test_workspace_and_runtime_docs_publish_current_boundary_model() -> None:
    workspace_standard = (
        REPO_ROOT / "core/docs/standards/engineering/python_workspace_standard.md"
    ).read_text(encoding="utf-8")
    python_code_design_standard = (
        REPO_ROOT / "core/docs/standards/engineering/python_code_design_standard.md"
    ).read_text(encoding="utf-8")
    query_readme = (
        REPO_ROOT / "core/python/src/watchtower_core/query/README.md"
    ).read_text(encoding="utf-8")
    package_readme = (
        REPO_ROOT / "core/python/src/watchtower_core/README.md"
    ).read_text(encoding="utf-8")
    plan_python_readme = (
        REPO_ROOT / "plan/python/src/watchtower_plan/README.md"
    ).read_text(encoding="utf-8")
    plan_python_sync_readme = (
        REPO_ROOT / "plan/python/src/watchtower_plan/sync/README.md"
    ).read_text(encoding="utf-8")
    control_plane_readme = (
        REPO_ROOT / "core/python/src/watchtower_core/control_plane/README.md"
    ).read_text(encoding="utf-8")
    workspace_agents = (REPO_ROOT / "core/python/AGENTS.md").read_text(encoding="utf-8")
    workspace_readme = (REPO_ROOT / "core/python/README.md").read_text(encoding="utf-8")
    best_practices_standard = (
        REPO_ROOT / "core/docs/standards/engineering/engineering_best_practices_standard.md"
    ).read_text(encoding="utf-8")

    assert "core/docs/standards/engineering/python_code_design_standard.md" in workspace_standard
    assert "Keep package boundaries explicit:" in python_code_design_standard
    assert "`control_plane/` owns reusable loaders" in python_code_design_standard
    assert (
        "`plan/python/src/watchtower_plan/` and future `watchtower_<pack>` packages own "
        "repository-local or pack-local orchestration"
        in python_code_design_standard
    )
    assert "plan/python/src/watchtower_plan/query/" in workspace_standard
    assert "core/python/src/watchtower_core/documentation/" in workspace_standard
    assert "core/python/src/watchtower_core/query/" in workspace_standard
    assert "plan/python/src/watchtower_plan/sync/" in workspace_standard
    assert "core/python/src/watchtower_core/rebuild/" in workspace_standard
    assert "core/python/src/watchtower_core/routing/" in workspace_standard
    assert "core/python/src/watchtower_core/workflow_execution/" in workspace_standard
    assert "Export-safe generic query services" in workspace_standard
    assert "Export-safe generic sync harness plus repo-shared command, route, and repository-path rebuild services" in workspace_standard
    assert "A reusable-core query helper" in workspace_standard
    assert "plan/python/src/watchtower_plan/" in workspace_standard
    assert "Approved WatchTowerPlan-specific" in workspace_standard
    assert "| `documentation/` | `reusable_core` |" in package_readme
    assert "Classification`: `reusable_core`" in query_readme
    assert "| `query/` | `reusable_core` |" in package_readme
    assert "| `rebuild/` | `reusable_core` |" in package_readme
    assert "| `routing/` | `reusable_core` |" in package_readme
    assert "| `workflow_execution/` | `reusable_core` |" in package_readme
    assert "repo-shared command, route, and repository-path index rebuild services" in package_readme
    assert "core/docs/standards/engineering/python_code_design_standard.md" in package_readme
    assert "approved plan-owned Python boundary" in plan_python_readme
    assert "Repository-local sync services" in plan_python_sync_readme
    assert "Shrink Rules" in plan_python_sync_readme
    assert (
        "core/docs/standards/engineering/python_code_design_standard.md"
        in plan_python_sync_readme
    )
    assert "human_surface_policy.py" in control_plane_readme
    assert "retention_policy.py" in control_plane_readme
    assert "core/docs/standards/engineering/python_code_design_standard.md" in control_plane_readme
    assert "core/docs/standards/engineering/python_code_design_standard.md" in workspace_agents
    assert "core/python/src/watchtower_core/rebuild/README.md" in workspace_readme
    assert "core/python/src/watchtower_core/routing/README.md" in workspace_readme
    assert "core/python/src/watchtower_core/workflow_execution/README.md" in workspace_readme
    assert "core/docs/standards/engineering/python_code_design_standard.md" in workspace_readme
    assert (
        "A new pack-owned query command should add its pack-native service under the "
        "owning pack boundary"
        in best_practices_standard
    )
    assert "core/docs/standards/engineering/python_code_design_standard.md" in (
        best_practices_standard
    )

    for relative_path in (
        "plan/docs/standards/governance/github_collaboration_standard.md",
        "plan/docs/standards/governance/github_task_sync_standard.md",
        "core/docs/references/github_collaboration_reference.md",
        "core/docs/commands/core_python/watchtower_core_plan_sync_github_tasks.md",
    ):
        markdown = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert "plan/python/src/watchtower_plan/sync/github_tasks.py" in markdown
        assert "core/python/src/watchtower_core/sync/github_tasks.py" not in markdown


def test_control_plane_loader_validates_current_traceability_artifacts() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    acceptance_contract = loader.load_validated_document(
        "core/control_plane/contracts/acceptance/"
        "governed_acceptance_example_acceptance.json"
    )
    traceability_index = loader.load_validated_document(
        "core/control_plane/indexes/traceability/traceability_index.json"
    )
    validation_evidence = loader.load_validated_document(
        "core/control_plane/ledgers/validation_evidence/"
        "governed_acceptance_example_validation_baseline.json"
    )
    initiative_index = loader.load_validated_document(
        "plan/.wt/indexes/initiative_index.json"
    )
    coordination_index = loader.load_validated_document(
        "plan/.wt/indexes/coordination_index.json"
    )

    assert acceptance_contract["id"] == (
        "contract.acceptance.governed_acceptance_example"
    )
    assert traceability_index["id"] == "index.traceability"
    assert validation_evidence["id"] == (
        "evidence.governed_acceptance_example.validation_baseline"
    )
    assert initiative_index["id"] == "index.initiatives"
    assert coordination_index["id"] == "index.coordination"
